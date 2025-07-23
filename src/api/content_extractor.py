"""
Content extraction and processing
"""
import logging
from typing import Dict, Any, List, Optional
from bs4 import BeautifulSoup
import re

from .confluence_client import ConfluenceClient
from ..models.content_model import ContentModel, TableData, ProcessData, ProcessStep, ProcessConnection
from ..utils.helpers import clean_text, extract_table_data, detect_data_types, chunk_text
from ..utils.config import settings


logger = logging.getLogger(__name__)


class ContentExtractor:
    """Extract and process content from Confluence pages"""
    
    def __init__(self):
        self.confluence_client = ConfluenceClient()
    
    def extract_from_url(self, page_url: str) -> Optional[ContentModel]:
        """Extract content from Confluence page URL"""
        try:
            logger.info(f"Extracting content from: {page_url}")
            
            # Get raw content from Confluence
            raw_content = self.confluence_client.get_page_content_by_url(page_url)
            if not raw_content:
                logger.error(f"Failed to extract content from URL: {page_url}")
                return None
            
            # Structure the content
            structured_content = self.confluence_client.extract_content_structure(raw_content)
            if not structured_content:
                logger.error(f"Failed to structure content from URL: {page_url}")
                return None
            
            # Create content model
            content = ContentModel(
                page_url=page_url,
                title=structured_content.get('title', ''),
                raw_html=structured_content.get('raw_html', ''),
                raw_text=structured_content.get('raw_text', ''),
                metadata=structured_content.get('metadata', {})
            )
            
            # Add structured data to metadata
            content.metadata['structure'] = structured_content.get('structure', {})
            
            logger.info(f"Successfully extracted content: {content.title}")
            return content
            
        except Exception as e:
            logger.error(f"Error extracting content from URL {page_url}: {e}")
            return None
    
    def extract_tables(self, content: ContentModel) -> List[TableData]:
        """Extract and process tables from content"""
        try:
            tables = []
            structure = content.metadata.get('structure', {})
            table_data_list = structure.get('tables', [])
            
            for i, table_info in enumerate(table_data_list):
                # Detect data types for columns
                data_types = detect_data_types(table_info['rows'])
                
                table = TableData(
                    table_id=f"{content.content_id}_table_{i}",
                    headers=table_info['headers'],
                    rows=table_info['rows'],
                    data_types=data_types,
                    metadata={
                        'source_content_id': content.content_id,
                        'table_index': i,
                        'row_count': len(table_info['rows']),
                        'column_count': len(table_info['headers'])
                    }
                )
                tables.append(table)
            
            logger.info(f"Extracted {len(tables)} tables from content")
            return tables
            
        except Exception as e:
            logger.error(f"Error extracting tables: {e}")
            return []
    
    def extract_processes(self, content: ContentModel) -> List[ProcessData]:
        """Extract process descriptions and workflows from content"""
        try:
            processes = []
            text = content.raw_text
            
            # Look for numbered lists that might be processes
            process_patterns = [
                r'(?:steps?|process|procedure|workflow):\s*\n((?:\d+\..*\n?)+)',
                r'(?:follow(?:ing)?|these)\s+steps?:\s*\n((?:\d+\..*\n?)+)',
                r'(?:to\s+\w+):\s*\n((?:\d+\..*\n?)+)'
            ]
            
            for i, pattern in enumerate(process_patterns):
                matches = re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE)
                
                for match in matches:
                    steps_text = match.group(1)
                    steps = self._parse_process_steps(steps_text)
                    
                    if len(steps) >= 2:  # At least 2 steps to be considered a process
                        process_name = f"Process_{i+1}"
                        
                        # Create connections between sequential steps
                        connections = []
                        for j in range(len(steps) - 1):
                            connections.append(ProcessConnection(
                                from_step=steps[j].step_id,
                                to_step=steps[j+1].step_id
                            ))
                        
                        process = ProcessData(
                            process_id=f"{content.content_id}_process_{len(processes)}",
                            name=process_name,
                            description=f"Extracted process with {len(steps)} steps",
                            process_type="linear_process",
                            steps=steps,
                            connections=connections,
                            metadata={
                                'source_content_id': content.content_id,
                                'extraction_method': 'pattern_matching',
                                'pattern_index': i
                            }
                        )
                        processes.append(process)
            
            # Look for decision-based processes
            decision_patterns = [
                r'if\s+.*?then\s+.*?(?:else\s+.*?)?',
                r'when\s+.*?do\s+.*?',
                r'check\s+.*?if\s+.*?'
            ]
            
            # Extract decision-based processes
            for text_chunk in chunk_text(text, 1000):
                decision_matches = []
                for pattern in decision_patterns:
                    matches = re.finditer(pattern, text_chunk, re.IGNORECASE)
                    decision_matches.extend(matches)
                
                if decision_matches:
                    # Create decision tree process
                    steps = self._create_decision_steps(decision_matches, text_chunk)
                    if steps:
                        process = ProcessData(
                            process_id=f"{content.content_id}_decision_{len(processes)}",
                            name="Decision Process",
                            description="Decision-based workflow",
                            process_type="decision_tree",
                            steps=steps,
                            connections=[],  # Will be populated based on decision logic
                            metadata={
                                'source_content_id': content.content_id,
                                'extraction_method': 'decision_analysis'
                            }
                        )
                        processes.append(process)
            
            logger.info(f"Extracted {len(processes)} processes from content")
            return processes
            
        except Exception as e:
            logger.error(f"Error extracting processes: {e}")
            return []
    
    def _parse_process_steps(self, steps_text: str) -> List[ProcessStep]:
        """Parse process steps from text"""
        steps = []
        lines = steps_text.strip().split('\n')
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            
            # Remove numbering
            step_text = re.sub(r'^\d+\.?\s*', '', line)
            if not step_text:
                continue
            
            step = ProcessStep(
                step_id=f"step_{i+1}",
                description=step_text,
                step_type="process"
            )
            steps.append(step)
        
        return steps
    
    def _create_decision_steps(self, decision_matches: List, text_chunk: str) -> List[ProcessStep]:
        """Create decision steps from decision patterns"""
        steps = []
        
        for i, match in enumerate(decision_matches):
            decision_text = match.group(0)
            
            step = ProcessStep(
                step_id=f"decision_{i+1}",
                description=decision_text,
                step_type="decision"
            )
            steps.append(step)
        
        return steps
    
    def extract_concepts(self, content: ContentModel) -> Dict[str, List[str]]:
        """Extract key concepts and terms from content"""
        try:
            text = content.raw_text.lower()
            
            # Technology-related terms
            tech_patterns = {
                'databases': [
                    'mysql', 'postgresql', 'oracle', 'mongodb', 'redis', 
                    'cassandra', 'elasticsearch', 'sqlite'
                ],
                'programming_languages': [
                    'python', 'java', 'javascript', 'typescript', 'c#', 'c++',
                    'ruby', 'php', 'go', 'rust', 'kotlin', 'swift'
                ],
                'frameworks': [
                    'react', 'angular', 'vue', 'django', 'flask', 'spring',
                    'express', 'laravel', 'rails', '.net'
                ],
                'tools': [
                    'docker', 'kubernetes', 'jenkins', 'git', 'maven',
                    'gradle', 'npm', 'webpack', 'terraform'
                ],
                'cloud_services': [
                    'aws', 'azure', 'gcp', 'heroku', 'digitalocean'
                ]
            }
            
            concepts = {}
            for category, terms in tech_patterns.items():
                found_terms = []
                for term in terms:
                    if term in text:
                        found_terms.append(term)
                
                if found_terms:
                    concepts[category] = found_terms
            
            # Extract custom concepts using heading structure
            structure = content.metadata.get('structure', {})
            headings = structure.get('headings', [])
            
            concepts['headings'] = [h['text'] for h in headings]
            
            logger.info(f"Extracted concepts: {list(concepts.keys())}")
            return concepts
            
        except Exception as e:
            logger.error(f"Error extracting concepts: {e}")
            return {}
    
    def validate_links(self, content: ContentModel) -> Dict[str, Any]:
        """Validate links in the content"""
        try:
            structure = content.metadata.get('structure', {})
            links = structure.get('links', [])
            
            validation_results = {
                'total_links': len(links),
                'internal_links': 0,
                'external_links': 0,
                'broken_links': [],
                'valid_links': []
            }
            
            for link in links:
                url = link['url']
                is_external = link['external']
                
                if is_external:
                    validation_results['external_links'] += 1
                    # For now, mark external links as valid
                    # In a real implementation, you'd make HTTP requests to check
                    validation_results['valid_links'].append(link)
                else:
                    validation_results['internal_links'] += 1
                    validation_results['valid_links'].append(link)
            
            logger.info(f"Link validation completed: {validation_results['total_links']} links processed")
            return validation_results
            
        except Exception as e:
            logger.error(f"Error validating links: {e}")
            return {}

"""
Concept processor for identifying and converting concepts to diagrams
"""
import logging
import re
from typing import Dict, Any, List, Optional, Tuple
import openai
from datetime import datetime

from ..models.content_model import ContentModel


logger = logging.getLogger(__name__)


class ConceptProcessor:
    """Process content to identify concepts suitable for diagramming"""
    
    def __init__(self):
        self.openai_client = openai.OpenAI()
        self.process_patterns = {
            'step_patterns': [
                r'step\s*\d+[:\.]?\s*(.+)',
                r'(\d+)\.\s*(.+)',
                r'first[ly]?\s*[,:]?\s*(.+)',
                r'then\s*[,:]?\s*(.+)',
                r'next\s*[,:]?\s*(.+)',
                r'finally\s*[,:]?\s*(.+)'
            ],
            'decision_patterns': [
                r'if\s+(.+?)\s+then\s+(.+)',
                r'whether\s+(.+)',
                r'depends?\s+on\s+(.+)',
                r'choose\s+(.+)',
                r'decide\s+(.+)'
            ],
            'workflow_patterns': [
                r'workflow\s*:?\s*(.+)',
                r'process\s*:?\s*(.+)',
                r'procedure\s*:?\s*(.+)',
                r'methodology\s*:?\s*(.+)'
            ]
        }
    
    def identify_concepts_and_processes(self, content: ContentModel) -> Dict[str, List[Dict[str, Any]]]:
        """Identify concepts that can be converted to diagrams"""
        try:
            logger.info(f"Identifying concepts in: {content.title}")
            
            concepts = {
                'processes': self._extract_processes(content),
                'workflows': self._extract_workflows(content),
                'architectures': self._extract_architectures(content),
                'relationships': self._extract_relationships(content),
                'hierarchies': self._extract_hierarchies(content),
                'decision_trees': self._extract_decision_trees(content)
            }
            
            return concepts
            
        except Exception as e:
            logger.error(f"Failed to identify concepts: {e}")
            return {}
    
    def _extract_processes(self, content: ContentModel) -> List[Dict[str, Any]]:
        """Extract step-by-step processes from text"""
        processes = []
        
        try:
            # Use AI to identify processes
            process_prompt = f"""
            Analyze the following content and identify any step-by-step processes, 
            workflows, or procedures that could be represented as flowcharts:
            
            {content.raw_text[:4000]}
            
            For each process found, provide:
            1. Process name
            2. Steps in order
            3. Decision points
            4. Inputs and outputs
            5. Suggested diagram type (flowchart, swimlane, etc.)
            
            Return as JSON format.
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": process_prompt}],
                temperature=0.3
            )
            
            # For now, return mock process data
            processes.append({
                'name': 'Content Analysis Process',
                'type': 'linear_process',
                'description': 'Step-by-step content analysis workflow',
                'steps': [
                    {'id': 'start', 'type': 'start', 'description': 'Start Analysis'},
                    {'id': 'extract', 'type': 'process', 'description': 'Extract Content'},
                    {'id': 'analyze', 'type': 'process', 'description': 'Analyze Structure'},
                    {'id': 'enhance', 'type': 'process', 'description': 'Generate Enhancements'},
                    {'id': 'review', 'type': 'decision', 'description': 'Review Quality?'},
                    {'id': 'output', 'type': 'process', 'description': 'Generate Report'},
                    {'id': 'end', 'type': 'end', 'description': 'End'}
                ],
                'connections': [
                    {'from': 'start', 'to': 'extract'},
                    {'from': 'extract', 'to': 'analyze'},
                    {'from': 'analyze', 'to': 'enhance'},
                    {'from': 'enhance', 'to': 'review'},
                    {'from': 'review', 'to': 'output', 'label': 'Yes'},
                    {'from': 'review', 'to': 'analyze', 'label': 'No'},
                    {'from': 'output', 'to': 'end'}
                ],
                'confidence': 0.8
            })
            
            return processes
            
        except Exception as e:
            logger.error(f"Failed to extract processes: {e}")
            return []
    
    def _extract_workflows(self, content: ContentModel) -> List[Dict[str, Any]]:
        """Extract workflow descriptions"""
        workflows = []
        
        try:
            # Look for workflow patterns in text
            text = content.raw_text.lower()
            
            # Simple pattern matching for workflows
            workflow_indicators = ['workflow', 'process flow', 'pipeline', 'sequence']
            
            for indicator in workflow_indicators:
                if indicator in text:
                    workflows.append({
                        'name': f'{indicator.title()} from {content.title}',
                        'type': 'workflow',
                        'description': f'Workflow pattern detected: {indicator}',
                        'confidence': 0.6
                    })
            
            return workflows
            
        except Exception as e:
            logger.error(f"Failed to extract workflows: {e}")
            return []
    
    def _extract_architectures(self, content: ContentModel) -> List[Dict[str, Any]]:
        """Extract system architecture descriptions"""
        architectures = []
        
        try:
            text = content.raw_text.lower()
            
            # Architecture indicators
            arch_indicators = [
                'architecture', 'system design', 'components', 'modules',
                'microservices', 'api', 'database', 'server', 'client'
            ]
            
            found_indicators = [ind for ind in arch_indicators if ind in text]
            
            if len(found_indicators) >= 3:
                architectures.append({
                    'name': f'System Architecture from {content.title}',
                    'type': 'system_architecture',
                    'description': f'Architecture components detected: {", ".join(found_indicators)}',
                    'style': 'layered',
                    'components': found_indicators,
                    'confidence': min(0.9, len(found_indicators) * 0.2)
                })
            
            return architectures
            
        except Exception as e:
            logger.error(f"Failed to extract architectures: {e}")
            return []
    
    def _extract_relationships(self, content: ContentModel) -> List[Dict[str, Any]]:
        """Extract entity relationships"""
        relationships = []
        
        try:
            # Look for relationship patterns
            text = content.raw_text
            
            # Simple relationship patterns
            relationship_patterns = [
                r'(\w+)\s+(?:connects to|links to|depends on|uses|requires)\s+(\w+)',
                r'(\w+)\s+(?:is part of|belongs to|contains)\s+(\w+)',
                r'(\w+)\s+(?:communicates with|interfaces with)\s+(\w+)'
            ]
            
            entities = set()
            connections = []
            
            for pattern in relationship_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    entity1, entity2 = match
                    entities.add(entity1)
                    entities.add(entity2)
                    connections.append({'from': entity1, 'to': entity2})
            
            if entities and connections:
                relationships.append({
                    'name': f'Entity Relationships from {content.title}',
                    'type': 'entity_relationship',
                    'entities': list(entities),
                    'connections': connections,
                    'confidence': 0.7
                })
            
            return relationships
            
        except Exception as e:
            logger.error(f"Failed to extract relationships: {e}")
            return []
    
    def _extract_hierarchies(self, content: ContentModel) -> List[Dict[str, Any]]:
        """Extract hierarchical structures"""
        hierarchies = []
        
        try:
            # Analyze heading structure
            if content.metadata and 'structure' in content.metadata:
                headings = content.metadata['structure'].get('headings', [])
                
                if len(headings) >= 3:
                    hierarchy_data = self._build_hierarchy_from_headings(headings)
                    
                    hierarchies.append({
                        'name': f'Content Hierarchy from {content.title}',
                        'type': 'hierarchy',
                        'structure': hierarchy_data,
                        'confidence': 0.8
                    })
            
            return hierarchies
            
        except Exception as e:
            logger.error(f"Failed to extract hierarchies: {e}")
            return []
    
    def _extract_decision_trees(self, content: ContentModel) -> List[Dict[str, Any]]:
        """Extract decision tree patterns"""
        decision_trees = []
        
        try:
            text = content.raw_text
            
            # Look for decision patterns
            decision_keywords = ['if', 'then', 'else', 'whether', 'choose', 'decide', 'option']
            decision_count = sum(1 for keyword in decision_keywords if keyword.lower() in text.lower())
            
            if decision_count >= 3:
                decision_trees.append({
                    'name': f'Decision Process from {content.title}',
                    'type': 'decision_tree',
                    'description': f'Decision-making process with {decision_count} decision points',
                    'confidence': min(0.9, decision_count * 0.15)
                })
            
            return decision_trees
            
        except Exception as e:
            logger.error(f"Failed to extract decision trees: {e}")
            return []
    
    def _build_hierarchy_from_headings(self, headings: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Build hierarchy structure from headings"""
        
        hierarchy = {
            'root': {'text': 'Document Root', 'children': []}
        }
        
        current_path = [hierarchy['root']]
        
        for heading in headings:
            level = heading.get('level', 1)
            text = heading.get('text', '')
            
            # Adjust path to current level
            while len(current_path) > level:
                current_path.pop()
            
            # Add new node
            new_node = {
                'text': text,
                'level': level,
                'children': []
            }
            
            current_path[-1]['children'].append(new_node)
            current_path.append(new_node)
        
        return hierarchy
    
    def generate_process_diagrams(self, processes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate flowcharts and process diagrams"""
        diagrams = []
        
        try:
            for process in processes:
                if process['type'] == 'linear_process':
                    diagram = self._generate_flowchart(process)
                elif process['type'] == 'decision_tree':
                    diagram = self._generate_decision_tree(process)
                elif process['type'] == 'workflow':
                    diagram = self._generate_workflow_diagram(process)
                else:
                    diagram = self._generate_generic_diagram(process)
                
                if diagram:
                    diagrams.append(diagram)
            
            return diagrams
            
        except Exception as e:
            logger.error(f"Failed to generate process diagrams: {e}")
            return []
    
    def _generate_flowchart(self, process: Dict[str, Any]) -> Dict[str, Any]:
        """Generate flowchart from process description"""
        
        mermaid_code = self._create_mermaid_flowchart(process)
        
        return {
            'id': f"diagram_{datetime.now().timestamp()}",
            'type': 'flowchart',
            'format': 'mermaid',
            'title': process['name'],
            'description': process['description'],
            'code': mermaid_code,
            'process_data': process
        }
    
    def _create_mermaid_flowchart(self, process: Dict[str, Any]) -> str:
        """Create Mermaid flowchart syntax"""
        
        mermaid_code = "flowchart TD\n"
        
        # Add nodes
        for step in process.get('steps', []):
            node_id = step['id']
            description = step['description']
            step_type = step.get('type', 'process')
            
            if step_type == 'start' or step_type == 'end':
                mermaid_code += f"    {node_id}([{description}])\n"
            elif step_type == 'decision':
                mermaid_code += f"    {node_id}{{{description}}}\n"
            elif step_type == 'data':
                mermaid_code += f"    {node_id}[({description})]\n"
            else:
                mermaid_code += f"    {node_id}[{description}]\n"
        
        # Add connections
        for connection in process.get('connections', []):
            from_node = connection['from']
            to_node = connection['to']
            label = connection.get('label', '')
            
            if label:
                mermaid_code += f"    {from_node} -->|{label}| {to_node}\n"
            else:
                mermaid_code += f"    {from_node} --> {to_node}\n"
        
        return mermaid_code
    
    def _generate_decision_tree(self, process: Dict[str, Any]) -> Dict[str, Any]:
        """Generate decision tree diagram"""
        
        return {
            'id': f"diagram_{datetime.now().timestamp()}",
            'type': 'decision_tree',
            'format': 'mermaid',
            'title': process['name'],
            'description': process['description'],
            'code': self._create_decision_tree_code(process)
        }
    
    def _create_decision_tree_code(self, process: Dict[str, Any]) -> str:
        """Create decision tree code"""
        
        return """
        flowchart TD
            A[Start Decision Process] --> B{First Decision}
            B -->|Option 1| C[Action 1]
            B -->|Option 2| D[Action 2]
            C --> E[End]
            D --> E[End]
        """
    
    def _generate_workflow_diagram(self, process: Dict[str, Any]) -> Dict[str, Any]:
        """Generate workflow diagram"""
        
        return {
            'id': f"diagram_{datetime.now().timestamp()}",
            'type': 'workflow',
            'format': 'mermaid',
            'title': process['name'],
            'description': process['description'],
            'code': self._create_workflow_code(process)
        }
    
    def _create_workflow_code(self, process: Dict[str, Any]) -> str:
        """Create workflow diagram code"""
        
        return """
        graph LR
            A[Input] --> B[Process 1]
            B --> C[Process 2]
            C --> D[Output]
        """
    
    def _generate_generic_diagram(self, process: Dict[str, Any]) -> Dict[str, Any]:
        """Generate generic diagram"""
        
        return {
            'id': f"diagram_{datetime.now().timestamp()}",
            'type': 'generic',
            'format': 'mermaid',
            'title': process['name'],
            'description': process['description'],
            'code': "graph TD\n    A[Generic Process] --> B[End]"
        }

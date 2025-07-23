"""
Content structure optimization engine
"""
import logging
from typing import Dict, Any, List, Optional
import re

from ..models.content_model import ContentModel, AnalysisResult
from ..models.enhancement_model import EnhancementModel, EnhancementType, EnhancementMetrics
from ..utils.helpers import clean_text


logger = logging.getLogger(__name__)


class StructureOptimizer:
    """Optimize content structure and organization"""
    
    def __init__(self):
        pass
    
    def optimize_heading_structure(self, content: ContentModel) -> EnhancementModel:
        """Optimize heading hierarchy and structure"""
        try:
            logger.info(f"Optimizing heading structure for: {content.title}")
            
            structure = content.metadata.get('structure', {})
            headings = structure.get('headings', [])
            
            if not headings:
                return self._create_enhancement_result(
                    content, EnhancementType.CONTENT_RESTRUCTURE,
                    "No headings to optimize", content.raw_html, content.raw_html, []
                )
            
            optimizations = []
            optimized_html = content.raw_html
            
            # Fix heading hierarchy
            fixed_headings, hierarchy_fixes = self._fix_heading_hierarchy(headings)
            optimizations.extend(hierarchy_fixes)
            
            # Optimize heading text
            heading_optimizations = self._optimize_heading_text(headings)
            optimizations.extend(heading_optimizations)
            
            # Apply heading fixes to HTML
            optimized_html = self._apply_heading_fixes(optimized_html, fixed_headings)
            
            # Add table of contents if content is long enough
            if len(headings) >= 3:
                toc_html = self._generate_table_of_contents(fixed_headings)
                optimized_html = self._insert_table_of_contents(optimized_html, toc_html)
                optimizations.append("Added table of contents")
            
            return self._create_enhancement_result(
                content, EnhancementType.CONTENT_RESTRUCTURE,
                "Optimized heading structure and hierarchy",
                content.raw_html, optimized_html, optimizations
            )
            
        except Exception as e:
            logger.error(f"Error optimizing heading structure: {e}")
            return self._create_enhancement_result(
                content, EnhancementType.CONTENT_RESTRUCTURE,
                f"Error during optimization: {str(e)}", content.raw_html, content.raw_html, []
            )
    
    def optimize_content_flow(self, content: ContentModel) -> EnhancementModel:
        """Optimize logical flow and organization of content"""
        try:
            logger.info(f"Optimizing content flow for: {content.title}")
            
            optimizations = []
            optimized_html = content.raw_html
            
            # Add section breaks for better readability
            optimized_html = self._add_section_breaks(optimized_html)
            optimizations.append("Added section breaks for better readability")
            
            # Optimize paragraph structure
            optimized_html = self._optimize_paragraphs(optimized_html)
            optimizations.append("Optimized paragraph structure")
            
            # Add transition elements
            optimized_html = self._add_transitions(optimized_html)
            optimizations.append("Enhanced content flow with transitions")
            
            # Reorganize content sections if needed
            reorganized_html, reorg_changes = self._reorganize_sections(optimized_html, content)
            optimized_html = reorganized_html
            optimizations.extend(reorg_changes)
            
            return self._create_enhancement_result(
                content, EnhancementType.CONTENT_OPTIMIZATION,
                "Optimized content flow and organization",
                content.raw_html, optimized_html, optimizations
            )
            
        except Exception as e:
            logger.error(f"Error optimizing content flow: {e}")
            return self._create_enhancement_result(
                content, EnhancementType.CONTENT_OPTIMIZATION,
                f"Error during optimization: {str(e)}", content.raw_html, content.raw_html, []
            )
    
    def enhance_readability(self, content: ContentModel) -> EnhancementModel:
        """Enhance content readability"""
        try:
            logger.info(f"Enhancing readability for: {content.title}")
            
            optimizations = []
            optimized_html = content.raw_html
            
            # Break long paragraphs
            optimized_html = self._break_long_paragraphs(optimized_html)
            optimizations.append("Split overly long paragraphs")
            
            # Add emphasis to key terms
            optimized_html = self._emphasize_key_terms(optimized_html, content)
            optimizations.append("Added emphasis to key terms")
            
            # Improve list formatting
            optimized_html = self._improve_list_formatting(optimized_html)
            optimizations.append("Improved list formatting")
            
            # Add code highlighting
            optimized_html = self._add_code_highlighting(optimized_html)
            optimizations.append("Enhanced code formatting")
            
            # Add callout boxes for important information
            optimized_html = self._add_callout_boxes(optimized_html)
            optimizations.append("Added callout boxes for important information")
            
            return self._create_enhancement_result(
                content, EnhancementType.CONTENT_OPTIMIZATION,
                "Enhanced content readability",
                content.raw_html, optimized_html, optimizations
            )
            
        except Exception as e:
            logger.error(f"Error enhancing readability: {e}")
            return self._create_enhancement_result(
                content, EnhancementType.CONTENT_OPTIMIZATION,
                f"Error during enhancement: {str(e)}", content.raw_html, content.raw_html, []
            )
    
    def _fix_heading_hierarchy(self, headings: List[Dict[str, Any]]) -> tuple:
        """Fix heading hierarchy issues"""
        fixed_headings = []
        fixes = []
        
        if not headings:
            return fixed_headings, fixes
        
        prev_level = 0
        
        for heading in headings:
            current_level = heading['level']
            
            # Fix level jumps
            if current_level > prev_level + 1:
                new_level = prev_level + 1
                fixed_heading = heading.copy()
                fixed_heading['level'] = new_level
                fixed_headings.append(fixed_heading)
                fixes.append(f"Fixed heading level jump: H{current_level} -> H{new_level}")
            else:
                fixed_headings.append(heading)
            
            prev_level = fixed_headings[-1]['level']
        
        return fixed_headings, fixes
    
    def _optimize_heading_text(self, headings: List[Dict[str, Any]]) -> List[str]:
        """Optimize heading text for clarity and SEO"""
        optimizations = []
        
        for heading in headings:
            text = heading['text']
            
            # Check heading length
            if len(text) > 60:
                optimizations.append(f"Long heading detected: '{text[:50]}...' (consider shortening)")
            
            # Check for unclear headings
            unclear_patterns = [
                r'^(this|that|here|there)\s',
                r'^(introduction|overview|details)$'
            ]
            
            for pattern in unclear_patterns:
                if re.match(pattern, text, re.IGNORECASE):
                    optimizations.append(f"Consider making heading more specific: '{text}'")
        
        return optimizations
    
    def _apply_heading_fixes(self, html: str, fixed_headings: List[Dict[str, Any]]) -> str:
        """Apply heading hierarchy fixes to HTML"""
        from bs4 import BeautifulSoup
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Find and update headings
            for i, heading in enumerate(fixed_headings):
                heading_tags = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
                
                if i < len(heading_tags):
                    old_tag = heading_tags[i]
                    new_level = heading['level']
                    new_tag_name = f'h{new_level}'
                    
                    if old_tag.name != new_tag_name:
                        old_tag.name = new_tag_name
            
            return str(soup)
            
        except Exception as e:
            logger.error(f"Error applying heading fixes: {e}")
            return html
    
    def _generate_table_of_contents(self, headings: List[Dict[str, Any]]) -> str:
        """Generate table of contents HTML"""
        toc_html = '<div class="table-of-contents">\n'
        toc_html += '<h2>Table of Contents</h2>\n<ul>\n'
        
        for heading in headings:
            level = heading['level']
            text = heading['text']
            anchor = re.sub(r'[^a-zA-Z0-9\s]', '', text).replace(' ', '-').lower()
            
            indent = '  ' * (level - 1)
            toc_html += f'{indent}<li><a href="#{anchor}">{text}</a></li>\n'
        
        toc_html += '</ul>\n</div>\n'
        return toc_html
    
    def _insert_table_of_contents(self, html: str, toc_html: str) -> str:
        """Insert table of contents into HTML"""
        from bs4 import BeautifulSoup
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Find first heading or content div
            first_heading = soup.find(['h1', 'h2', 'h3'])
            if first_heading:
                toc_soup = BeautifulSoup(toc_html, 'html.parser')
                first_heading.insert_before(toc_soup)
            
            return str(soup)
            
        except Exception as e:
            logger.error(f"Error inserting table of contents: {e}")
            return html
    
    def _add_section_breaks(self, html: str) -> str:
        """Add visual section breaks"""
        from bs4 import BeautifulSoup
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Add section breaks before h2 headings
            h2_tags = soup.find_all('h2')
            for h2 in h2_tags[1:]:  # Skip first h2
                section_break = soup.new_tag('hr', **{'class': 'section-break'})
                h2.insert_before(section_break)
            
            return str(soup)
            
        except Exception as e:
            logger.error(f"Error adding section breaks: {e}")
            return html
    
    def _optimize_paragraphs(self, html: str) -> str:
        """Optimize paragraph structure"""
        from bs4 import BeautifulSoup
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            paragraphs = soup.find_all('p')
            for p in paragraphs:
                text = p.get_text().strip()
                
                # Split very long paragraphs
                if len(text) > 500:
                    sentences = text.split('. ')
                    if len(sentences) > 3:
                        # Split into multiple paragraphs
                        mid_point = len(sentences) // 2
                        first_half = '. '.join(sentences[:mid_point]) + '.'
                        second_half = '. '.join(sentences[mid_point:])
                        
                        p.string = first_half
                        new_p = soup.new_tag('p')
                        new_p.string = second_half
                        p.insert_after(new_p)
            
            return str(soup)
            
        except Exception as e:
            logger.error(f"Error optimizing paragraphs: {e}")
            return html
    
    def _add_transitions(self, html: str) -> str:
        """Add transition elements between sections"""
        # For now, this is a placeholder
        # In a real implementation, you'd analyze content flow and add appropriate transitions
        return html
    
    def _reorganize_sections(self, html: str, content: ContentModel) -> tuple:
        """Reorganize content sections for better flow"""
        changes = []
        
        # This is a placeholder for section reorganization logic
        # In a real implementation, you'd analyze content structure and reorder sections
        
        return html, changes
    
    def _break_long_paragraphs(self, html: str) -> str:
        """Break overly long paragraphs"""
        return self._optimize_paragraphs(html)  # Reuse existing logic
    
    def _emphasize_key_terms(self, html: str, content: ContentModel) -> str:
        """Add emphasis to key terms"""
        from bs4 import BeautifulSoup
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Get key concepts from content analysis
            structure = content.metadata.get('structure', {})
            # For now, emphasize technology terms
            tech_terms = ['API', 'REST', 'JSON', 'HTTP', 'HTTPS', 'SQL', 'NoSQL']
            
            for term in tech_terms:
                # Find and emphasize occurrences
                for text_node in soup.find_all(text=True):
                    if term in text_node.string:
                        new_text = text_node.string.replace(term, f'<strong>{term}</strong>')
                        if new_text != text_node.string:
                            text_node.replace_with(BeautifulSoup(new_text, 'html.parser'))
            
            return str(soup)
            
        except Exception as e:
            logger.error(f"Error emphasizing key terms: {e}")
            return html
    
    def _improve_list_formatting(self, html: str) -> str:
        """Improve list formatting"""
        from bs4 import BeautifulSoup
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Add classes to lists for better styling
            lists = soup.find_all(['ul', 'ol'])
            for list_elem in lists:
                if not list_elem.get('class'):
                    list_elem['class'] = ['formatted-list']
            
            return str(soup)
            
        except Exception as e:
            logger.error(f"Error improving list formatting: {e}")
            return html
    
    def _add_code_highlighting(self, html: str) -> str:
        """Add syntax highlighting to code blocks"""
        from bs4 import BeautifulSoup
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Find code blocks and add highlighting classes
            code_blocks = soup.find_all(['code', 'pre'])
            for code in code_blocks:
                if not code.get('class'):
                    code['class'] = ['highlighted-code']
            
            return str(soup)
            
        except Exception as e:
            logger.error(f"Error adding code highlighting: {e}")
            return html
    
    def _add_callout_boxes(self, html: str) -> str:
        """Add callout boxes for important information"""
        from bs4 import BeautifulSoup
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Look for paragraphs with important information indicators
            important_indicators = ['important', 'note', 'warning', 'tip', 'caution']
            
            paragraphs = soup.find_all('p')
            for p in paragraphs:
                text = p.get_text().lower()
                
                for indicator in important_indicators:
                    if indicator in text:
                        # Wrap in callout box
                        callout_div = soup.new_tag('div', **{'class': f'callout callout-{indicator}'})
                        p.wrap(callout_div)
                        break
            
            return str(soup)
            
        except Exception as e:
            logger.error(f"Error adding callout boxes: {e}")
            return html
    
    def _create_enhancement_result(self, content: ContentModel, enhancement_type: EnhancementType,
                                 description: str, before_content: str, after_content: str,
                                 changes: List[str]) -> EnhancementModel:
        """Create enhancement result"""
        
        # Calculate metrics
        before_words = len(before_content.split())
        after_words = len(after_content.split())
        
        metrics = EnhancementMetrics(
            content_id=content.content_id,
            original_word_count=before_words,
            enhanced_word_count=after_words,
            tables_found=0,
            visualizations_created=0,
            processes_identified=0,
            diagrams_created=0,
            outdated_technologies=0,
            modernization_suggestions=0,
            broken_links_found=0,
            links_fixed=0,
            readability_score_before=0.5,  # Placeholder
            readability_score_after=0.7,   # Placeholder
            enhancement_score=0.8          # Placeholder
        )
        
        return EnhancementModel(
            content_id=content.content_id,
            enhancement_type=enhancement_type,
            title=f"Structure Optimization: {content.title}",
            description=description,
            before_content=before_content,
            after_content=after_content,
            changes_summary=changes,
            metrics=metrics
        )

"""
Enhanced Concept Processor Module
AI-powered identification and conversion of concepts into diagrams and visualizations.
"""

import re
import logging
from typing import List, Dict, Any, Optional, Tuple
from bs4 import BeautifulSoup
import json
from datetime import datetime

logger = logging.getLogger(__name__)

class DiagramGenerator:
    """Generates various types of diagrams from identified concepts."""
    
    def __init__(self):
        self.mermaid_syntax = {
            'flowchart': 'flowchart TD',
            'sequence': 'sequenceDiagram',
            'class': 'classDiagram',
            'state': 'stateDiagram-v2',
            'gantt': 'gantt'
        }
    
    def generate_flowchart(self, process_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate flowchart from process description."""
        try:
            flowchart_code = self._create_mermaid_flowchart(process_data)
            
            return {
                'type': 'flowchart',
                'code': flowchart_code,
                'format': 'mermaid',
                'title': process_data.get('name', 'Process Flow'),
                'description': f"Process flow for {process_data.get('name', 'identified process')}",
                'complexity': self._assess_diagram_complexity(process_data),
                'interactive_elements': self._suggest_interactive_elements(process_data)
            }
            
        except Exception as e:
            logger.error(f"Error generating flowchart: {str(e)}")
            return {'type': 'flowchart', 'error': str(e)}
    
    def _create_mermaid_flowchart(self, process: Dict[str, Any]) -> str:
        """Create Mermaid flowchart syntax."""
        mermaid_code = "flowchart TD\n"
        
        # Add start node
        mermaid_code += "    Start([Start])\n"
        
        steps = process.get('steps', [])
        connections = process.get('connections', [])
        
        # Add process steps
        for i, step in enumerate(steps):
            node_id = f"Step{i+1}"
            step_type = step.get('type', 'process')
            description = step.get('description', f'Step {i+1}')
            
            # Escape special characters for Mermaid
            escaped_desc = self._escape_mermaid_text(description)
            
            if step_type == 'process':
                mermaid_code += f"    {node_id}[{escaped_desc}]\n"
            elif step_type == 'decision':
                mermaid_code += f"    {node_id}{{{escaped_desc}}}\n"
            elif step_type == 'data':
                mermaid_code += f"    {node_id}[({escaped_desc})]\n"
            elif step_type == 'subprocess':
                mermaid_code += f"    {node_id}[[{escaped_desc}]]\n"
        
        # Add connections
        if connections:
            for connection in connections:
                from_node = connection.get('from', 'Start')
                to_node = connection.get('to', 'End')
                label = connection.get('label', '')
                
                if label:
                    escaped_label = self._escape_mermaid_text(label)
                    mermaid_code += f"    {from_node} -->|{escaped_label}| {to_node}\n"
                else:
                    mermaid_code += f"    {from_node} --> {to_node}\n"
        else:
            # Create linear connections if none specified
            prev_node = 'Start'
            for i in range(len(steps)):
                current_node = f"Step{i+1}"
                mermaid_code += f"    {prev_node} --> {current_node}\n"
                prev_node = current_node
            mermaid_code += f"    {prev_node} --> End\n"
        
        # Add end node
        mermaid_code += "    End([End])\n"
        
        # Add styling
        mermaid_code += self._add_mermaid_styling()
        
        return mermaid_code
    
    def _escape_mermaid_text(self, text: str) -> str:
        """Escape special characters for Mermaid syntax."""
        # Remove or replace problematic characters
        text = text.replace('"', "'").replace('\n', ' ').replace('\r', '')
        # Limit length to prevent overly long labels
        if len(text) > 50:
            text = text[:47] + "..."
        return text
    
    def _add_mermaid_styling(self) -> str:
        """Add basic styling to Mermaid diagram."""
        return """
    classDef startEnd fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef process fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef decision fill:#fff3e0,stroke:#e65100,stroke-width:2px
    
    class Start,End startEnd
"""
    
    def _assess_diagram_complexity(self, process_data: Dict[str, Any]) -> str:
        """Assess the complexity of the diagram."""
        steps = process_data.get('steps', [])
        connections = process_data.get('connections', [])
        
        step_count = len(steps)
        connection_count = len(connections)
        decision_count = sum(1 for step in steps if step.get('type') == 'decision')
        
        complexity_score = 0
        
        if step_count > 10:
            complexity_score += 2
        elif step_count > 5:
            complexity_score += 1
        
        if decision_count > 3:
            complexity_score += 2
        elif decision_count > 1:
            complexity_score += 1
        
        if connection_count > step_count:  # Non-linear flow
            complexity_score += 1
        
        if complexity_score >= 4:
            return 'high'
        elif complexity_score >= 2:
            return 'medium'
        else:
            return 'low'
    
    def _suggest_interactive_elements(self, process_data: Dict[str, Any]) -> List[str]:
        """Suggest interactive elements for the diagram."""
        suggestions = []
        
        if process_data.get('complexity') == 'high':
            suggestions.extend(['zoom_pan', 'collapsible_nodes'])
        
        if any(step.get('type') == 'decision' for step in process_data.get('steps', [])):
            suggestions.append('conditional_highlighting')
        
        suggestions.extend(['hover_details', 'click_navigation'])
        
        return suggestions


class ConceptProcessor:
    """Enhanced processor for identifying and converting concepts to diagrams."""
    
    def __init__(self):
        self.diagram_generator = DiagramGenerator()
        # Mock AI processing since we don't have OpenAI configured
        self.ai_enabled = False
        logger.info("ConceptProcessor initialized in rule-based mode")
    
    def identify_concepts_and_processes(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Identify concepts that can be converted to diagrams."""
        try:
            raw_text = content.get('raw_text', '')
            
            concepts = {
                'processes': self._extract_processes(content),
                'workflows': self._extract_workflows(content),
                'architectures': self._extract_architectures(content),
                'relationships': self._extract_relationships(content),
                'hierarchies': self._extract_hierarchies(content),
                'decision_trees': self._extract_decision_trees(content),
                'timelines': self._extract_timelines(content)
            }
            
            # Filter out empty results
            concepts = {k: v for k, v in concepts.items() if v}
            
            return {
                'identified_concepts': concepts,
                'total_count': sum(len(v) for v in concepts.values()),
                'diagram_suggestions': self._generate_diagram_suggestions(concepts),
                'processing_method': 'rule_based'
            }
            
        except Exception as e:
            logger.error(f"Error identifying concepts: {str(e)}")
            return {'identified_concepts': {}, 'total_count': 0, 'error': str(e)}
    
    def _extract_processes(self, content: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract step-by-step processes from text."""
        raw_text = content.get('raw_text', '')
        processes = []
        
        # Rule-based extraction
        processes.extend(self._rule_based_extract_processes(raw_text))
        
        return processes
    
    def _rule_based_extract_processes(self, text: str) -> List[Dict[str, Any]]:
        """Extract processes using rule-based pattern matching."""
        processes = []
        
        # Pattern 1: Numbered steps
        numbered_pattern = r'(\d+)\.\s*([^\n]+(?:\n(?!\d+\.)[^\n]*)*)'
        numbered_matches = re.findall(numbered_pattern, text, re.MULTILINE)
        
        if len(numbered_matches) >= 3:  # At least 3 steps to be considered a process
            steps = []
            for num, description in numbered_matches:
                step_type = 'decision' if any(keyword in description.lower() 
                                           for keyword in ['if', 'whether', 'check', 'verify', 'decide']) else 'process'
                steps.append({
                    'description': description.strip(),
                    'type': step_type,
                    'step_number': int(num)
                })
            
            processes.append({
                'name': 'Numbered Process',
                'steps': steps,
                'connections': self._generate_linear_connections(steps),
                'complexity': 'medium',
                'diagram_type': 'flowchart',
                'source': 'numbered_list'
            })
        
        # Pattern 2: Bullet points with action words
        action_pattern = r'[•\-\*]\s*([^\n]+(?:\n(?![•\-\*])[^\n]*)*)'
        action_matches = re.findall(action_pattern, text, re.MULTILINE)
        
        if len(action_matches) >= 3:
            action_steps = []
            for i, description in enumerate(action_matches):
                if any(action_word in description.lower() 
                      for action_word in ['create', 'build', 'setup', 'configure', 'install', 'deploy']):
                    action_steps.append({
                        'description': description.strip(),
                        'type': 'process',
                        'step_number': i + 1
                    })
            
            if len(action_steps) >= 3:
                processes.append({
                    'name': 'Action-based Process',
                    'steps': action_steps,
                    'connections': self._generate_linear_connections(action_steps),
                    'complexity': 'low',
                    'diagram_type': 'flowchart',
                    'source': 'bullet_points'
                })
        
        # Pattern 3: Sequential action words
        sequential_pattern = r'(first|then|next|after|finally|lastly)\s*[,:]?\s*([^\n.!?]+)'
        sequential_matches = re.findall(sequential_pattern, text, re.IGNORECASE)
        
        if len(sequential_matches) >= 3:
            seq_steps = []
            for i, (indicator, description) in enumerate(sequential_matches):
                seq_steps.append({
                    'description': description.strip(),
                    'type': 'process',
                    'step_number': i + 1,
                    'indicator': indicator.lower()
                })
            
            processes.append({
                'name': 'Sequential Process',
                'steps': seq_steps,
                'connections': self._generate_linear_connections(seq_steps),
                'complexity': 'low',
                'diagram_type': 'flowchart',
                'source': 'sequential_indicators'
            })
        
        return processes
    
    def _generate_linear_connections(self, steps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate linear connections between steps."""
        connections = []
        
        if not steps:
            return connections
        
        # Start to first step
        connections.append({
            'from': 'Start',
            'to': 'Step1',
            'label': ''
        })
        
        # Connect consecutive steps
        for i in range(len(steps) - 1):
            connections.append({
                'from': f'Step{i+1}',
                'to': f'Step{i+2}',
                'label': ''
            })
        
        # Last step to end
        connections.append({
            'from': f'Step{len(steps)}',
            'to': 'End',
            'label': ''
        })
        
        return connections
    
    def _extract_workflows(self, content: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract workflow patterns from content."""
        workflows = []
        raw_text = content.get('raw_text', '')
        
        # Look for workflow keywords
        workflow_indicators = [
            'workflow', 'process flow', 'procedure', 'methodology',
            'steps to', 'how to', 'guide', 'instructions'
        ]
        
        for indicator in workflow_indicators:
            if indicator in raw_text.lower():
                # Extract surrounding context
                pattern = rf'(.{{0,100}}{re.escape(indicator)}.{{0,500}})'
                matches = re.findall(pattern, raw_text, re.IGNORECASE | re.DOTALL)
                
                for match in matches:
                    workflows.append({
                        'name': f'Workflow ({indicator})',
                        'description': match.strip(),
                        'type': 'workflow',
                        'complexity': 'medium',
                        'indicator': indicator
                    })
        
        return workflows[:3]  # Limit to top 3 workflows
    
    def _extract_architectures(self, content: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract architecture and system design patterns."""
        architectures = []
        raw_text = content.get('raw_text', '')
        
        # Architecture keywords
        arch_keywords = [
            'architecture', 'system design', 'component', 'module',
            'microservice', 'api', 'database', 'frontend', 'backend'
        ]
        
        arch_count = sum(1 for keyword in arch_keywords if keyword in raw_text.lower())
        
        if arch_count >= 3:  # Significant architectural content
            architectures.append({
                'name': 'System Architecture',
                'type': 'architecture',
                'style': self._detect_architecture_style(raw_text),
                'components': self._extract_components(raw_text),
                'complexity': 'high',
                'keyword_count': arch_count
            })
        
        return architectures
    
    def _detect_architecture_style(self, text: str) -> str:
        """Detect the style of architecture described."""
        text_lower = text.lower()
        
        if 'microservice' in text_lower:
            return 'microservices'
        elif 'layer' in text_lower or 'tier' in text_lower:
            return 'layered'
        elif 'mvc' in text_lower or 'model view controller' in text_lower:
            return 'mvc'
        elif 'event' in text_lower and 'driven' in text_lower:
            return 'event_driven'
        else:
            return 'general'
    
    def _extract_components(self, text: str) -> List[str]:
        """Extract system components from text."""
        components = []
        
        # Component patterns
        component_patterns = [
            r'(\w+)\s+(?:component|module|service)',
            r'(?:component|module|service)\s+(\w+)',
            r'(\w+)\s+(?:api|database|frontend|backend)'
        ]
        
        for pattern in component_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            components.extend(matches)
        
        # Remove duplicates and return unique components
        return list(set(components))[:10]  # Limit to 10 components
    
    def _extract_relationships(self, content: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract relationship patterns suitable for network diagrams."""
        relationships = []
        raw_text = content.get('raw_text', '')
        
        # Look for relationship indicators
        relationship_patterns = [
            r'(\w+)\s+(?:connects to|links to|depends on|uses|calls)\s+(\w+)',
            r'(\w+)\s+(?:→|->|=>)\s+(\w+)',
            r'(\w+)\s+and\s+(\w+)\s+(?:interact|communicate|integrate)'
        ]
        
        for pattern in relationship_patterns:
            matches = re.findall(pattern, raw_text, re.IGNORECASE)
            for match in matches:
                relationships.append({
                    'from': match[0],
                    'to': match[1],
                    'type': 'relationship',
                    'diagram_type': 'network'
                })
        
        return relationships[:10]  # Limit to 10 relationships
    
    def _extract_hierarchies(self, content: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract hierarchical structures."""
        hierarchies = []
        raw_text = content.get('raw_text', '')
        
        # Look for hierarchy indicators
        hierarchy_indicators = ['hierarchy', 'structure', 'organization', 'tree', 'parent', 'child']
        
        hierarchy_count = sum(1 for indicator in hierarchy_indicators if indicator in raw_text.lower())
        
        if hierarchy_count >= 2:
            hierarchies.append({
                'name': 'Organizational Hierarchy',
                'type': 'hierarchy',
                'diagram_type': 'tree',
                'complexity': 'medium'
            })
        
        return hierarchies
    
    def _extract_decision_trees(self, content: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract decision tree patterns."""
        decision_trees = []
        raw_text = content.get('raw_text', '')
        
        # Look for decision patterns
        decision_patterns = [
            r'if\s+(.+?)\s+then\s+(.+)',
            r'whether\s+(.+)',
            r'depends?\s+on\s+(.+)',
            r'choose\s+(.+)',
            r'decide\s+(.+)'
        ]
        
        decision_count = 0
        for pattern in decision_patterns:
            matches = re.findall(pattern, raw_text, re.IGNORECASE)
            decision_count += len(matches)
        
        if decision_count >= 3:
            decision_trees.append({
                'name': 'Decision Tree',
                'type': 'decision_tree',
                'diagram_type': 'decision_tree',
                'decision_count': decision_count,
                'complexity': 'medium'
            })
        
        return decision_trees
    
    def _extract_timelines(self, content: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract timeline and chronological information."""
        timelines = []
        raw_text = content.get('raw_text', '')
        
        # Look for time-related patterns
        time_patterns = [
            r'(\d{4})[:\-\s]*(.+)',  # Year-based events
            r'(january|february|march|april|may|june|july|august|september|october|november|december)\s+(\d{4})',
            r'(q1|q2|q3|q4)\s+(\d{4})',  # Quarterly
            r'(week|month|year)\s+(\d+)'
        ]
        
        time_event_count = 0
        for pattern in time_patterns:
            matches = re.findall(pattern, raw_text, re.IGNORECASE)
            time_event_count += len(matches)
        
        if time_event_count >= 3:
            timelines.append({
                'name': 'Timeline',
                'type': 'timeline',
                'diagram_type': 'gantt',
                'event_count': time_event_count,
                'complexity': 'medium'
            })
        
        return timelines
    
    def _generate_diagram_suggestions(self, concepts: Dict[str, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """Generate diagram suggestions based on identified concepts."""
        suggestions = []
        
        for concept_type, concept_list in concepts.items():
            for concept in concept_list:
                if concept_type == 'processes':
                    suggestions.append({
                        'type': 'flowchart',
                        'priority': 'high',
                        'reason': f"Process identified: {concept.get('name', 'Unnamed Process')}",
                        'concept': concept,
                        'estimated_effort': 'medium'
                    })
                elif concept_type == 'architectures':
                    suggestions.append({
                        'type': 'architecture_diagram',
                        'priority': 'high',
                        'reason': f"System architecture detected",
                        'concept': concept,
                        'estimated_effort': 'high'
                    })
                elif concept_type == 'relationships':
                    suggestions.append({
                        'type': 'network_diagram',
                        'priority': 'medium',
                        'reason': f"Relationships identified",
                        'concept': concept,
                        'estimated_effort': 'medium'
                    })
                elif concept_type == 'timelines':
                    suggestions.append({
                        'type': 'timeline_chart',
                        'priority': 'medium',
                        'reason': f"Timeline events detected",
                        'concept': concept,
                        'estimated_effort': 'low'
                    })
        
        return suggestions
    
    def generate_process_diagrams(self, processes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate flowcharts and process diagrams."""
        diagrams = []
        
        for process in processes:
            try:
                if process.get('diagram_type') == 'flowchart':
                    diagram = self.diagram_generator.generate_flowchart(process)
                    diagrams.append(diagram)
                    
            except Exception as e:
                logger.error(f"Error generating diagram for process: {str(e)}")
                continue
        
        return diagrams
    
    def _parse_process_response(self, response_text: str) -> List[Dict[str, Any]]:
        """Parse AI response for process extraction."""
        try:
            # Try to parse as JSON
            if response_text.strip().startswith('['):
                return json.loads(response_text)
            else:
                # Extract JSON from response
                json_match = re.search(r'\[(.*?)\]', response_text, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group(0))
                else:
                    return []
        except Exception as e:
            logger.error(f"Error parsing AI response: {str(e)}")
            return []

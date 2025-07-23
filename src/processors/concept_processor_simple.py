"""
Simple Concept Processor for Phase 2 Testing
"""
import logging
import re
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class ConceptProcessor:
    """Simple concept processor for testing."""
    
    def __init__(self):
        self.concept_patterns = {
            'process': [
                r'\b(?:process|procedure|workflow|steps?|method)\b',
                r'\b(?:deploy|build|test|validate|approve)\b'
            ],
            'technology': [
                r'\b(?:java|python|javascript|sql|database|server)\b',
                r'\b(?:api|rest|soap|http|https|json|xml)\b'
            ],
            'business': [
                r'\b(?:user|customer|client|business|requirement)\b',
                r'\b(?:revenue|cost|budget|profit|investment)\b'
            ]
        }
    
    async def identify_concepts(self, content: str) -> List[Dict[str, Any]]:
        """Identify concepts in the content."""
        try:
            concepts = []
            
            # Simple pattern matching for concept identification
            for concept_type, patterns in self.concept_patterns.items():
                for pattern in patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    for match in matches:
                        concepts.append({
                            'name': match,
                            'type': concept_type,
                            'confidence': 0.8
                        })
            
            # Remove duplicates
            unique_concepts = []
            seen = set()
            for concept in concepts:
                key = (concept['name'].lower(), concept['type'])
                if key not in seen:
                    seen.add(key)
                    unique_concepts.append(concept)
            
            return unique_concepts[:20]  # Limit to 20 concepts
            
        except Exception as e:
            logger.error(f"Error identifying concepts: {str(e)}")
            return []
    
    async def generate_diagram(self, concept: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Generate a simple diagram for the concept."""
        try:
            concept_type = concept.get('type', 'unknown')
            concept_name = concept.get('name', 'Unknown')
            
            if concept_type == 'process':
                return {
                    'type': 'flowchart',
                    'title': f'{concept_name} Process',
                    'mermaid': f'''
                    flowchart TD
                        A[Start {concept_name}] --> B[Process Step 1]
                        B --> C[Process Step 2]
                        C --> D[Complete {concept_name}]
                    ''',
                    'description': f'Process diagram for {concept_name}'
                }
            elif concept_type == 'technology':
                return {
                    'type': 'component',
                    'title': f'{concept_name} Architecture',
                    'mermaid': f'''
                    graph LR
                        A[Client] --> B[{concept_name}]
                        B --> C[Database]
                    ''',
                    'description': f'Component diagram for {concept_name}'
                }
            else:
                return {
                    'type': 'simple',
                    'title': f'{concept_name} Overview',
                    'mermaid': f'''
                    graph TB
                        A[{concept_name}]
                    ''',
                    'description': f'Simple diagram for {concept_name}'
                }
                
        except Exception as e:
            logger.error(f"Error generating diagram: {str(e)}")
            return None

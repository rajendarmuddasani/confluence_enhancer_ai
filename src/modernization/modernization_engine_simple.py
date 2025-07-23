"""
Simple Modernization Engine for Phase 2 Testing
"""
import logging
import re
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class ModernizationEngine:
    """Simple modernization engine for testing."""
    
    def __init__(self):
        self.technology_database = {
            'java 8': {'status': 'outdated', 'modern_alternative': 'Java 17+', 'urgency': 'medium'},
            'jsf': {'status': 'outdated', 'modern_alternative': 'React/Angular', 'urgency': 'high'},
            'oracle 11g': {'status': 'outdated', 'modern_alternative': 'PostgreSQL/MySQL 8+', 'urgency': 'medium'},
            'tomcat 7': {'status': 'outdated', 'modern_alternative': 'Tomcat 10+', 'urgency': 'high'},
            'struts': {'status': 'outdated', 'modern_alternative': 'Spring Boot', 'urgency': 'critical'},
            'jquery 1.8': {'status': 'outdated', 'modern_alternative': 'Modern JS/React', 'urgency': 'high'},
        }
    
    async def detect_technologies(self, content: str) -> List[Dict[str, Any]]:
        """Detect technologies mentioned in the content."""
        try:
            detected = []
            content_lower = content.lower()
            
            for tech, info in self.technology_database.items():
                if tech in content_lower:
                    detected.append({
                        'technology': tech,
                        'status': info['status'],
                        'modern_alternative': info['modern_alternative'],
                        'urgency': info['urgency'],
                        'category': 'framework' if any(x in tech for x in ['jsf', 'struts', 'spring']) else 'runtime'
                    })
            
            return detected
            
        except Exception as e:
            logger.error(f"Error detecting technologies: {str(e)}")
            return []
    
    async def analyze_modernization_needs(self, technologies: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze modernization needs based on detected technologies."""
        try:
            outdated_techs = [t for t in technologies if t.get('status') == 'outdated']
            
            analysis = {
                'total_technologies': len(technologies),
                'outdated_count': len(outdated_techs),
                'critical_updates': len([t for t in outdated_techs if t.get('urgency') == 'critical']),
                'high_priority': len([t for t in outdated_techs if t.get('urgency') == 'high']),
                'suggestions': []
            }
            
            for tech in outdated_techs:
                analysis['suggestions'].append({
                    'current': tech['technology'],
                    'recommended': tech['modern_alternative'],
                    'priority': tech['urgency'],
                    'reason': f'{tech["technology"]} is outdated and should be updated'
                })
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing modernization needs: {str(e)}")
            return {'error': str(e)}
    
    async def generate_implementation_roadmap(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate implementation roadmap."""
        try:
            suggestions = analysis.get('suggestions', [])
            
            # Group by priority
            critical = [s for s in suggestions if s.get('priority') == 'critical']
            high = [s for s in suggestions if s.get('priority') == 'high']
            medium = [s for s in suggestions if s.get('priority') == 'medium']
            
            phases = []
            
            if critical:
                phases.append({
                    'phase': 'Phase 1: Critical Updates',
                    'priority': 'critical',
                    'duration': '3-6 months',
                    'technologies': [s['current'] for s in critical]
                })
            
            if high:
                phases.append({
                    'phase': 'Phase 2: High Priority Updates',
                    'priority': 'high',
                    'duration': '6-12 months',
                    'technologies': [s['current'] for s in high]
                })
            
            if medium:
                phases.append({
                    'phase': 'Phase 3: Medium Priority Updates',
                    'priority': 'medium',
                    'duration': '12-18 months',
                    'technologies': [s['current'] for s in medium]
                })
            
            return {
                'total_timeline': '18-24 months',
                'total_effort': 'High',
                'phases': phases,
                'estimated_cost': 'High',
                'risk_level': 'Medium'
            }
            
        except Exception as e:
            logger.error(f"Error generating roadmap: {str(e)}")
            return {'error': str(e)}

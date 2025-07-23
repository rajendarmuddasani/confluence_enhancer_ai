"""
Enhancement engine for content improvement
"""
import logging
from typing import Dict, Any, List, Optional
import openai
from dataclasses import dataclass
from datetime import datetime

from ..models.content_model import ContentModel
from ..models.enhancement_model import EnhancementModel, EnhancementType, EnhancementMetrics


logger = logging.getLogger(__name__)


@dataclass
class Enhancement:
    """Single enhancement suggestion"""
    id: str
    type: EnhancementType
    title: str
    description: str
    priority: str  # 'high', 'medium', 'low'
    category: str
    original_content: str
    enhanced_content: str
    confidence: float
    metrics: EnhancementMetrics
    issues: List[str]
    recommendations: List[str]


class EnhancementEngine:
    """Main enhancement engine for content improvement"""
    
    def __init__(self):
        self.openai_client = openai.OpenAI()
        self.enhancement_types = {
            'readability': self._enhance_readability,
            'structure': self._enhance_structure,
            'clarity': self._enhance_clarity,
            'consistency': self._enhance_consistency,
            'completeness': self._enhance_completeness
        }
    
    def generate_enhancements(self, content: ContentModel) -> List[Enhancement]:
        """Generate comprehensive content enhancements"""
        try:
            logger.info(f"Generating enhancements for: {content.title}")
            
            enhancements = []
            
            # Analyze content for improvement opportunities
            analysis = self._analyze_content_quality(content)
            
            # Generate enhancements for each identified issue
            for issue_type, issues in analysis.items():
                for issue in issues:
                    enhancement = self._create_enhancement_for_issue(content, issue_type, issue)
                    if enhancement:
                        enhancements.append(enhancement)
            
            # Sort by priority and confidence
            enhancements.sort(key=lambda x: (x.priority == 'high', x.confidence), reverse=True)
            
            return enhancements
            
        except Exception as e:
            logger.error(f"Failed to generate enhancements: {e}")
            return []
    
    def _analyze_content_quality(self, content: ContentModel) -> Dict[str, List[Dict[str, Any]]]:
        """Analyze content quality and identify improvement opportunities"""
        
        prompt = f"""
        Analyze the following Confluence page content for quality issues and improvement opportunities:
        
        Title: {content.title}
        Content: {content.raw_text[:4000]}  # Limit for token constraints
        
        Please identify issues in these categories:
        1. Readability (complex sentences, passive voice, jargon)
        2. Structure (heading hierarchy, organization, flow)
        3. Clarity (ambiguous statements, unclear instructions)
        4. Consistency (formatting, terminology, style)
        5. Completeness (missing information, broken links, outdated content)
        
        For each issue found, provide:
        - Specific location in content
        - Description of the problem
        - Suggested improvement
        - Priority level (high/medium/low)
        - Confidence score (0-1)
        
        Return as JSON format.
        """
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            
            # Parse response and extract issues
            # For now, return mock data structure
            return {
                'readability': [
                    {
                        'description': 'Complex sentence structure detected',
                        'location': 'paragraph 2',
                        'suggestion': 'Break into shorter sentences',
                        'priority': 'medium',
                        'confidence': 0.8
                    }
                ],
                'structure': [
                    {
                        'description': 'Inconsistent heading hierarchy',
                        'location': 'section 3',
                        'suggestion': 'Restructure headings in logical order',
                        'priority': 'high',
                        'confidence': 0.9
                    }
                ],
                'clarity': [],
                'consistency': [],
                'completeness': []
            }
            
        except Exception as e:
            logger.error(f"Failed to analyze content quality: {e}")
            return {}
    
    def _create_enhancement_for_issue(self, content: ContentModel, issue_type: str, issue: Dict[str, Any]) -> Optional[Enhancement]:
        """Create enhancement suggestion for a specific issue"""
        
        try:
            # Generate enhanced content for the issue
            enhanced_content = self._generate_enhanced_content(content.raw_text, issue)
            
            if not enhanced_content:
                return None
            
            # Calculate metrics
            metrics = self._calculate_enhancement_metrics(
                content.raw_text, 
                enhanced_content,
                issue
            )
            
            enhancement = Enhancement(
                id=f"enh_{datetime.now().timestamp()}",
                type=EnhancementType.CONTENT_RESTRUCTURE,  # Map issue_type to enum
                title=f"Improve {issue_type}: {issue['description']}",
                description=issue['suggestion'],
                priority=issue['priority'],
                category=issue_type,
                original_content=self._extract_relevant_content(content.raw_text, issue),
                enhanced_content=enhanced_content,
                confidence=issue['confidence'],
                metrics=metrics,
                issues=[issue['description']],
                recommendations=[issue['suggestion']]
            )
            
            return enhancement
            
        except Exception as e:
            logger.error(f"Failed to create enhancement for issue: {e}")
            return None
    
    def _generate_enhanced_content(self, original_content: str, issue: Dict[str, Any]) -> str:
        """Generate enhanced content for a specific issue"""
        
        prompt = f"""
        Original content: {original_content[:2000]}
        
        Issue: {issue['description']}
        Location: {issue['location']}
        Suggested improvement: {issue['suggestion']}
        
        Please provide an improved version of the relevant content that addresses this issue.
        Focus on the specific problem area and provide a clear, improved alternative.
        """
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Failed to generate enhanced content: {e}")
            return ""
    
    def _extract_relevant_content(self, full_content: str, issue: Dict[str, Any]) -> str:
        """Extract the relevant content section for the issue"""
        # Simple implementation - in practice, would use NLP to locate exact content
        words = full_content.split()
        # Return a section around the issue location
        return ' '.join(words[:200])  # Return first 200 words as placeholder
    
    def _calculate_enhancement_metrics(self, original: str, enhanced: str, issue: Dict[str, Any]) -> EnhancementMetrics:
        """Calculate metrics for the enhancement"""
        
        # Simple metrics calculation
        original_length = len(original.split())
        enhanced_length = len(enhanced.split())
        
        readability_score = 75 + (issue['confidence'] * 20)  # Mock calculation
        improvement_percentage = issue['confidence'] * 100
        estimated_time = 5 + (len(enhanced.split()) // 50) * 2  # Mock time estimation
        
        return EnhancementMetrics(
            readability_score=readability_score,
            improvement_percentage=improvement_percentage,
            estimated_time_to_implement=estimated_time
        )
    
    def _enhance_readability(self, content: str) -> str:
        """Enhance content readability"""
        # Placeholder implementation
        return content
    
    def _enhance_structure(self, content: str) -> str:
        """Enhance content structure"""
        # Placeholder implementation
        return content
    
    def _enhance_clarity(self, content: str) -> str:
        """Enhance content clarity"""
        # Placeholder implementation
        return content
    
    def _enhance_consistency(self, content: str) -> str:
        """Enhance content consistency"""
        # Placeholder implementation
        return content
    
    def _enhance_completeness(self, content: str) -> str:
        """Enhance content completeness"""
        # Placeholder implementation
        return content
    
    def apply_enhancement(self, content: ContentModel, enhancement: Enhancement) -> EnhancementModel:
        """Apply an enhancement to content"""
        try:
            logger.info(f"Applying enhancement: {enhancement.title}")
            
            # Apply the enhancement to the content
            enhanced_html = content.raw_html.replace(
                enhancement.original_content,
                enhancement.enhanced_content
            )
            
            # Create enhancement model
            enhancement_model = EnhancementModel(
                enhancement_id=enhancement.id,
                content_id=content.content_id,
                enhancement_type=enhancement.type,
                title=enhancement.title,
                description=enhancement.description,
                original_content=enhancement.original_content,
                enhanced_content=enhancement.enhanced_content,
                metrics=enhancement.metrics,
                status="applied",
                confidence=enhancement.confidence,
                applied_at=datetime.now(),
                issues_resolved=[enhancement.issues],
                recommendations_followed=[enhancement.recommendations]
            )
            
            return enhancement_model
            
        except Exception as e:
            logger.error(f"Failed to apply enhancement: {e}")
            raise

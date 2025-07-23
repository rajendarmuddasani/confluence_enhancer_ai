"""
AI-powered content analysis engine
"""
import logging
from typing import Dict, Any, List, Optional
import openai
import anthropic
from sentence_transformers import SentenceTransformer
import numpy as np
import re

from ..models.content_model import ContentModel, AnalysisResult
from ..utils.config import settings
from ..utils.helpers import chunk_text, clean_text


logger = logging.getLogger(__name__)


class ContentAnalyzer:
    """AI-powered content analysis and understanding"""
    
    def __init__(self):
        # Initialize AI clients
        if settings.OPENAI_API_KEY:
            self.openai_client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        else:
            self.openai_client = None
            logger.warning("OpenAI API key not configured")
        
        if settings.ANTHROPIC_API_KEY:
            self.anthropic_client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        else:
            self.anthropic_client = None
            logger.warning("Anthropic API key not configured")
        
        # Initialize sentence transformer for embeddings
        try:
            self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
        except Exception as e:
            logger.error(f"Failed to load sentence transformer: {e}")
            self.sentence_model = None
    
    def analyze_content_structure(self, content: ContentModel) -> AnalysisResult:
        """Analyze content structure and organization"""
        try:
            logger.info(f"Analyzing content structure for: {content.title}")
            
            structure = content.metadata.get('structure', {})
            headings = structure.get('headings', [])
            
            # Analyze heading hierarchy
            hierarchy_analysis = self._analyze_heading_hierarchy(headings)
            
            # Analyze content flow
            flow_analysis = self._analyze_content_flow(content.raw_text)
            
            # Analyze readability
            readability_analysis = self._analyze_readability(content.raw_text)
            
            results = {
                'hierarchy': hierarchy_analysis,
                'flow': flow_analysis,
                'readability': readability_analysis,
                'word_count': len(content.raw_text.split()),
                'paragraph_count': len(content.raw_text.split('\n\n')),
                'heading_count': len(headings)
            }
            
            # Calculate confidence score based on analysis completeness
            confidence = 0.8 if all([hierarchy_analysis, flow_analysis, readability_analysis]) else 0.6
            
            return AnalysisResult(
                content_id=content.content_id,
                analysis_type="content_structure",
                results=results,
                confidence_score=confidence
            )
            
        except Exception as e:
            logger.error(f"Error analyzing content structure: {e}")
            return AnalysisResult(
                content_id=content.content_id,
                analysis_type="content_structure",
                results={},
                confidence_score=0.0
            )
    
    def analyze_content_quality(self, content: ContentModel) -> AnalysisResult:
        """Analyze content quality and suggest improvements"""
        try:
            logger.info(f"Analyzing content quality for: {content.title}")
            
            text = content.raw_text
            
            # Use AI to analyze content quality
            quality_analysis = self._ai_content_quality_analysis(text)
            
            # Analyze specific quality metrics
            quality_metrics = {
                'clarity_score': self._calculate_clarity_score(text),
                'completeness_score': self._calculate_completeness_score(content),
                'consistency_score': self._calculate_consistency_score(text),
                'accuracy_indicators': self._find_accuracy_indicators(text),
                'improvement_suggestions': quality_analysis.get('suggestions', [])
            }
            
            # Calculate overall quality score
            overall_score = (
                quality_metrics['clarity_score'] * 0.3 +
                quality_metrics['completeness_score'] * 0.3 +
                quality_metrics['consistency_score'] * 0.4
            )
            
            quality_metrics['overall_score'] = overall_score
            
            return AnalysisResult(
                content_id=content.content_id,
                analysis_type="content_quality",
                results=quality_metrics,
                confidence_score=0.85
            )
            
        except Exception as e:
            logger.error(f"Error analyzing content quality: {e}")
            return AnalysisResult(
                content_id=content.content_id,
                analysis_type="content_quality",
                results={},
                confidence_score=0.0
            )
    
    def extract_key_concepts(self, content: ContentModel) -> AnalysisResult:
        """Extract key concepts and topics using AI"""
        try:
            logger.info(f"Extracting key concepts from: {content.title}")
            
            text = content.raw_text
            
            # Use AI to extract concepts
            if self.openai_client:
                concepts = self._extract_concepts_with_ai(text)
            else:
                concepts = self._extract_concepts_with_rules(text)
            
            # Generate embeddings for semantic analysis
            embeddings = self._generate_content_embeddings(text)
            
            results = {
                'key_concepts': concepts.get('concepts', []),
                'topics': concepts.get('topics', []),
                'entities': concepts.get('entities', []),
                'technologies': concepts.get('technologies', []),
                'embeddings': embeddings.tolist() if embeddings is not None else []
            }
            
            return AnalysisResult(
                content_id=content.content_id,
                analysis_type="key_concepts",
                results=results,
                confidence_score=0.9 if self.openai_client else 0.7
            )
            
        except Exception as e:
            logger.error(f"Error extracting key concepts: {e}")
            return AnalysisResult(
                content_id=content.content_id,
                analysis_type="key_concepts",
                results={},
                confidence_score=0.0
            )
    
    def _analyze_heading_hierarchy(self, headings: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze heading hierarchy and structure"""
        if not headings:
            return {'issues': ['No headings found'], 'structure_score': 0.3}
        
        issues = []
        structure_score = 1.0
        
        # Check for proper hierarchy
        prev_level = 0
        for heading in headings:
            level = heading['level']
            if level > prev_level + 1:
                issues.append(f"Heading level jump: H{prev_level} to H{level}")
                structure_score -= 0.1
            prev_level = level
        
        # Check for heading length
        for heading in headings:
            text = heading['text']
            if len(text) > 60:
                issues.append(f"Long heading: '{text[:50]}...'")
                structure_score -= 0.05
        
        return {
            'issues': issues,
            'structure_score': max(0.0, structure_score),
            'heading_count': len(headings),
            'max_level': max(h['level'] for h in headings) if headings else 0
        }
    
    def _analyze_content_flow(self, text: str) -> Dict[str, Any]:
        """Analyze logical flow of content"""
        sentences = text.split('.')
        
        # Simple flow analysis
        transition_words = [
            'however', 'therefore', 'furthermore', 'additionally',
            'consequently', 'meanwhile', 'nevertheless', 'moreover'
        ]
        
        transition_count = 0
        for word in transition_words:
            transition_count += text.lower().count(word)
        
        flow_score = min(1.0, transition_count / max(1, len(sentences) / 10))
        
        return {
            'flow_score': flow_score,
            'transition_count': transition_count,
            'sentence_count': len(sentences)
        }
    
    def _analyze_readability(self, text: str) -> Dict[str, Any]:
        """Analyze text readability"""
        words = text.split()
        sentences = text.split('.')
        
        if not words or not sentences:
            return {'readability_score': 0.0}
        
        # Simple readability metrics
        avg_words_per_sentence = len(words) / len(sentences)
        avg_chars_per_word = sum(len(word) for word in words) / len(words)
        
        # Simple readability score (inverse of complexity)
        complexity = (avg_words_per_sentence / 15) + (avg_chars_per_word / 6)
        readability_score = max(0.0, 1.0 - complexity / 2)
        
        return {
            'readability_score': readability_score,
            'avg_words_per_sentence': avg_words_per_sentence,
            'avg_chars_per_word': avg_chars_per_word,
            'total_words': len(words),
            'total_sentences': len(sentences)
        }
    
    def _ai_content_quality_analysis(self, text: str) -> Dict[str, Any]:
        """Use AI to analyze content quality comprehensively"""
        try:
            if self.openai_client:
                response = self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "system",
                            "content": """You are a content quality expert. Analyze the provided text and provide:
1. Overall quality assessment (1-10 scale)
2. Specific areas for improvement
3. Suggestions for enhancement
4. Readability assessment
5. Structure recommendations

Respond in JSON format with clear, actionable insights."""
                        },
                        {
                            "role": "user",
                            "content": f"Analyze this content for quality:\n\n{text[:4000]}"  # Limit text length
                        }
                    ],
                    max_tokens=1000,
                    temperature=0.3
                )
                
                try:
                    import json
                    return json.loads(response.choices[0].message.content)
                except json.JSONDecodeError:
                    return {"suggestions": [response.choices[0].message.content]}
                    
            elif self.anthropic_client:
                response = self.anthropic_client.messages.create(
                    model="claude-3-sonnet-20240229",
                    max_tokens=1000,
                    messages=[
                        {
                            "role": "user",
                            "content": f"""As a content quality expert, analyze this text and provide:
1. Overall quality score (1-10)
2. Specific improvement areas
3. Enhancement suggestions
4. Readability assessment

Content to analyze:
{text[:4000]}

Provide response in JSON format."""
                        }
                    ]
                )
                
                try:
                    import json
                    return json.loads(response.content[0].text)
                except json.JSONDecodeError:
                    return {"suggestions": [response.content[0].text]}
            
            else:
                return self._fallback_quality_analysis(text)
                
        except Exception as e:
            logger.error(f"AI quality analysis failed: {e}")
            return self._fallback_quality_analysis(text)
    
    def _fallback_quality_analysis(self, text: str) -> Dict[str, Any]:
        """Fallback quality analysis without AI"""
        suggestions = []
        
        # Basic quality checks
        if len(text.split()) < 100:
            suggestions.append("Content appears too short - consider adding more detail")
        
        sentences = text.split('.')
        avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences) if sentences else 0
        
        if avg_sentence_length > 25:
            suggestions.append("Sentences are quite long - consider breaking them down for better readability")
        
        if text.count('\n') < len(text.split()) / 50:
            suggestions.append("Consider adding more paragraphs and line breaks for better structure")
        
        return {
            "overall_score": 6.0,
            "suggestions": suggestions,
            "readability_notes": f"Average sentence length: {avg_sentence_length:.1f} words"
        }
    
    def _extract_concepts_with_ai(self, text: str) -> Dict[str, Any]:
        """Extract key concepts using AI"""
        try:
            if self.openai_client:
                response = self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "system",
                            "content": """Extract key concepts, topics, and themes from the provided text. 
Return a JSON object with:
- concepts: list of main concepts/topics
- themes: overarching themes
- keywords: important keywords
- categories: content categories
- entities: named entities (people, places, technologies)"""
                        },
                        {
                            "role": "user",
                            "content": f"Extract key concepts from this content:\n\n{text[:3000]}"
                        }
                    ],
                    max_tokens=800,
                    temperature=0.2
                )
                
                try:
                    import json
                    return json.loads(response.choices[0].message.content)
                except json.JSONDecodeError:
                    # Fallback if JSON parsing fails
                    content = response.choices[0].message.content
                    return {"concepts": content.split('\n'), "raw_response": content}
                    
        except Exception as e:
            logger.error(f"AI concept extraction failed: {e}")
            return self._extract_concepts_with_rules(text)
    
    def _extract_concepts_with_rules(self, text: str) -> Dict[str, Any]:
        """Fallback rule-based concept extraction"""
        words = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
        
        # Simple frequency-based extraction
        word_freq = {}
        for word in words:
            if len(word) > 3:  # Ignore short words
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Get top concepts
        top_concepts = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return {
            "concepts": [concept[0] for concept in top_concepts],
            "keywords": list(word_freq.keys())[:20],
            "method": "rule_based_fallback"
        }
    
    def _generate_content_embeddings(self, text: str) -> Optional[List[float]]:
        """Generate semantic embeddings for content"""
        try:
            if self.sentence_model:
                # Split text into chunks if too long
                chunks = chunk_text(text, 500)
                embeddings = []
                
                for chunk in chunks:
                    embedding = self.sentence_model.encode(chunk)
                    embeddings.append(embedding)
                
                # Average embeddings for the full text
                if embeddings:
                    avg_embedding = np.mean(embeddings, axis=0)
                    return avg_embedding.tolist()
            
            return None
            
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            return None
    
    def _calculate_clarity_score(self, text: str) -> float:
        """Calculate content clarity score"""
        try:
            # Basic clarity metrics
            sentences = text.split('.')
            words = text.split()
            
            if not sentences or not words:
                return 0.0
            
            # Average sentence length
            avg_sentence_length = len(words) / len(sentences)
            sentence_score = max(0, 10 - (avg_sentence_length - 15) * 0.5)  # Optimal ~15 words
            
            # Vocabulary complexity
            complex_words = len([w for w in words if len(w) > 6])
            complexity_ratio = complex_words / len(words) if words else 0
            complexity_score = max(0, 10 - complexity_ratio * 20)
            
            # Readability indicators
            transition_words = ['however', 'therefore', 'furthermore', 'moreover', 'consequently']
            transition_count = sum(1 for word in transition_words if word in text.lower())
            transition_score = min(10, transition_count * 2)
            
            # Average the scores
            clarity_score = (sentence_score + complexity_score + transition_score) / 3
            return min(10.0, max(0.0, clarity_score))
            
        except Exception as e:
            logger.error(f"Error calculating clarity score: {e}")
            return 5.0  # Default score
    
    def _calculate_completeness_score(self, content: ContentModel) -> float:
        """Calculate content completeness score"""
        try:
            score = 5.0  # Base score
            
            # Check for essential elements
            structure = content.metadata.get('structure', {})
            
            # Has title
            if content.title and len(content.title.strip()) > 0:
                score += 1.0
            
            # Has headings
            headings = structure.get('headings', [])
            if len(headings) >= 2:
                score += 1.5
            elif len(headings) >= 1:
                score += 1.0
            
            # Has sufficient content
            word_count = len(content.raw_text.split())
            if word_count >= 500:
                score += 1.5
            elif word_count >= 200:
                score += 1.0
            elif word_count >= 100:
                score += 0.5
            
            # Has lists or structured content
            if structure.get('lists', 0) > 0:
                score += 0.5
            
            # Has tables or data
            if structure.get('tables', 0) > 0:
                score += 0.5
            
            # Has links or references
            if structure.get('links', 0) > 0:
                score += 0.5
            
            return min(10.0, max(0.0, score))
            
        except Exception as e:
            logger.error(f"Error calculating completeness score: {e}")
            return 5.0
    
    def _calculate_consistency_score(self, text: str) -> float:
        """Calculate content consistency score"""
        try:
            score = 5.0  # Base score
            
            # Check heading consistency
            headings = re.findall(r'^#+\s+(.+)$', text, re.MULTILINE)
            if len(headings) > 1:
                # Check if headings follow a pattern
                heading_styles = [len(h.split()) for h in headings]
                style_variance = np.var(heading_styles) if heading_styles else 0
                if style_variance < 4:  # Low variance = consistent
                    score += 1.5
                else:
                    score += 0.5
            
            # Check formatting consistency
            bullet_patterns = [r'^\*\s+', r'^-\s+', r'^\d+\.\s+']
            pattern_counts = [len(re.findall(pattern, text, re.MULTILINE)) for pattern in bullet_patterns]
            dominant_pattern = max(pattern_counts) if pattern_counts else 0
            other_patterns = sum(pattern_counts) - dominant_pattern
            
            if other_patterns == 0 and dominant_pattern > 0:
                score += 2.0  # Consistent formatting
            elif other_patterns < dominant_pattern / 2:
                score += 1.0  # Mostly consistent
            
            # Check paragraph consistency
            paragraphs = text.split('\n\n')
            if len(paragraphs) > 2:
                para_lengths = [len(p.split()) for p in paragraphs if p.strip()]
                if para_lengths:
                    avg_length = np.mean(para_lengths)
                    length_variance = np.var(para_lengths)
                    if length_variance < avg_length:  # Consistent paragraph lengths
                        score += 1.5
                    else:
                        score += 0.5
            
            return min(10.0, max(0.0, score))
            
        except Exception as e:
            logger.error(f"Error calculating consistency score: {e}")
            return 5.0
    
    def _find_accuracy_indicators(self, text: str) -> List[str]:
        """Find indicators of content accuracy"""
        indicators = []
        
        # Look for dates (potentially outdated)
        date_patterns = [
            r'\b(19|20)\d{2}\b',  # Years
            r'\b\d{1,2}/\d{1,2}/(19|20)\d{2}\b',  # Dates
            r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+(19|20)\d{2}\b'
        ]
        
        dates_found = []
        for pattern in date_patterns:
            dates_found.extend(re.findall(pattern, text))
        
        if dates_found:
            indicators.append(f"Contains {len(dates_found)} date references - verify currency")
        
        # Look for version numbers
        version_pattern = r'\bv?\d+\.\d+(?:\.\d+)?\b'
        versions = re.findall(version_pattern, text)
        if versions:
            indicators.append(f"Contains {len(versions)} version references - check if current")
        
        # Look for "todo" or incomplete markers
        incomplete_markers = ['TODO', 'FIXME', 'TBD', 'coming soon', 'will be updated']
        for marker in incomplete_markers:
            if marker.lower() in text.lower():
                indicators.append(f"Contains incomplete marker: '{marker}'")
        
        # Look for URLs (may be outdated)
        url_pattern = r'https?://[^\s<>"{\|}\\^`\[\]]+'
        urls = re.findall(url_pattern, text)
        if urls:
            indicators.append(f"Contains {len(urls)} URLs - verify links are active")
        
        return indicators

    def analyze_semantic_structure(self, content: ContentModel) -> AnalysisResult:
        """Analyze semantic structure and topic flow"""
        try:
            text = content.raw_text
            
            # Split into sections based on headings
            sections = self._split_into_semantic_sections(text)
            
            # Analyze topic coherence
            coherence_score = self._calculate_topic_coherence(sections)
            
            # Analyze information flow
            flow_score = self._analyze_information_flow(sections)
            
            # Generate topic model
            topics = self._extract_topic_model(text)
            
            results = {
                'sections': len(sections),
                'coherence_score': coherence_score,
                'flow_score': flow_score,
                'topics': topics,
                'semantic_density': self._calculate_semantic_density(text),
                'topic_transitions': self._analyze_topic_transitions(sections)
            }
            
            return AnalysisResult(
                content_id=content.content_id,
                analysis_type="semantic_structure",
                results=results,
                confidence_score=0.75
            )
            
        except Exception as e:
            logger.error(f"Error in semantic analysis: {e}")
            return AnalysisResult(
                content_id=content.content_id,
                analysis_type="semantic_structure",
                results={},
                confidence_score=0.0
            )
    
    def _split_into_semantic_sections(self, text: str) -> List[Dict[str, str]]:
        """Split text into semantic sections"""
        sections = []
        
        # Split by headers first
        header_pattern = r'^(#+)\s+(.+)$'
        lines = text.split('\n')
        current_section = {"level": 0, "title": "Introduction", "content": ""}
        
        for line in lines:
            header_match = re.match(header_pattern, line)
            if header_match:
                # Save previous section
                if current_section["content"].strip():
                    sections.append(current_section)
                
                # Start new section
                level = len(header_match.group(1))
                title = header_match.group(2)
                current_section = {"level": level, "title": title, "content": ""}
            else:
                current_section["content"] += line + "\n"
        
        # Add the last section
        if current_section["content"].strip():
            sections.append(current_section)
        
        return sections
    
    def _calculate_topic_coherence(self, sections: List[Dict[str, str]]) -> float:
        """Calculate topic coherence across sections"""
        if len(sections) < 2:
            return 8.0  # Single section is coherent by default
        
        try:
            if self.sentence_model:
                # Generate embeddings for each section
                embeddings = []
                for section in sections:
                    content = section.get("content", "")
                    if content.strip():
                        embedding = self.sentence_model.encode(content)
                        embeddings.append(embedding)
                
                if len(embeddings) < 2:
                    return 7.0
                
                # Calculate pairwise similarities
                similarities = []
                for i in range(len(embeddings) - 1):
                    similarity = np.dot(embeddings[i], embeddings[i + 1]) / (
                        np.linalg.norm(embeddings[i]) * np.linalg.norm(embeddings[i + 1])
                    )
                    similarities.append(similarity)
                
                # Convert to 0-10 scale
                avg_similarity = np.mean(similarities)
                coherence_score = (avg_similarity + 1) * 5  # Convert from [-1,1] to [0,10]
                return min(10.0, max(0.0, coherence_score))
            
            else:
                # Fallback: keyword overlap analysis
                return self._calculate_keyword_coherence(sections)
                
        except Exception as e:
            logger.error(f"Error calculating topic coherence: {e}")
            return 5.0
    
    def _calculate_keyword_coherence(self, sections: List[Dict[str, str]]) -> float:
        """Fallback coherence calculation using keyword overlap"""
        try:
            section_keywords = []
            for section in sections:
                content = section.get("content", "")
                words = re.findall(r'\b[a-zA-Z]{4,}\b', content.lower())
                # Get most frequent words
                word_freq = {}
                for word in words:
                    word_freq[word] = word_freq.get(word, 0) + 1
                
                top_words = set([word for word, freq in sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]])
                section_keywords.append(top_words)
            
            if len(section_keywords) < 2:
                return 7.0
            
            # Calculate average overlap between consecutive sections
            overlaps = []
            for i in range(len(section_keywords) - 1):
                overlap = len(section_keywords[i] & section_keywords[i + 1])
                total_unique = len(section_keywords[i] | section_keywords[i + 1])
                if total_unique > 0:
                    overlap_ratio = overlap / total_unique
                    overlaps.append(overlap_ratio)
            
            avg_overlap = np.mean(overlaps) if overlaps else 0
            return min(10.0, avg_overlap * 20)  # Scale to 0-10
            
        except Exception as e:
            logger.error(f"Error in keyword coherence calculation: {e}")
            return 5.0

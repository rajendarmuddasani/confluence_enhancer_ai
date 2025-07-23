"""
Content Modernizer module for updating writing style, structure, and presentation
"""
import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

@dataclass
class ContentModernizationSuggestion:
    content_id: str
    section: str
    issue_type: str
    current_text: str
    suggested_text: str
    reason: str
    impact: str  # "low", "medium", "high"
    category: str  # "style", "structure", "accessibility", "readability"

class ContentModernizer:
    """Modernizes content style, structure, and presentation"""
    
    def __init__(self):
        self.modernization_rules = self._load_modernization_rules()
        self.style_patterns = self._load_style_patterns()
        
    def _load_modernization_rules(self) -> Dict[str, Dict]:
        """Load content modernization rules"""
        return {
            "heading_structure": {
                "patterns": [
                    r"^(.+)\n=+$",  # Underlined headings
                    r"^(.+)\n-+$",  # Underlined subheadings
                ],
                "suggestion": "Use Markdown heading syntax (# ## ###)",
                "category": "structure",
                "impact": "medium"
            },
            "outdated_phrases": {
                "replacements": {
                    "please find attached": "I've attached",
                    "as per": "according to",
                    "at this point in time": "now",
                    "in order to": "to",
                    "due to the fact that": "because",
                    "it should be noted that": "",
                    "it is important to note": "",
                    "needless to say": "",
                    "last but not least": "finally",
                    "at the end of the day": "ultimately"
                },
                "category": "style",
                "impact": "low"
            },
            "passive_voice": {
                "patterns": [
                    r"\b(is|are|was|were|being|been)\s+\w+ed\b",
                    r"\b(is|are|was|were)\s+(being\s+)?\w+ed\s+by\b"
                ],
                "suggestion": "Consider using active voice for clarity",
                "category": "style",
                "impact": "medium"
            },
            "accessibility": {
                "patterns": [
                    r"click here",
                    r"read more",
                    r"see below",
                    r"above mentioned",
                    r"this link"
                ],
                "suggestion": "Use descriptive link text for accessibility",
                "category": "accessibility",
                "impact": "high"
            },
            "inclusive_language": {
                "replacements": {
                    "guys": "everyone",
                    "man hours": "person hours",
                    "manpower": "workforce",
                    "whitelist": "allowlist",
                    "blacklist": "blocklist",
                    "master/slave": "primary/secondary",
                    "sanity check": "validity check",
                    "crazy": "unusual",
                    "insane": "extreme"
                },
                "category": "style",
                "impact": "high"
            },
            "table_formatting": {
                "patterns": [
                    r"\|.*\|.*\|",  # Simple table detection
                ],
                "suggestion": "Consider using modern table formatting with proper headers",
                "category": "structure",
                "impact": "medium"
            },
            "code_formatting": {
                "patterns": [
                    r"```\n.*```",  # Code blocks without language
                    r"`[^`\n]{50,}`"  # Very long inline code
                ],
                "suggestion": "Specify language for code blocks and break long inline code",
                "category": "structure",
                "impact": "medium"
            }
        }
    
    def _load_style_patterns(self) -> Dict[str, List[str]]:
        """Load patterns for style analysis"""
        return {
            "wordy_expressions": [
                r"in spite of the fact that",
                r"due to the fact that",
                r"for the purpose of",
                r"in the event that",
                r"in the process of",
                r"at this point in time",
                r"in order to",
                r"it should be noted that"
            ],
            "weak_language": [
                r"\bpretty\s+\w+",
                r"\bsort\s+of",
                r"\bkind\s+of",
                r"\bthing\b",
                r"\bstuff\b",
                r"\bbasically\b",
                r"\bactually\b"
            ],
            "redundant_phrases": [
                r"absolutely essential",
                r"completely finished",
                r"totally unique",
                r"very unique",
                r"end result",
                r"final outcome",
                r"past history",
                r"advance planning"
            ]
        }
    
    def analyze_content(self, content: str, content_id: str) -> List[ContentModernizationSuggestion]:
        """Analyze content for modernization opportunities"""
        suggestions = []
        
        # Split content into sections for analysis
        sections = self._split_into_sections(content)
        
        for section_name, section_content in sections.items():
            # Check each modernization rule
            for rule_name, rule_config in self.modernization_rules.items():
                section_suggestions = self._apply_rule(
                    rule_name, rule_config, section_content, content_id, section_name
                )
                suggestions.extend(section_suggestions)
        
        # Sort by impact and category
        suggestions.sort(key=lambda x: (
            {"high": 3, "medium": 2, "low": 1}[x.impact],
            x.category
        ), reverse=True)
        
        return suggestions
    
    def _split_into_sections(self, content: str) -> Dict[str, str]:
        """Split content into logical sections"""
        sections = {"main": content}
        
        # Try to identify sections by headers
        header_pattern = r"^#+\s+(.+)$"
        lines = content.split('\n')
        current_section = "introduction"
        current_content = []
        
        for line in lines:
            header_match = re.match(header_pattern, line, re.MULTILINE)
            if header_match:
                # Save previous section
                if current_content:
                    sections[current_section] = '\n'.join(current_content)
                
                # Start new section
                current_section = header_match.group(1).lower().replace(' ', '_')
                current_content = [line]
            else:
                current_content.append(line)
        
        # Save last section
        if current_content:
            sections[current_section] = '\n'.join(current_content)
        
        return sections
    
    def _apply_rule(self, rule_name: str, rule_config: Dict, content: str, 
                   content_id: str, section: str) -> List[ContentModernizationSuggestion]:
        """Apply a specific modernization rule to content"""
        suggestions = []
        
        if rule_name == "heading_structure":
            suggestions.extend(self._check_heading_structure(content, content_id, section, rule_config))
        elif rule_name == "outdated_phrases":
            suggestions.extend(self._check_outdated_phrases(content, content_id, section, rule_config))
        elif rule_name == "passive_voice":
            suggestions.extend(self._check_passive_voice(content, content_id, section, rule_config))
        elif rule_name == "accessibility":
            suggestions.extend(self._check_accessibility(content, content_id, section, rule_config))
        elif rule_name == "inclusive_language":
            suggestions.extend(self._check_inclusive_language(content, content_id, section, rule_config))
        elif rule_name == "table_formatting":
            suggestions.extend(self._check_table_formatting(content, content_id, section, rule_config))
        elif rule_name == "code_formatting":
            suggestions.extend(self._check_code_formatting(content, content_id, section, rule_config))
        
        return suggestions
    
    def _check_heading_structure(self, content: str, content_id: str, section: str, 
                                rule_config: Dict) -> List[ContentModernizationSuggestion]:
        """Check for outdated heading structure"""
        suggestions = []
        
        for pattern in rule_config["patterns"]:
            matches = re.finditer(pattern, content, re.MULTILINE)
            for match in matches:
                suggestions.append(ContentModernizationSuggestion(
                    content_id=content_id,
                    section=section,
                    issue_type="heading_structure",
                    current_text=match.group(0),
                    suggested_text=f"# {match.group(1)}" if "=+" in match.group(0) else f"## {match.group(1)}",
                    reason=rule_config["suggestion"],
                    impact=rule_config["impact"],
                    category=rule_config["category"]
                ))
        
        return suggestions
    
    def _check_outdated_phrases(self, content: str, content_id: str, section: str, 
                               rule_config: Dict) -> List[ContentModernizationSuggestion]:
        """Check for outdated phrases"""
        suggestions = []
        
        for old_phrase, new_phrase in rule_config["replacements"].items():
            pattern = r'\b' + re.escape(old_phrase) + r'\b'
            matches = re.finditer(pattern, content, re.IGNORECASE)
            
            for match in matches:
                context_start = max(0, match.start() - 50)
                context_end = min(len(content), match.end() + 50)
                context = content[context_start:context_end]
                
                suggested_text = content[context_start:match.start() - context_start] + new_phrase + content[match.end() - context_start:context_end - context_start]
                
                suggestions.append(ContentModernizationSuggestion(
                    content_id=content_id,
                    section=section,
                    issue_type="outdated_phrase",
                    current_text=context,
                    suggested_text=suggested_text,
                    reason=f"Replace outdated phrase '{old_phrase}' with modern alternative",
                    impact=rule_config["impact"],
                    category=rule_config["category"]
                ))
        
        return suggestions
    
    def _check_passive_voice(self, content: str, content_id: str, section: str, 
                            rule_config: Dict) -> List[ContentModernizationSuggestion]:
        """Check for excessive passive voice usage"""
        suggestions = []
        
        for pattern in rule_config["patterns"]:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                # Get surrounding context
                sentence_start = content.rfind('.', 0, match.start()) + 1
                sentence_end = content.find('.', match.end())
                if sentence_end == -1:
                    sentence_end = len(content)
                
                sentence = content[sentence_start:sentence_end].strip()
                
                suggestions.append(ContentModernizationSuggestion(
                    content_id=content_id,
                    section=section,
                    issue_type="passive_voice",
                    current_text=sentence,
                    suggested_text=f"[Consider rewriting in active voice] {sentence}",
                    reason=rule_config["suggestion"],
                    impact=rule_config["impact"],
                    category=rule_config["category"]
                ))
        
        return suggestions
    
    def _check_accessibility(self, content: str, content_id: str, section: str, 
                           rule_config: Dict) -> List[ContentModernizationSuggestion]:
        """Check for accessibility issues"""
        suggestions = []
        
        for pattern in rule_config["patterns"]:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                context_start = max(0, match.start() - 30)
                context_end = min(len(content), match.end() + 30)
                context = content[context_start:context_end]
                
                suggestions.append(ContentModernizationSuggestion(
                    content_id=content_id,
                    section=section,
                    issue_type="accessibility",
                    current_text=context,
                    suggested_text=f"[Use descriptive text instead of '{match.group(0)}']",
                    reason=rule_config["suggestion"],
                    impact=rule_config["impact"],
                    category=rule_config["category"]
                ))
        
        return suggestions
    
    def _check_inclusive_language(self, content: str, content_id: str, section: str, 
                                 rule_config: Dict) -> List[ContentModernizationSuggestion]:
        """Check for non-inclusive language"""
        suggestions = []
        
        for old_term, new_term in rule_config["replacements"].items():
            pattern = r'\b' + re.escape(old_term) + r'\b'
            matches = re.finditer(pattern, content, re.IGNORECASE)
            
            for match in matches:
                context_start = max(0, match.start() - 30)
                context_end = min(len(content), match.end() + 30)
                context = content[context_start:context_end]
                
                suggested_text = context.replace(match.group(0), new_term)
                
                suggestions.append(ContentModernizationSuggestion(
                    content_id=content_id,
                    section=section,
                    issue_type="inclusive_language",
                    current_text=context,
                    suggested_text=suggested_text,
                    reason=f"Use more inclusive language: '{old_term}' → '{new_term}'",
                    impact=rule_config["impact"],
                    category=rule_config["category"]
                ))
        
        return suggestions
    
    def _check_table_formatting(self, content: str, content_id: str, section: str, 
                               rule_config: Dict) -> List[ContentModernizationSuggestion]:
        """Check table formatting"""
        suggestions = []
        
        # Find table-like structures
        for pattern in rule_config["patterns"]:
            matches = re.finditer(pattern, content, re.MULTILINE)
            for match in matches:
                # Get the full table context
                lines = content.split('\n')
                match_line = content[:match.start()].count('\n')
                
                # Find table boundaries
                table_start = match_line
                table_end = match_line
                
                for i in range(match_line, len(lines)):
                    if '|' in lines[i]:
                        table_end = i
                    else:
                        break
                
                table_content = '\n'.join(lines[table_start:table_end + 1])
                
                suggestions.append(ContentModernizationSuggestion(
                    content_id=content_id,
                    section=section,
                    issue_type="table_formatting",
                    current_text=table_content,
                    suggested_text="[Consider using modern table formatting with proper headers and alignment]",
                    reason=rule_config["suggestion"],
                    impact=rule_config["impact"],
                    category=rule_config["category"]
                ))
        
        return suggestions
    
    def _check_code_formatting(self, content: str, content_id: str, section: str, 
                              rule_config: Dict) -> List[ContentModernizationSuggestion]:
        """Check code formatting"""
        suggestions = []
        
        for pattern in rule_config["patterns"]:
            matches = re.finditer(pattern, content, re.DOTALL)
            for match in matches:
                if pattern == r"```\n.*```":
                    # Code block without language
                    suggestions.append(ContentModernizationSuggestion(
                        content_id=content_id,
                        section=section,
                        issue_type="code_formatting",
                        current_text=match.group(0)[:100] + "...",
                        suggested_text="```[language]\n[code]\n```",
                        reason="Specify programming language for syntax highlighting",
                        impact=rule_config["impact"],
                        category=rule_config["category"]
                    ))
                else:
                    # Long inline code
                    suggestions.append(ContentModernizationSuggestion(
                        content_id=content_id,
                        section=section,
                        issue_type="code_formatting",
                        current_text=match.group(0)[:50] + "...",
                        suggested_text="Consider using code block for long code snippets",
                        reason="Long inline code reduces readability",
                        impact=rule_config["impact"],
                        category=rule_config["category"]
                    ))
        
        return suggestions
    
    def generate_modernization_summary(self, suggestions: List[ContentModernizationSuggestion]) -> Dict:
        """Generate a summary of modernization suggestions"""
        summary = {
            "total_suggestions": len(suggestions),
            "by_category": {},
            "by_impact": {},
            "by_section": {},
            "priority_recommendations": []
        }
        
        # Count by category
        for suggestion in suggestions:
            category = suggestion.category
            impact = suggestion.impact
            section = suggestion.section
            
            summary["by_category"][category] = summary["by_category"].get(category, 0) + 1
            summary["by_impact"][impact] = summary["by_impact"].get(impact, 0) + 1
            summary["by_section"][section] = summary["by_section"].get(section, 0) + 1
        
        # Get high-impact recommendations
        high_impact = [s for s in suggestions if s.impact == "high"]
        summary["priority_recommendations"] = high_impact[:5]  # Top 5
        
        return summary

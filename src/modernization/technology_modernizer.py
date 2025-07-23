"""
Technology Modernizer module for identifying and suggesting updates to legacy technologies
"""
import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

@dataclass
class TechnologyMapping:
    old_tech: str
    new_tech: str
    confidence: float
    reason: str
    migration_complexity: str  # "low", "medium", "high"
    
@dataclass
class ModernizationSuggestion:
    content_id: str
    original_text: str
    suggested_text: str
    technology_mappings: List[TechnologyMapping]
    impact_score: float
    priority: str  # "low", "medium", "high", "critical"
    estimated_effort: str

class TechnologyModernizer:
    """Identifies outdated technologies and suggests modern alternatives"""
    
    def __init__(self):
        self.technology_mappings = self._load_technology_mappings()
        self.version_patterns = self._load_version_patterns()
        
    def _load_technology_mappings(self) -> Dict[str, Dict]:
        """Load predefined technology mappings"""
        return {
            # JavaScript Frameworks
            "jquery": {
                "modern_alternatives": ["React", "Vue.js", "Angular"],
                "default_suggestion": "React",
                "complexity": "medium",
                "reason": "Modern component-based frameworks offer better maintainability"
            },
            "backbone.js": {
                "modern_alternatives": ["React", "Vue.js", "Angular"],
                "default_suggestion": "React",
                "complexity": "high",
                "reason": "Modern frameworks provide better state management and component architecture"
            },
            
            # CSS Frameworks
            "bootstrap 3": {
                "modern_alternatives": ["Bootstrap 5", "Tailwind CSS", "Material-UI"],
                "default_suggestion": "Bootstrap 5",
                "complexity": "low",
                "reason": "Bootstrap 5 offers improved flexbox support and better customization"
            },
            
            # Database Technologies
            "mysql 5.6": {
                "modern_alternatives": ["MySQL 8.0", "PostgreSQL 14+", "Oracle 21c"],
                "default_suggestion": "MySQL 8.0",
                "complexity": "medium",
                "reason": "Newer versions provide better performance and security features"
            },
            
            # Programming Languages
            "python 2.7": {
                "modern_alternatives": ["Python 3.9+", "Python 3.11"],
                "default_suggestion": "Python 3.11",
                "complexity": "high",
                "reason": "Python 2.7 is deprecated and no longer supported"
            },
            
            # Web Servers
            "apache 2.2": {
                "modern_alternatives": ["Apache 2.4", "Nginx", "Caddy"],
                "default_suggestion": "Apache 2.4",
                "complexity": "medium",
                "reason": "Newer versions offer better performance and security"
            },
            
            # Build Tools
            "grunt": {
                "modern_alternatives": ["Webpack", "Vite", "Rollup"],
                "default_suggestion": "Vite",
                "complexity": "medium",
                "reason": "Modern build tools offer faster builds and better optimization"
            },
            
            # Testing Frameworks
            "qunit": {
                "modern_alternatives": ["Jest", "Vitest", "Cypress"],
                "default_suggestion": "Jest",
                "complexity": "low",
                "reason": "Modern testing frameworks offer better features and ecosystem support"
            }
        }
    
    def _load_version_patterns(self) -> Dict[str, List[str]]:
        """Load regex patterns for detecting technology versions"""
        return {
            "javascript_frameworks": [
                r"jquery['\"]?\s*[:=]\s*['\"]?(\d+\.\d+\.\d+)",
                r"angular['\"]?\s*[:=]\s*['\"]?(\d+\.\d+\.\d+)",
                r"react['\"]?\s*[:=]\s*['\"]?(\d+\.\d+\.\d+)",
                r"vue['\"]?\s*[:=]\s*['\"]?(\d+\.\d+\.\d+)"
            ],
            "css_frameworks": [
                r"bootstrap['\"]?\s*[:=]\s*['\"]?(\d+\.\d+\.\d+)",
                r"foundation['\"]?\s*[:=]\s*['\"]?(\d+\.\d+\.\d+)"
            ],
            "databases": [
                r"mysql['\"]?\s*[:=]\s*['\"]?(\d+\.\d+)",
                r"postgresql['\"]?\s*[:=]\s*['\"]?(\d+\.\d+)",
                r"oracle['\"]?\s*[:=]\s*['\"]?(\d+\w*)"
            ],
            "languages": [
                r"python['\"]?\s*[:=]\s*['\"]?(\d+\.\d+)",
                r"java['\"]?\s*[:=]\s*['\"]?(\d+)",
                r"node['\"]?\s*[:=]\s*['\"]?(\d+\.\d+\.\d+)"
            ]
        }
    
    def analyze_content(self, content: str, content_id: str) -> List[ModernizationSuggestion]:
        """Analyze content for outdated technologies and generate modernization suggestions"""
        suggestions = []
        
        # Detect technologies and versions
        detected_technologies = self._detect_technologies(content)
        
        for tech_info in detected_technologies:
            tech_name = tech_info["name"].lower()
            version = tech_info.get("version", "")
            
            # Check if technology needs modernization
            if tech_name in self.technology_mappings:
                mapping_info = self.technology_mappings[tech_name]
                
                # Create technology mapping
                tech_mapping = TechnologyMapping(
                    old_tech=f"{tech_info['name']} {version}".strip(),
                    new_tech=mapping_info["default_suggestion"],
                    confidence=self._calculate_confidence(tech_name, version),
                    reason=mapping_info["reason"],
                    migration_complexity=mapping_info["complexity"]
                )
                
                # Generate modernization suggestion
                suggestion = self._generate_modernization_suggestion(
                    content_id, content, tech_mapping, tech_info
                )
                suggestions.append(suggestion)
        
        # Sort by priority and impact
        suggestions.sort(key=lambda x: (
            {"critical": 4, "high": 3, "medium": 2, "low": 1}[x.priority],
            x.impact_score
        ), reverse=True)
        
        return suggestions
    
    def _detect_technologies(self, content: str) -> List[Dict]:
        """Detect technologies mentioned in content"""
        detected = []
        
        # Look for common technology patterns
        tech_patterns = {
            "jQuery": [r"\bjquery\b", r"\$\(", r"\.jquery"],
            "Angular": [r"\bangular\b", r"ng-"],
            "React": [r"\breact\b", r"\.jsx", r"useState", r"useEffect"],
            "Vue.js": [r"\bvue\b", r"\.vue", r"v-if", r"v-for"],
            "Bootstrap": [r"\bbootstrap\b", r"\.bs-", r"container-fluid"],
            "MySQL": [r"\bmysql\b", r"SELECT.*FROM", r"INSERT INTO"],
            "PostgreSQL": [r"\bpostgresql\b", r"\bpostgres\b"],
            "Oracle": [r"\boracle\b", r"ORA-", r"SYSDATE"],
            "Python": [r"\bpython\b", r"\.py\b", r"import ", r"def "],
            "Java": [r"\bjava\b", r"\.java\b", r"public class", r"public static void"],
            "Node.js": [r"\bnode\b", r"npm ", r"require\(", r"module\.exports"],
            "Apache": [r"\bapache\b", r"httpd", r"\.htaccess"],
            "Nginx": [r"\bnginx\b", r"server_name", r"location /"],
            "Grunt": [r"\bgrunt\b", r"Gruntfile", r"grunt\."],
            "Webpack": [r"\bwebpack\b", r"webpack\.config", r"module\.exports"]
        }
        
        for tech_name, patterns in tech_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, content, re.IGNORECASE)
                if any(matches):
                    # Try to extract version information
                    version = self._extract_version(content, tech_name.lower())
                    detected.append({
                        "name": tech_name,
                        "version": version,
                        "patterns_matched": len(list(re.finditer(pattern, content, re.IGNORECASE)))
                    })
                    break  # Found this technology, move to next
        
        return detected
    
    def _extract_version(self, content: str, tech_name: str) -> str:
        """Extract version number for a specific technology"""
        # Common version patterns
        version_patterns = [
            rf"{tech_name}['\"]?\s*[:=]\s*['\"]?(\d+\.\d+\.\d+)",
            rf"{tech_name}['\"]?\s*[:=]\s*['\"]?(\d+\.\d+)",
            rf"{tech_name}['\"]?\s*[:=]\s*['\"]?(\d+)",
            rf"version['\"]?\s*[:=]\s*['\"]?(\d+\.\d+\.\d+)",
            rf"v(\d+\.\d+\.\d+)",
            rf"(\d+\.\d+\.\d+)"
        ]
        
        for pattern in version_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return ""
    
    def _calculate_confidence(self, tech_name: str, version: str) -> float:
        """Calculate confidence score for modernization suggestion"""
        base_confidence = 0.7
        
        # Higher confidence for well-known outdated technologies
        if tech_name in ["jquery", "python 2.7", "bootstrap 3"]:
            base_confidence = 0.9
        
        # Adjust based on version information availability
        if version:
            base_confidence += 0.1
        
        return min(base_confidence, 1.0)
    
    def _generate_modernization_suggestion(
        self, content_id: str, content: str, tech_mapping: TechnologyMapping, tech_info: Dict
    ) -> ModernizationSuggestion:
        """Generate a complete modernization suggestion"""
        
        # Calculate impact score
        impact_score = self._calculate_impact_score(tech_info, content)
        
        # Determine priority
        priority = self._determine_priority(tech_mapping.old_tech, impact_score)
        
        # Generate suggested text
        suggested_text = self._generate_suggested_text(content, tech_mapping)
        
        # Estimate effort
        effort = self._estimate_effort(tech_mapping.migration_complexity, impact_score)
        
        return ModernizationSuggestion(
            content_id=content_id,
            original_text=content[:500] + "..." if len(content) > 500 else content,
            suggested_text=suggested_text,
            technology_mappings=[tech_mapping],
            impact_score=impact_score,
            priority=priority,
            estimated_effort=effort
        )
    
    def _calculate_impact_score(self, tech_info: Dict, content: str) -> float:
        """Calculate the impact score of modernizing this technology"""
        score = 0.5  # Base score
        
        # Higher score for more mentions
        patterns_matched = tech_info.get("patterns_matched", 1)
        score += min(patterns_matched * 0.1, 0.3)
        
        # Higher score for deprecated technologies
        deprecated_techs = ["jquery", "python 2.7", "bootstrap 3", "grunt", "backbone.js"]
        if tech_info["name"].lower() in deprecated_techs:
            score += 0.3
        
        # Higher score for security-critical technologies
        security_critical = ["mysql", "postgresql", "oracle", "apache", "nginx"]
        if any(tech in tech_info["name"].lower() for tech in security_critical):
            score += 0.2
        
        return min(score, 1.0)
    
    def _determine_priority(self, old_tech: str, impact_score: float) -> str:
        """Determine the priority of the modernization"""
        if "python 2.7" in old_tech.lower() or impact_score > 0.8:
            return "critical"
        elif impact_score > 0.6:
            return "high"
        elif impact_score > 0.4:
            return "medium"
        else:
            return "low"
    
    def _generate_suggested_text(self, original_content: str, tech_mapping: TechnologyMapping) -> str:
        """Generate suggested updated text"""
        # This is a simplified approach - in practice, you'd have more sophisticated text replacement
        old_tech_lower = tech_mapping.old_tech.lower()
        new_tech = tech_mapping.new_tech
        
        # Simple replacement strategy
        suggested = original_content
        
        # Replace technology mentions
        patterns_to_replace = [
            (old_tech_lower, new_tech),
            (old_tech_lower.replace(" ", ""), new_tech.replace(" ", "")),
            (old_tech_lower.replace(".", ""), new_tech.replace(".", ""))
        ]
        
        for old_pattern, new_pattern in patterns_to_replace:
            suggested = re.sub(
                rf"\b{re.escape(old_pattern)}\b",
                new_pattern,
                suggested,
                flags=re.IGNORECASE
            )
        
        return suggested
    
    def _estimate_effort(self, complexity: str, impact_score: float) -> str:
        """Estimate the effort required for modernization"""
        effort_mapping = {
            "low": "1-2 days",
            "medium": "1-2 weeks",
            "high": "2-4 weeks"
        }
        
        base_effort = effort_mapping.get(complexity, "1-2 weeks")
        
        # Adjust based on impact score
        if impact_score > 0.8:
            if "days" in base_effort:
                base_effort = base_effort.replace("days", "weeks")
            elif "1-2 weeks" in base_effort:
                base_effort = "2-4 weeks"
        
        return base_effort

    def get_modernization_roadmap(self, suggestions: List[ModernizationSuggestion]) -> Dict:
        """Generate a modernization roadmap based on suggestions"""
        roadmap = {
            "phases": [],
            "total_estimated_effort": "",
            "priority_breakdown": {"critical": 0, "high": 0, "medium": 0, "low": 0},
            "technology_categories": {}
        }
        
        # Group suggestions by priority
        priority_groups = {"critical": [], "high": [], "medium": [], "low": []}
        for suggestion in suggestions:
            priority_groups[suggestion.priority].append(suggestion)
            roadmap["priority_breakdown"][suggestion.priority] += 1
        
        # Create phases
        phase_num = 1
        for priority in ["critical", "high", "medium", "low"]:
            if priority_groups[priority]:
                roadmap["phases"].append({
                    "phase": phase_num,
                    "priority": priority,
                    "suggestions": priority_groups[priority],
                    "estimated_duration": self._calculate_phase_duration(priority_groups[priority])
                })
                phase_num += 1
        
        return roadmap
    
    def _calculate_phase_duration(self, suggestions: List[ModernizationSuggestion]) -> str:
        """Calculate estimated duration for a phase"""
        total_weeks = 0
        for suggestion in suggestions:
            effort = suggestion.estimated_effort
            if "days" in effort:
                weeks = 1
            elif "1-2 weeks" in effort:
                weeks = 2
            elif "2-4 weeks" in effort:
                weeks = 3
            else:
                weeks = 2
            total_weeks += weeks
        
        return f"{total_weeks} weeks"

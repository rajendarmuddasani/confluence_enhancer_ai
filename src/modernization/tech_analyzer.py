"""
Technology stack analysis module
"""
import logging
import re
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

from ..models.content_model import ContentModel


logger = logging.getLogger(__name__)


@dataclass
class TechnologyInfo:
    """Information about a technology"""
    name: str
    version: Optional[str] = None
    category: str = "unknown"
    release_date: Optional[str] = None
    end_of_life: Optional[str] = None
    support_status: str = "unknown"
    popularity_score: float = 0.0
    security_score: float = 0.0


@dataclass
class TechnologyDetection:
    """Result of technology detection"""
    technology: TechnologyInfo
    confidence: float
    context: str
    line_number: Optional[int] = None
    suggestions: List[str] = None


class TechAnalyzer:
    """Analyze technology stack from content"""
    
    def __init__(self):
        self.technology_patterns = self._load_technology_patterns()
        self.version_patterns = self._load_version_patterns()
        self.technology_database = self._load_technology_database()
        
    def _load_technology_patterns(self) -> Dict[str, List[str]]:
        """Load technology detection patterns"""
        return {
            # Programming Languages
            'python': [
                r'\bpython\s*([0-9]+\.?[0-9]*\.?[0-9]*)\b',
                r'\bpython\b',
                r'\.py\b',
                r'\bpip\s+install\b',
                r'\bvirtualenv\b',
                r'\bconda\b'
            ],
            'java': [
                r'\bjava\s*([0-9]+)\b',
                r'\bopenjdk\b',
                r'\boracle\s+jdk\b',
                r'\.jar\b',
                r'\bmaven\b',
                r'\bgradle\b'
            ],
            'javascript': [
                r'\bnode\.?js\s*([0-9]+\.?[0-9]*\.?[0-9]*)\b',
                r'\bnpm\b',
                r'\byarn\b',
                r'package\.json',
                r'\.js\b'
            ],
            'typescript': [
                r'\btypescript\s*([0-9]+\.?[0-9]*\.?[0-9]*)\b',
                r'\.ts\b',
                r'\btsc\b'
            ],
            
            # Frameworks
            'react': [
                r'\breact\s*([0-9]+\.?[0-9]*\.?[0-9]*)\b',
                r'react-dom',
                r'jsx',
                r'create-react-app'
            ],
            'angular': [
                r'\bangular\s*([0-9]+\.?[0-9]*\.?[0-9]*)\b',
                r'@angular/',
                r'ng\s+new',
                r'angular-cli'
            ],
            'vue': [
                r'\bvue\.?js\s*([0-9]+\.?[0-9]*\.?[0-9]*)\b',
                r'@vue/',
                r'vue-cli'
            ],
            'spring': [
                r'\bspring\s+boot\s*([0-9]+\.?[0-9]*\.?[0-9]*)\b',
                r'\bspring\s+framework\b',
                r'@SpringBootApplication',
                r'spring-boot-starter'
            ],
            'django': [
                r'\bdjango\s*([0-9]+\.?[0-9]*\.?[0-9]*)\b',
                r'manage\.py',
                r'django-admin',
                r'DJANGO_SETTINGS_MODULE'
            ],
            'flask': [
                r'\bflask\s*([0-9]+\.?[0-9]*\.?[0-9]*)\b',
                r'from\s+flask\s+import',
                r'@app\.route'
            ],
            
            # Databases
            'mysql': [
                r'\bmysql\s*([0-9]+\.?[0-9]*\.?[0-9]*)\b',
                r'mysqld',
                r'my\.cnf'
            ],
            'postgresql': [
                r'\bpostgresql\s*([0-9]+\.?[0-9]*\.?[0-9]*)\b',
                r'\bpostgres\b',
                r'psql',
                r'pg_dump'
            ],
            'mongodb': [
                r'\bmongodb\s*([0-9]+\.?[0-9]*\.?[0-9]*)\b',
                r'\bmongo\b',
                r'mongod',
                r'mongoose'
            ],
            'oracle': [
                r'\boracle\s+database\s*([0-9]+[a-z]*)\b',
                r'\boracle\s*([0-9]+[a-z]*)\b',
                r'sqlplus',
                r'tnsnames\.ora'
            ],
            
            # Infrastructure
            'docker': [
                r'\bdocker\s*([0-9]+\.?[0-9]*\.?[0-9]*)\b',
                r'dockerfile',
                r'docker-compose',
                r'docker\s+run'
            ],
            'kubernetes': [
                r'\bkubernetes\s*([0-9]+\.?[0-9]*\.?[0-9]*)\b',
                r'\bk8s\b',
                r'kubectl',
                r'kustomize'
            ],
            'jenkins': [
                r'\bjenkins\s*([0-9]+\.?[0-9]*\.?[0-9]*)\b',
                r'jenkinsfile',
                r'jenkins\s+pipeline'
            ],
            
            # Cloud Platforms
            'aws': [
                r'\baws\b',
                r'\bamazon\s+web\s+services\b',
                r'ec2',
                r's3',
                r'lambda',
                r'cloudformation'
            ],
            'azure': [
                r'\bAzure\b',
                r'\bMicrosoft\s+Azure\b',
                r'azure\s+devops',
                r'azure\s+functions'
            ],
            'gcp': [
                r'\bGoogle\s+Cloud\b',
                r'\bGCP\b',
                r'Google\s+Cloud\s+Platform',
                r'gcloud'
            ]
        }
    
    def _load_version_patterns(self) -> Dict[str, str]:
        """Load version extraction patterns"""
        return {
            'semantic_version': r'([0-9]+)\.([0-9]+)\.([0-9]+)',
            'major_minor': r'([0-9]+)\.([0-9]+)',
            'major_only': r'([0-9]+)',
            'year_version': r'(20[0-9]{2})',
            'oracle_version': r'([0-9]+[a-z]*)'
        }
    
    def _load_technology_database(self) -> Dict[str, TechnologyInfo]:
        """Load technology information database"""
        return {
            'python_2': TechnologyInfo(
                name='Python 2',
                category='programming_language',
                end_of_life='2020-01-01',
                support_status='deprecated',
                security_score=2.0
            ),
            'python_3_6': TechnologyInfo(
                name='Python 3.6',
                category='programming_language',
                end_of_life='2021-12-23',
                support_status='deprecated',
                security_score=6.0
            ),
            'java_8': TechnologyInfo(
                name='Java 8',
                category='programming_language',
                end_of_life='2030-12-31',
                support_status='extended_support',
                security_score=7.0
            ),
            'java_11': TechnologyInfo(
                name='Java 11',
                category='programming_language',
                support_status='lts',
                security_score=8.5
            ),
            'react_15': TechnologyInfo(
                name='React 15',
                category='frontend_framework',
                end_of_life='2018-04-03',
                support_status='deprecated',
                security_score=3.0
            ),
            'angular_1': TechnologyInfo(
                name='AngularJS',
                category='frontend_framework',
                end_of_life='2021-12-31',
                support_status='deprecated',
                security_score=2.0
            ),
            'mysql_5_5': TechnologyInfo(
                name='MySQL 5.5',
                category='database',
                end_of_life='2018-12-03',
                support_status='deprecated',
                security_score=3.0
            ),
            'oracle_11g': TechnologyInfo(
                name='Oracle 11g',
                category='database',
                end_of_life='2020-12-31',
                support_status='deprecated',
                security_score=4.0
            )
        }
    
    def analyze_technology_stack(self, content: ContentModel) -> List[TechnologyDetection]:
        """Analyze content to detect technologies"""
        try:
            logger.info(f"Analyzing technology stack in: {content.title}")
            
            detections = []
            content_text = content.raw_text.lower()
            lines = content.raw_text.split('\n')
            
            for tech_name, patterns in self.technology_patterns.items():
                for pattern in patterns:
                    matches = re.finditer(pattern, content_text, re.IGNORECASE)
                    
                    for match in matches:
                        # Find line number
                        line_number = self._find_line_number(content.raw_text, match.start())
                        
                        # Extract version if available
                        version = self._extract_version(match.group())
                        
                        # Create technology info
                        tech_info = TechnologyInfo(
                            name=tech_name,
                            version=version,
                            category=self._categorize_technology(tech_name)
                        )
                        
                        # Calculate confidence
                        confidence = self._calculate_confidence(match, pattern, content_text)
                        
                        # Get context
                        context = self._extract_context(lines, line_number)
                        
                        detection = TechnologyDetection(
                            technology=tech_info,
                            confidence=confidence,
                            context=context,
                            line_number=line_number,
                            suggestions=self._generate_suggestions(tech_name, version)
                        )
                        
                        detections.append(detection)
            
            # Remove duplicates and merge similar detections
            detections = self._deduplicate_detections(detections)
            
            return detections
            
        except Exception as e:
            logger.error(f"Error analyzing technology stack: {e}")
            return []
    
    def _find_line_number(self, text: str, position: int) -> int:
        """Find line number for character position"""
        return text[:position].count('\n') + 1
    
    def _extract_version(self, text: str) -> Optional[str]:
        """Extract version from text"""
        for pattern_name, pattern in self.version_patterns.items():
            match = re.search(pattern, text)
            if match:
                if pattern_name == 'semantic_version':
                    return f"{match.group(1)}.{match.group(2)}.{match.group(3)}"
                elif pattern_name == 'major_minor':
                    return f"{match.group(1)}.{match.group(2)}"
                else:
                    return match.group(1)
        return None
    
    def _categorize_technology(self, tech_name: str) -> str:
        """Categorize technology type"""
        categories = {
            'programming_language': ['python', 'java', 'javascript', 'typescript', 'php', 'ruby', 'go'],
            'frontend_framework': ['react', 'angular', 'vue', 'ember', 'svelte'],
            'backend_framework': ['spring', 'django', 'flask', 'express', 'rails'],
            'database': ['mysql', 'postgresql', 'mongodb', 'oracle', 'sqlserver'],
            'infrastructure': ['docker', 'kubernetes', 'jenkins', 'terraform'],
            'cloud_platform': ['aws', 'azure', 'gcp']
        }
        
        for category, technologies in categories.items():
            if tech_name in technologies:
                return category
        
        return 'unknown'
    
    def _calculate_confidence(self, match: re.Match, pattern: str, content: str) -> float:
        """Calculate confidence score for detection"""
        base_confidence = 0.5
        
        # Higher confidence for version-specific patterns
        if re.search(r'[0-9]+', pattern):
            base_confidence += 0.2
        
        # Higher confidence for exact matches
        if match.group() == pattern:
            base_confidence += 0.2
        
        # Context-based confidence boost
        context_window = content[max(0, match.start() - 50):match.end() + 50]
        
        # Look for related keywords
        if any(keyword in context_window for keyword in ['install', 'version', 'upgrade', 'dependency']):
            base_confidence += 0.1
        
        return min(1.0, base_confidence)
    
    def _extract_context(self, lines: List[str], line_number: int) -> str:
        """Extract context around detection"""
        start_line = max(0, line_number - 2)
        end_line = min(len(lines), line_number + 2)
        
        context_lines = lines[start_line:end_line]
        return '\n'.join(context_lines).strip()
    
    def _generate_suggestions(self, tech_name: str, version: Optional[str]) -> List[str]:
        """Generate suggestions for technology"""
        suggestions = []
        
        # Version-specific suggestions
        if tech_name == 'python' and version:
            if version.startswith('2'):
                suggestions.append('Consider upgrading to Python 3.9+ for continued support')
            elif version.startswith('3.6') or version.startswith('3.7'):
                suggestions.append('Consider upgrading to Python 3.9+ for latest features')
        
        elif tech_name == 'java' and version:
            if version == '8':
                suggestions.append('Consider upgrading to Java 11 or 17 (LTS versions)')
        
        elif tech_name == 'react' and version:
            major_version = int(version.split('.')[0]) if version.split('.')[0].isdigit() else 0
            if major_version < 16:
                suggestions.append('Consider upgrading to React 18+ for latest features')
        
        elif tech_name == 'angular' and version:
            if version == '1' or version.startswith('1.'):
                suggestions.append('Consider migrating to Angular 15+ or modern alternative')
        
        # General technology suggestions
        outdated_technologies = {
            'jquery': 'Consider modern frameworks like React, Vue, or Angular',
            'backbone': 'Consider modern frameworks like React, Vue, or Angular',
            'mysql_5_5': 'Upgrade to MySQL 8.0+ for better performance and security',
            'oracle_11g': 'Upgrade to Oracle 19c+ for continued support'
        }
        
        if tech_name in outdated_technologies:
            suggestions.append(outdated_technologies[tech_name])
        
        return suggestions
    
    def _deduplicate_detections(self, detections: List[TechnologyDetection]) -> List[TechnologyDetection]:
        """Remove duplicate detections and merge similar ones"""
        unique_detections = {}
        
        for detection in detections:
            key = f"{detection.technology.name}_{detection.technology.version or 'no_version'}"
            
            if key not in unique_detections:
                unique_detections[key] = detection
            else:
                # Keep the one with higher confidence
                if detection.confidence > unique_detections[key].confidence:
                    unique_detections[key] = detection
        
        return list(unique_detections.values())
    
    def assess_technology_risk(self, detections: List[TechnologyDetection]) -> Dict[str, Any]:
        """Assess risk level of detected technologies"""
        try:
            risk_assessment = {
                'overall_risk': 'low',
                'high_risk_technologies': [],
                'deprecated_technologies': [],
                'outdated_versions': [],
                'security_concerns': [],
                'recommendations': []
            }
            
            high_risk_count = 0
            deprecated_count = 0
            
            for detection in detections:
                tech = detection.technology
                tech_key = f"{tech.name}_{tech.version or ''}".lower().replace(' ', '_')
                
                # Check if technology is in our database
                if tech_key in self.technology_database:
                    tech_info = self.technology_database[tech_key]
                    
                    if tech_info.support_status == 'deprecated':
                        deprecated_count += 1
                        risk_assessment['deprecated_technologies'].append({
                            'name': tech.name,
                            'version': tech.version,
                            'end_of_life': tech_info.end_of_life
                        })
                    
                    if tech_info.security_score < 5.0:
                        high_risk_count += 1
                        risk_assessment['security_concerns'].append({
                            'name': tech.name,
                            'version': tech.version,
                            'security_score': tech_info.security_score
                        })
            
            # Calculate overall risk
            total_technologies = len(detections)
            if total_technologies > 0:
                risk_ratio = (high_risk_count + deprecated_count) / total_technologies
                
                if risk_ratio > 0.5:
                    risk_assessment['overall_risk'] = 'high'
                elif risk_ratio > 0.25:
                    risk_assessment['overall_risk'] = 'medium'
            
            # Generate recommendations
            if deprecated_count > 0:
                risk_assessment['recommendations'].append(
                    f"Prioritize upgrading {deprecated_count} deprecated technologies"
                )
            
            if high_risk_count > 0:
                risk_assessment['recommendations'].append(
                    f"Address security concerns in {high_risk_count} technologies"
                )
            
            return risk_assessment
            
        except Exception as e:
            logger.error(f"Error assessing technology risk: {e}")
            return {}
    
    def generate_technology_report(self, detections: List[TechnologyDetection]) -> Dict[str, Any]:
        """Generate comprehensive technology analysis report"""
        try:
            logger.info("Generating technology analysis report")
            
            # Categorize technologies
            categorized = {}
            for detection in detections:
                category = detection.technology.category
                if category not in categorized:
                    categorized[category] = []
                categorized[category].append(detection)
            
            # Risk assessment
            risk_assessment = self.assess_technology_risk(detections)
            
            # Summary statistics
            summary = {
                'total_technologies': len(detections),
                'categories': len(categorized),
                'average_confidence': sum(d.confidence for d in detections) / len(detections) if detections else 0,
                'technologies_by_category': {cat: len(techs) for cat, techs in categorized.items()}
            }
            
            return {
                'summary': summary,
                'detections': [asdict(detection) for detection in detections],
                'categorized_technologies': categorized,
                'risk_assessment': risk_assessment,
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error generating technology report: {e}")
            return {}


def asdict(obj):
    """Convert dataclass to dictionary"""
    if hasattr(obj, '__dict__'):
        result = {}
        for key, value in obj.__dict__.items():
            if hasattr(value, '__dict__'):
                result[key] = asdict(value)
            elif isinstance(value, list):
                result[key] = [asdict(item) if hasattr(item, '__dict__') else item for item in value]
            else:
                result[key] = value
        return result
    return obj

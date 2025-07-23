"""
Modern alternative suggestions module
"""
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

from .tech_analyzer import TechnologyDetection, TechnologyInfo


logger = logging.getLogger(__name__)


@dataclass
class ModernAlternative:
    """Modern alternative to legacy technology"""
    name: str
    version: str
    category: str
    benefits: List[str]
    migration_effort: str  # 'low', 'medium', 'high'
    migration_time: str
    compatibility_score: float
    learning_curve: str  # 'easy', 'moderate', 'steep'
    community_support: float
    documentation_quality: float
    cost_impact: str  # 'lower', 'similar', 'higher'


@dataclass
class MigrationPlan:
    """Migration plan for technology upgrade"""
    original_technology: str
    target_technology: str
    phases: List[Dict[str, Any]]
    estimated_duration: str
    required_skills: List[str]
    risks: List[str]
    success_criteria: List[str]
    rollback_plan: Dict[str, Any]


class AlternativeSuggester:
    """Suggest modern alternatives for legacy technologies"""
    
    def __init__(self):
        self.alternatives_database = self._load_alternatives_database()
        self.migration_templates = self._load_migration_templates()
        
    def _load_alternatives_database(self) -> Dict[str, List[ModernAlternative]]:
        """Load database of modern alternatives"""
        return {
            # Programming Languages
            'python_2': [
                ModernAlternative(
                    name='Python',
                    version='3.11+',
                    category='programming_language',
                    benefits=[
                        'Active security updates and bug fixes',
                        'Better performance and memory efficiency',
                        'Improved syntax and language features',
                        'Better Unicode and async support',
                        'Rich ecosystem of modern libraries'
                    ],
                    migration_effort='medium',
                    migration_time='2-4 months',
                    compatibility_score=0.8,
                    learning_curve='easy',
                    community_support=9.5,
                    documentation_quality=9.0,
                    cost_impact='similar'
                )
            ],
            
            'java_8': [
                ModernAlternative(
                    name='Java',
                    version='17 LTS',
                    category='programming_language',
                    benefits=[
                        'Long-term support until 2029',
                        'Improved performance and memory management',
                        'New language features (records, switch expressions)',
                        'Better container support',
                        'Enhanced security features'
                    ],
                    migration_effort='low',
                    migration_time='1-2 months',
                    compatibility_score=0.95,
                    learning_curve='easy',
                    community_support=9.0,
                    documentation_quality=9.5,
                    cost_impact='similar'
                ),
                ModernAlternative(
                    name='Kotlin',
                    version='1.8+',
                    category='programming_language',
                    benefits=[
                        '100% interoperable with Java',
                        'More concise and expressive syntax',
                        'Null safety by design',
                        'Coroutines for async programming',
                        'Strong Google/JetBrains support'
                    ],
                    migration_effort='medium',
                    migration_time='3-6 months',
                    compatibility_score=0.9,
                    learning_curve='moderate',
                    community_support=8.5,
                    documentation_quality=8.5,
                    cost_impact='similar'
                )
            ],
            
            # Frontend Frameworks
            'angular_1': [
                ModernAlternative(
                    name='Angular',
                    version='15+',
                    category='frontend_framework',
                    benefits=[
                        'Complete rewrite with TypeScript',
                        'Better performance and bundle size',
                        'Modern development tools',
                        'Strong enterprise support',
                        'Comprehensive testing framework'
                    ],
                    migration_effort='high',
                    migration_time='6-12 months',
                    compatibility_score=0.3,
                    learning_curve='steep',
                    community_support=8.0,
                    documentation_quality=9.0,
                    cost_impact='similar'
                ),
                ModernAlternative(
                    name='React',
                    version='18+',
                    category='frontend_framework',
                    benefits=[
                        'Huge ecosystem and community',
                        'Excellent performance with hooks',
                        'Strong job market demand',
                        'Flexible and lightweight',
                        'Great developer experience'
                    ],
                    migration_effort='high',
                    migration_time='4-8 months',
                    compatibility_score=0.2,
                    learning_curve='moderate',
                    community_support=9.5,
                    documentation_quality=8.5,
                    cost_impact='similar'
                ),
                ModernAlternative(
                    name='Vue.js',
                    version='3+',
                    category='frontend_framework',
                    benefits=[
                        'Gentler learning curve',
                        'Excellent documentation',
                        'Progressive adoption possible',
                        'Great performance',
                        'Growing ecosystem'
                    ],
                    migration_effort='medium',
                    migration_time='3-6 months',
                    compatibility_score=0.4,
                    learning_curve='easy',
                    community_support=8.0,
                    documentation_quality=9.5,
                    cost_impact='similar'
                )
            ],
            
            'react_15': [
                ModernAlternative(
                    name='React',
                    version='18+',
                    category='frontend_framework',
                    benefits=[
                        'Hooks for better state management',
                        'Concurrent features for better UX',
                        'Automatic batching improvements',
                        'Better server-side rendering',
                        'Improved error boundaries'
                    ],
                    migration_effort='low',
                    migration_time='1-3 months',
                    compatibility_score=0.8,
                    learning_curve='easy',
                    community_support=9.5,
                    documentation_quality=8.5,
                    cost_impact='similar'
                )
            ],
            
            # Databases
            'mysql_5_5': [
                ModernAlternative(
                    name='MySQL',
                    version='8.0+',
                    category='database',
                    benefits=[
                        'Improved performance (2x faster)',
                        'JSON document support',
                        'Window functions and CTEs',
                        'Better security features',
                        'Enhanced replication'
                    ],
                    migration_effort='low',
                    migration_time='2-4 weeks',
                    compatibility_score=0.95,
                    learning_curve='easy',
                    community_support=9.0,
                    documentation_quality=8.5,
                    cost_impact='similar'
                ),
                ModernAlternative(
                    name='PostgreSQL',
                    version='15+',
                    category='database',
                    benefits=[
                        'Advanced SQL features',
                        'Better JSON and NoSQL support',
                        'Excellent ACID compliance',
                        'Strong extensions ecosystem',
                        'Superior data integrity'
                    ],
                    migration_effort='medium',
                    migration_time='1-3 months',
                    compatibility_score=0.7,
                    learning_curve='moderate',
                    community_support=8.5,
                    documentation_quality=9.0,
                    cost_impact='similar'
                )
            ],
            
            'oracle_11g': [
                ModernAlternative(
                    name='Oracle Database',
                    version='19c+',
                    category='database',
                    benefits=[
                        'Autonomous database features',
                        'Better cloud integration',
                        'Improved performance',
                        'Enhanced security features',
                        'Machine learning capabilities'
                    ],
                    migration_effort='medium',
                    migration_time='2-4 months',
                    compatibility_score=0.9,
                    learning_curve='easy',
                    community_support=7.5,
                    documentation_quality=8.5,
                    cost_impact='higher'
                ),
                ModernAlternative(
                    name='PostgreSQL',
                    version='15+',
                    category='database',
                    benefits=[
                        'Open source with no licensing costs',
                        'Excellent SQL compliance',
                        'Strong performance',
                        'Great community support',
                        'Cloud-friendly'
                    ],
                    migration_effort='high',
                    migration_time='6-12 months',
                    compatibility_score=0.6,
                    learning_curve='moderate',
                    community_support=8.5,
                    documentation_quality=9.0,
                    cost_impact='lower'
                )
            ],
            
            # Build Tools
            'maven_2': [
                ModernAlternative(
                    name='Maven',
                    version='3.9+',
                    category='build_tool',
                    benefits=[
                        'Better performance and stability',
                        'Improved dependency resolution',
                        'Better IDE integration',
                        'Enhanced plugin ecosystem',
                        'Java 17+ support'
                    ],
                    migration_effort='low',
                    migration_time='1-2 weeks',
                    compatibility_score=0.95,
                    learning_curve='easy',
                    community_support=8.0,
                    documentation_quality=8.0,
                    cost_impact='similar'
                ),
                ModernAlternative(
                    name='Gradle',
                    version='8+',
                    category='build_tool',
                    benefits=[
                        'Better performance with build cache',
                        'More flexible build scripts',
                        'Better multi-project support',
                        'Kotlin DSL support',
                        'Incremental builds'
                    ],
                    migration_effort='medium',
                    migration_time='1-2 months',
                    compatibility_score=0.7,
                    learning_curve='moderate',
                    community_support=8.5,
                    documentation_quality=8.0,
                    cost_impact='similar'
                )
            ],
            
            # Infrastructure
            'jenkins_1': [
                ModernAlternative(
                    name='Jenkins',
                    version='2.400+',
                    category='ci_cd',
                    benefits=[
                        'Pipeline as Code support',
                        'Better security model',
                        'Blue Ocean modern UI',
                        'Container-native support',
                        'Improved plugin management'
                    ],
                    migration_effort='medium',
                    migration_time='1-2 months',
                    compatibility_score=0.8,
                    learning_curve='easy',
                    community_support=8.0,
                    documentation_quality=7.5,
                    cost_impact='similar'
                ),
                ModernAlternative(
                    name='GitHub Actions',
                    version='Latest',
                    category='ci_cd',
                    benefits=[
                        'Native GitHub integration',
                        'Serverless execution model',
                        'Rich marketplace of actions',
                        'Matrix builds support',
                        'Built-in secrets management'
                    ],
                    migration_effort='medium',
                    migration_time='2-3 months',
                    compatibility_score=0.6,
                    learning_curve='easy',
                    community_support=9.0,
                    documentation_quality=9.0,
                    cost_impact='lower'
                ),
                ModernAlternative(
                    name='GitLab CI/CD',
                    version='Latest',
                    category='ci_cd',
                    benefits=[
                        'Integrated DevOps platform',
                        'Container registry included',
                        'Auto DevOps capabilities',
                        'Built-in security scanning',
                        'Kubernetes integration'
                    ],
                    migration_effort='medium',
                    migration_time='2-4 months',
                    compatibility_score=0.7,
                    learning_curve='moderate',
                    community_support=8.0,
                    documentation_quality=8.5,
                    cost_impact='similar'
                )
            ]
        }
    
    def _load_migration_templates(self) -> Dict[str, Dict[str, Any]]:
        """Load migration plan templates"""
        return {
            'language_upgrade': {
                'phases': [
                    {
                        'name': 'Assessment',
                        'duration': '1-2 weeks',
                        'tasks': [
                            'Inventory current codebase',
                            'Identify breaking changes',
                            'Create compatibility matrix',
                            'Plan testing strategy'
                        ]
                    },
                    {
                        'name': 'Preparation',
                        'duration': '2-3 weeks',
                        'tasks': [
                            'Setup new development environment',
                            'Update build scripts',
                            'Configure CI/CD pipelines',
                            'Create migration guides'
                        ]
                    },
                    {
                        'name': 'Migration',
                        'duration': '4-8 weeks',
                        'tasks': [
                            'Update core libraries',
                            'Fix breaking changes',
                            'Update deprecated APIs',
                            'Comprehensive testing'
                        ]
                    },
                    {
                        'name': 'Validation',
                        'duration': '2-3 weeks',
                        'tasks': [
                            'Performance testing',
                            'Security review',
                            'User acceptance testing',
                            'Documentation updates'
                        ]
                    }
                ]
            },
            'framework_migration': {
                'phases': [
                    {
                        'name': 'Planning',
                        'duration': '2-4 weeks',
                        'tasks': [
                            'Architecture design',
                            'Component mapping',
                            'Data migration strategy',
                            'Team training plan'
                        ]
                    },
                    {
                        'name': 'Foundation',
                        'duration': '3-4 weeks',
                        'tasks': [
                            'Setup new framework',
                            'Core infrastructure',
                            'Shared components',
                            'Development guidelines'
                        ]
                    },
                    {
                        'name': 'Feature Migration',
                        'duration': '8-16 weeks',
                        'tasks': [
                            'Migrate features incrementally',
                            'Maintain parallel systems',
                            'Progressive rollout',
                            'User feedback integration'
                        ]
                    },
                    {
                        'name': 'Completion',
                        'duration': '2-4 weeks',
                        'tasks': [
                            'Decommission old system',
                            'Performance optimization',
                            'Final testing',
                            'Go-live support'
                        ]
                    }
                ]
            },
            'database_upgrade': {
                'phases': [
                    {
                        'name': 'Pre-Migration',
                        'duration': '2-3 weeks',
                        'tasks': [
                            'Schema compatibility check',
                            'Data backup strategy',
                            'Performance baseline',
                            'Rollback procedures'
                        ]
                    },
                    {
                        'name': 'Migration Setup',
                        'duration': '1-2 weeks',
                        'tasks': [
                            'Install new database version',
                            'Configure replication',
                            'Setup monitoring',
                            'Test environments'
                        ]
                    },
                    {
                        'name': 'Data Migration',
                        'duration': '1-3 weeks',
                        'tasks': [
                            'Schema migration',
                            'Data transfer',
                            'Index recreation',
                            'Performance tuning'
                        ]
                    },
                    {
                        'name': 'Validation',
                        'duration': '1-2 weeks',
                        'tasks': [
                            'Data integrity checks',
                            'Performance validation',
                            'Application testing',
                            'Cutover planning'
                        ]
                    }
                ]
            }
        }
    
    def suggest_alternatives(self, technology_detections: List[TechnologyDetection]) -> Dict[str, List[ModernAlternative]]:
        """Suggest modern alternatives for detected technologies"""
        try:
            logger.info(f"Suggesting alternatives for {len(technology_detections)} technologies")
            
            suggestions = {}
            
            for detection in technology_detections:
                tech = detection.technology
                tech_key = self._normalize_technology_key(tech.name, tech.version)
                
                if tech_key in self.alternatives_database:
                    alternatives = self.alternatives_database[tech_key]
                    
                    # Score alternatives based on context
                    scored_alternatives = []
                    for alt in alternatives:
                        score = self._score_alternative(alt, detection)
                        scored_alternatives.append((alt, score))
                    
                    # Sort by score and take top alternatives
                    scored_alternatives.sort(key=lambda x: x[1], reverse=True)
                    suggestions[tech_key] = [alt for alt, score in scored_alternatives]
                
                else:
                    # Generate generic suggestions for unknown technologies
                    generic_suggestions = self._generate_generic_suggestions(tech)
                    if generic_suggestions:
                        suggestions[tech_key] = generic_suggestions
            
            return suggestions
            
        except Exception as e:
            logger.error(f"Error suggesting alternatives: {e}")
            return {}
    
    def _normalize_technology_key(self, name: str, version: Optional[str]) -> str:
        """Normalize technology name and version to database key"""
        normalized_name = name.lower().replace(' ', '_').replace('.', '_')
        
        if version:
            # Handle version-specific keys
            if 'python' in normalized_name and version.startswith('2'):
                return 'python_2'
            elif 'java' in normalized_name and version.startswith('8'):
                return 'java_8'
            elif 'angular' in normalized_name and (version == '1' or version.startswith('1.')):
                return 'angular_1'
            elif 'react' in normalized_name and version.startswith('15'):
                return 'react_15'
            elif 'mysql' in normalized_name and version.startswith('5.5'):
                return 'mysql_5_5'
            elif 'oracle' in normalized_name and '11g' in version:
                return 'oracle_11g'
            elif 'maven' in normalized_name and version.startswith('2'):
                return 'maven_2'
            elif 'jenkins' in normalized_name and version.startswith('1'):
                return 'jenkins_1'
        
        return normalized_name
    
    def _score_alternative(self, alternative: ModernAlternative, detection: TechnologyDetection) -> float:
        """Score alternative based on compatibility and other factors"""
        score = 0.0
        
        # Base score from compatibility
        score += alternative.compatibility_score * 0.4
        
        # Community support weight
        score += (alternative.community_support / 10) * 0.2
        
        # Learning curve (easier is better)
        learning_scores = {'easy': 1.0, 'moderate': 0.7, 'steep': 0.3}
        score += learning_scores.get(alternative.learning_curve, 0.5) * 0.15
        
        # Migration effort (lower is better)
        effort_scores = {'low': 1.0, 'medium': 0.6, 'high': 0.2}
        score += effort_scores.get(alternative.migration_effort, 0.5) * 0.15
        
        # Cost impact (lower/similar is better)
        cost_scores = {'lower': 1.0, 'similar': 0.8, 'higher': 0.3}
        score += cost_scores.get(alternative.cost_impact, 0.5) * 0.1
        
        return score
    
    def _generate_generic_suggestions(self, tech: TechnologyInfo) -> List[ModernAlternative]:
        """Generate generic suggestions for unknown technologies"""
        category_suggestions = {
            'programming_language': [
                ModernAlternative(
                    name='Modern Language Version',
                    version='Latest LTS',
                    category='programming_language',
                    benefits=['Security updates', 'Performance improvements', 'New features'],
                    migration_effort='medium',
                    migration_time='2-4 months',
                    compatibility_score=0.8,
                    learning_curve='easy',
                    community_support=8.0,
                    documentation_quality=8.0,
                    cost_impact='similar'
                )
            ],
            'frontend_framework': [
                ModernAlternative(
                    name='Modern Frontend Framework',
                    version='Latest',
                    category='frontend_framework',
                    benefits=['Better performance', 'Modern development experience', 'Active community'],
                    migration_effort='high',
                    migration_time='4-8 months',
                    compatibility_score=0.5,
                    learning_curve='moderate',
                    community_support=8.0,
                    documentation_quality=8.0,
                    cost_impact='similar'
                )
            ]
        }
        
        return category_suggestions.get(tech.category, [])
    
    def create_migration_plan(self, original_tech: str, target_alternative: ModernAlternative) -> MigrationPlan:
        """Create detailed migration plan"""
        try:
            logger.info(f"Creating migration plan from {original_tech} to {target_alternative.name}")
            
            # Select appropriate template
            template_key = self._select_migration_template(original_tech, target_alternative)
            template = self.migration_templates.get(template_key, self.migration_templates['language_upgrade'])
            
            # Customize phases for specific migration
            customized_phases = self._customize_migration_phases(template['phases'], original_tech, target_alternative)
            
            # Generate required skills
            required_skills = self._identify_required_skills(target_alternative)
            
            # Identify risks
            risks = self._identify_migration_risks(original_tech, target_alternative)
            
            # Create success criteria
            success_criteria = self._create_success_criteria(target_alternative)
            
            # Create rollback plan
            rollback_plan = self._create_rollback_plan(original_tech, target_alternative)
            
            migration_plan = MigrationPlan(
                original_technology=original_tech,
                target_technology=f"{target_alternative.name} {target_alternative.version}",
                phases=customized_phases,
                estimated_duration=target_alternative.migration_time,
                required_skills=required_skills,
                risks=risks,
                success_criteria=success_criteria,
                rollback_plan=rollback_plan
            )
            
            return migration_plan
            
        except Exception as e:
            logger.error(f"Error creating migration plan: {e}")
            return None
    
    def _select_migration_template(self, original_tech: str, target_alternative: ModernAlternative) -> str:
        """Select appropriate migration template"""
        if target_alternative.category == 'programming_language':
            return 'language_upgrade'
        elif target_alternative.category in ['frontend_framework', 'backend_framework']:
            return 'framework_migration'
        elif target_alternative.category == 'database':
            return 'database_upgrade'
        else:
            return 'language_upgrade'  # Default template
    
    def _customize_migration_phases(self, base_phases: List[Dict], original_tech: str, target_alternative: ModernAlternative) -> List[Dict]:
        """Customize migration phases for specific technology"""
        customized_phases = []
        
        for phase in base_phases:
            customized_phase = phase.copy()
            
            # Add technology-specific tasks
            if 'python' in original_tech.lower() and 'python' in target_alternative.name.lower():
                if phase['name'] == 'Migration':
                    customized_phase['tasks'].extend([
                        'Update print statements to functions',
                        'Fix unicode/string handling',
                        'Update division operators',
                        'Migrate to new import statements'
                    ])
            
            elif 'java' in original_tech.lower() and target_alternative.name.lower() == 'kotlin':
                if phase['name'] == 'Migration':
                    customized_phase['tasks'].extend([
                        'Convert Java classes to Kotlin',
                        'Update null handling with safe operators',
                        'Migrate to Kotlin coroutines',
                        'Update build.gradle for Kotlin'
                    ])
            
            customized_phases.append(customized_phase)
        
        return customized_phases
    
    def _identify_required_skills(self, target_alternative: ModernAlternative) -> List[str]:
        """Identify skills required for migration"""
        base_skills = [
            f"{target_alternative.name} development",
            f"{target_alternative.category.replace('_', ' ').title()} architecture",
            "Migration planning and execution",
            "Testing and quality assurance"
        ]
        
        # Add technology-specific skills
        if target_alternative.name == 'Kotlin':
            base_skills.extend([
                'Kotlin coroutines',
                'Kotlin-specific patterns',
                'Java-Kotlin interoperability'
            ])
        elif target_alternative.name == 'React':
            base_skills.extend([
                'React Hooks',
                'JSX and component patterns',
                'State management (Redux/Context)',
                'Modern JavaScript (ES6+)'
            ])
        
        return base_skills
    
    def _identify_migration_risks(self, original_tech: str, target_alternative: ModernAlternative) -> List[str]:
        """Identify potential migration risks"""
        risks = [
            'Performance regression during migration',
            'Integration issues with existing systems',
            'Team learning curve and productivity impact',
            'Unexpected compatibility issues'
        ]
        
        # Add specific risks based on migration effort
        if target_alternative.migration_effort == 'high':
            risks.extend([
                'Extended development timeline',
                'Increased project complexity',
                'Higher chance of scope creep'
            ])
        
        if target_alternative.compatibility_score < 0.7:
            risks.append('Significant code changes required')
        
        return risks
    
    def _create_success_criteria(self, target_alternative: ModernAlternative) -> List[str]:
        """Create success criteria for migration"""
        return [
            'All existing functionality preserved',
            'Performance meets or exceeds baseline',
            'All tests passing in new environment',
            'Team comfortable with new technology',
            'Documentation updated and complete',
            'Monitoring and alerting configured',
            'Rollback procedures tested and verified'
        ]
    
    def _create_rollback_plan(self, original_tech: str, target_alternative: ModernAlternative) -> Dict[str, Any]:
        """Create rollback plan for migration"""
        return {
            'triggers': [
                'Critical performance issues',
                'Major compatibility problems',
                'Security vulnerabilities',
                'Timeline overruns > 50%'
            ],
            'procedures': [
                'Restore from backup systems',
                'Revert code changes',
                'Update configuration',
                'Verify system functionality',
                'Communicate with stakeholders'
            ],
            'estimated_time': '4-8 hours',
            'required_approvals': ['Technical Lead', 'Project Manager'],
            'testing_required': True
        }
    
    def generate_alternatives_report(self, suggestions: Dict[str, List[ModernAlternative]]) -> Dict[str, Any]:
        """Generate comprehensive alternatives report"""
        try:
            logger.info("Generating alternatives report")
            
            report = {
                'summary': {
                    'total_technologies': len(suggestions),
                    'alternatives_suggested': sum(len(alts) for alts in suggestions.values()),
                    'migration_efforts': {},
                    'estimated_duration': {}
                },
                'recommendations': [],
                'detailed_alternatives': {},
                'generated_at': datetime.now().isoformat()
            }
            
            # Analyze migration efforts
            efforts = {'low': 0, 'medium': 0, 'high': 0}
            durations = []
            
            for tech_key, alternatives in suggestions.items():
                best_alternative = alternatives[0] if alternatives else None
                if best_alternative:
                    efforts[best_alternative.migration_effort] += 1
                    durations.append(best_alternative.migration_time)
                    
                    # Add to detailed alternatives
                    report['detailed_alternatives'][tech_key] = [
                        self._alternative_to_dict(alt) for alt in alternatives
                    ]
                    
                    # Generate recommendation
                    recommendation = {
                        'technology': tech_key,
                        'recommended_alternative': best_alternative.name,
                        'priority': self._calculate_priority(best_alternative),
                        'justification': f"Best compatibility ({best_alternative.compatibility_score:.1%}) and {best_alternative.migration_effort} migration effort"
                    }
                    report['recommendations'].append(recommendation)
            
            report['summary']['migration_efforts'] = efforts
            report['summary']['typical_duration'] = self._calculate_typical_duration(durations)
            
            return report
            
        except Exception as e:
            logger.error(f"Error generating alternatives report: {e}")
            return {}
    
    def _alternative_to_dict(self, alternative: ModernAlternative) -> Dict[str, Any]:
        """Convert ModernAlternative to dictionary"""
        return {
            'name': alternative.name,
            'version': alternative.version,
            'category': alternative.category,
            'benefits': alternative.benefits,
            'migration_effort': alternative.migration_effort,
            'migration_time': alternative.migration_time,
            'compatibility_score': alternative.compatibility_score,
            'learning_curve': alternative.learning_curve,
            'community_support': alternative.community_support,
            'documentation_quality': alternative.documentation_quality,
            'cost_impact': alternative.cost_impact
        }
    
    def _calculate_priority(self, alternative: ModernAlternative) -> str:
        """Calculate priority for migration"""
        if alternative.migration_effort == 'low' and alternative.compatibility_score > 0.8:
            return 'high'
        elif alternative.migration_effort == 'medium' or alternative.compatibility_score > 0.6:
            return 'medium'
        else:
            return 'low'
    
    def _calculate_typical_duration(self, durations: List[str]) -> str:
        """Calculate typical migration duration"""
        if not durations:
            return 'Unknown'
        
        # Simple heuristic based on most common duration pattern
        duration_counts = {}
        for duration in durations:
            duration_counts[duration] = duration_counts.get(duration, 0) + 1
        
        most_common = max(duration_counts.items(), key=lambda x: x[1])
        return most_common[0]

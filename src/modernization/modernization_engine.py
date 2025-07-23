"""
Enhanced Technology Modernization Engine
Analyzes content for outdated technologies and provides modern alternatives with implementation roadmaps.
"""

import re
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import json

logger = logging.getLogger(__name__)

class TechnologyDatabase:
    """Database of technologies and their modern alternatives."""
    
    def __init__(self):
        self.technology_map = {
            # Programming Languages
            'java 8': {
                'category': 'programming_languages',
                'modern_alternatives': ['Java 17 LTS', 'Java 21 LTS'],
                'urgency': 'high',
                'end_of_life': '2030-12-31',
                'migration_effort': 'medium',
                'benefits': ['Improved performance', 'Better security', 'New language features', 'Records and Pattern Matching']
            },
            'python 2': {
                'category': 'programming_languages',
                'modern_alternatives': ['Python 3.11+', 'Python 3.12+'],
                'urgency': 'critical',
                'end_of_life': '2020-01-01',
                'migration_effort': 'high',
                'benefits': ['Security updates', 'Better Unicode support', 'Type hints', 'Performance improvements']
            },
            'angular 1': {
                'category': 'frontend_frameworks',
                'modern_alternatives': ['Angular 17+', 'React 18+', 'Vue 3+'],
                'urgency': 'high',
                'end_of_life': '2021-12-31',
                'migration_effort': 'high',
                'benefits': ['TypeScript support', 'Better performance', 'Modern tooling', 'Component-based architecture']
            },
            'php 5': {
                'category': 'programming_languages',
                'modern_alternatives': ['PHP 8.3+'],
                'urgency': 'critical',
                'end_of_life': '2018-12-31',
                'migration_effort': 'medium',
                'benefits': ['Performance improvements', 'Security updates', 'Modern syntax', 'JIT compilation']
            },
            
            # Databases
            'mysql 5.5': {
                'category': 'databases',
                'modern_alternatives': ['MySQL 8.0+', 'PostgreSQL 15+', 'MariaDB 10.11+'],
                'urgency': 'high',
                'end_of_life': '2018-12-31',
                'migration_effort': 'medium',
                'benefits': ['Better performance', 'JSON support', 'Enhanced security', 'Window functions']
            },
            'oracle 11g': {
                'category': 'databases',
                'modern_alternatives': ['Oracle 19c', 'Oracle 21c', 'PostgreSQL 15+'],
                'urgency': 'medium',
                'end_of_life': '2020-12-31',
                'migration_effort': 'high',
                'benefits': ['Cloud integration', 'In-memory processing', 'Advanced analytics', 'Autonomous features']
            },
            'sql server 2008': {
                'category': 'databases',
                'modern_alternatives': ['SQL Server 2022', 'Azure SQL Database'],
                'urgency': 'critical',
                'end_of_life': '2019-07-09',
                'migration_effort': 'medium',
                'benefits': ['Cloud integration', 'Enhanced security', 'Advanced analytics', 'Always Encrypted']
            },
            
            # Frameworks and Libraries
            'spring 3': {
                'category': 'backend_frameworks',
                'modern_alternatives': ['Spring Boot 3.x', 'Spring Framework 6.x'],
                'urgency': 'high',
                'end_of_life': '2016-12-31',
                'migration_effort': 'medium',
                'benefits': ['Reactive programming', 'Better cloud support', 'Native compilation', 'Improved testing']
            },
            'django 1.x': {
                'category': 'backend_frameworks',
                'modern_alternatives': ['Django 4.x', 'FastAPI', 'Flask 2.x'],
                'urgency': 'high',
                'end_of_life': '2018-04-01',
                'migration_effort': 'medium',
                'benefits': ['Async support', 'Better ORM', 'Enhanced security', 'Improved admin interface']
            },
            'react 15': {
                'category': 'frontend_frameworks',
                'modern_alternatives': ['React 18+'],
                'urgency': 'medium',
                'end_of_life': '2020-10-16',
                'migration_effort': 'medium',
                'benefits': ['Hooks', 'Concurrent features', 'Suspense', 'Better performance']
            },
            
            # Development Tools
            'jenkins 1.x': {
                'category': 'devops_tools',
                'modern_alternatives': ['Jenkins 2.x LTS', 'GitHub Actions', 'GitLab CI/CD', 'Azure DevOps'],
                'urgency': 'high',
                'end_of_life': '2017-04-20',
                'migration_effort': 'medium',
                'benefits': ['Pipeline as code', 'Better security', 'Cloud-native', 'Container support']
            },
            'maven 2': {
                'category': 'build_tools',
                'modern_alternatives': ['Maven 3.9+', 'Gradle 8+'],
                'urgency': 'medium',
                'end_of_life': '2014-02-18',
                'migration_effort': 'low',
                'benefits': ['Better dependency management', 'Parallel builds', 'Improved performance']
            },
            'ant': {
                'category': 'build_tools',
                'modern_alternatives': ['Maven 3.9+', 'Gradle 8+', 'SBT'],
                'urgency': 'medium',
                'end_of_life': 'n/a',
                'migration_effort': 'medium',
                'benefits': ['Declarative configuration', 'Better dependency management', 'IDE integration']
            },
            
            # Infrastructure
            'windows server 2008': {
                'category': 'operating_systems',
                'modern_alternatives': ['Windows Server 2022', 'Ubuntu Server 22.04 LTS', 'RHEL 9'],
                'urgency': 'critical',
                'end_of_life': '2020-01-14',
                'migration_effort': 'high',
                'benefits': ['Security updates', 'Container support', 'Cloud integration', 'Better performance']
            },
            'vmware vsphere 5': {
                'category': 'virtualization',
                'modern_alternatives': ['VMware vSphere 8', 'Kubernetes', 'Docker Swarm', 'AWS ECS'],
                'urgency': 'medium',
                'end_of_life': '2018-09-19',
                'migration_effort': 'high',
                'benefits': ['Container orchestration', 'Cloud-native', 'Better resource utilization', 'Microservices support']
            }
        }
        
        self.trend_data = {
            'cloud_native': {
                'technologies': ['Kubernetes', 'Docker', 'Serverless', 'Microservices'],
                'adoption_rate': 'high',
                'maturity': 'mature'
            },
            'ai_ml': {
                'technologies': ['TensorFlow', 'PyTorch', 'Scikit-learn', 'Hugging Face'],
                'adoption_rate': 'very_high',
                'maturity': 'mature'
            },
            'modern_web': {
                'technologies': ['React', 'Vue', 'Angular', 'TypeScript', 'Next.js'],
                'adoption_rate': 'high',
                'maturity': 'mature'
            },
            'devops': {
                'technologies': ['GitHub Actions', 'GitLab CI', 'Terraform', 'Ansible'],
                'adoption_rate': 'high',
                'maturity': 'mature'
            }
        }


class TrendAnalyzer:
    """Analyzes technology trends and adoption patterns."""
    
    def __init__(self):
        self.current_year = datetime.now().year
    
    def analyze_technology_trends(self, technologies: List[str]) -> Dict[str, Any]:
        """Analyze current trends for given technologies."""
        trend_analysis = {
            'trending_up': [],
            'stable': [],
            'declining': [],
            'emerging': [],
            'recommendations': []
        }
        
        # Trending technologies
        trending_technologies = [
            'kubernetes', 'docker', 'react', 'typescript', 'python',
            'terraform', 'aws', 'azure', 'serverless', 'graphql',
            'nextjs', 'tailwindcss', 'rust', 'go', 'postgresql'
        ]
        
        # Declining technologies
        declining_technologies = [
            'jquery', 'angular 1', 'php 5', 'java 8', 'python 2',
            'flash', 'silverlight', 'backbone.js', 'grunt', 'bower'
        ]
        
        for tech in technologies:
            tech_lower = tech.lower()
            
            if any(trending in tech_lower for trending in trending_technologies):
                trend_analysis['trending_up'].append({
                    'technology': tech,
                    'trend': 'increasing adoption',
                    'recommendation': 'Continue investment'
                })
            elif any(declining in tech_lower for declining in declining_technologies):
                trend_analysis['declining'].append({
                    'technology': tech,
                    'trend': 'decreasing adoption',
                    'recommendation': 'Plan migration'
                })
            else:
                trend_analysis['stable'].append({
                    'technology': tech,
                    'trend': 'stable',
                    'recommendation': 'Monitor for changes'
                })
        
        return trend_analysis


class ModernizationEngine:
    """Enhanced engine for analyzing and modernizing technology content."""
    
    def __init__(self):
        self.tech_database = TechnologyDatabase()
        self.trend_analyzer = TrendAnalyzer()
        self.current_date = datetime.now()
    
    def analyze_and_modernize_content(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Comprehensive analysis of content for modernization opportunities."""
        try:
            raw_text = content.get('raw_text', '')
            
            analysis = {
                'outdated_technologies': self._identify_outdated_tech(raw_text),
                'modernization_suggestions': [],
                'best_practices': self._generate_best_practices(raw_text),
                'implementation_guides': [],
                'trend_analysis': self._analyze_content_trends(raw_text),
                'risk_assessment': {},
                'modernization_roadmap': {},
                'cost_benefit_analysis': {}
            }
            
            # Generate modernization suggestions
            for tech in analysis['outdated_technologies']:
                suggestions = self._suggest_modern_alternatives(tech)
                analysis['modernization_suggestions'].extend(suggestions)
                
                # Generate implementation guide
                implementation_guide = self._generate_implementation_guide(tech, suggestions)
                analysis['implementation_guides'].append(implementation_guide)
            
            # Generate comprehensive roadmap
            analysis['modernization_roadmap'] = self.generate_modernization_roadmap(
                analysis['modernization_suggestions']
            )
            
            # Risk assessment
            analysis['risk_assessment'] = self._assess_modernization_risks(
                analysis['outdated_technologies']
            )
            
            # Cost-benefit analysis
            analysis['cost_benefit_analysis'] = self._perform_cost_benefit_analysis(
                analysis['modernization_suggestions']
            )
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error in modernization analysis: {str(e)}")
            return {'error': str(e), 'outdated_technologies': [], 'modernization_suggestions': []}
    
    def _identify_outdated_tech(self, text: str) -> List[Dict[str, Any]]:
        """Identify outdated technologies mentioned in content."""
        outdated_tech = []
        text_lower = text.lower()
        
        for tech_name, tech_info in self.tech_database.technology_map.items():
            # Create pattern variations for technology detection
            patterns = [
                re.escape(tech_name),
                re.escape(tech_name.replace(' ', '')),
                re.escape(tech_name.replace(' ', '-')),
                re.escape(tech_name.replace(' ', '_'))
            ]
            
            for pattern in patterns:
                if re.search(rf'\b{pattern}\b', text_lower):
                    context = self._extract_context(text, tech_name, 100)
                    
                    outdated_tech.append({
                        'technology': tech_name,
                        'category': tech_info['category'],
                        'found_context': context,
                        'modernization_urgency': tech_info['urgency'],
                        'end_of_life': tech_info['end_of_life'],
                        'migration_effort': tech_info['migration_effort'],
                        'modern_alternatives': tech_info['modern_alternatives'],
                        'benefits': tech_info['benefits']
                    })
                    break  # Avoid duplicates
        
        return outdated_tech
    
    def _extract_context(self, text: str, technology: str, context_length: int = 100) -> str:
        """Extract surrounding context for a technology mention."""
        text_lower = text.lower()
        tech_lower = technology.lower()
        
        # Find the position of the technology mention
        pos = text_lower.find(tech_lower)
        if pos == -1:
            return ""
        
        # Extract context around the mention
        start = max(0, pos - context_length)
        end = min(len(text), pos + len(technology) + context_length)
        
        context = text[start:end].strip()
        
        # Add ellipsis if we're not at the beginning/end
        if start > 0:
            context = "..." + context
        if end < len(text):
            context = context + "..."
        
        return context
    
    def _suggest_modern_alternatives(self, outdated_tech: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate detailed modernization suggestions."""
        suggestions = []
        tech_name = outdated_tech['technology']
        
        for alternative in outdated_tech['modern_alternatives']:
            suggestion = {
                'original_technology': tech_name,
                'modern_alternative': alternative,
                'category': outdated_tech['category'],
                'benefits': outdated_tech['benefits'],
                'migration_effort': outdated_tech['migration_effort'],
                'modernization_urgency': outdated_tech['modernization_urgency'],
                'implementation_timeline': self._estimate_implementation_timeline(
                    outdated_tech['migration_effort']
                ),
                'compatibility_notes': self._generate_compatibility_notes(tech_name, alternative),
                'learning_resources': self._suggest_learning_resources(alternative),
                'success_metrics': self._define_success_metrics(tech_name, alternative)
            }
            suggestions.append(suggestion)
        
        return suggestions
    
    def _estimate_implementation_timeline(self, migration_effort: str) -> Dict[str, Any]:
        """Estimate implementation timeline based on migration effort."""
        timelines = {
            'low': {'duration': '2-4 weeks', 'phases': 2, 'team_size': '1-2 developers'},
            'medium': {'duration': '2-3 months', 'phases': 3, 'team_size': '2-4 developers'},
            'high': {'duration': '4-6 months', 'phases': 4, 'team_size': '4-6 developers'},
            'critical': {'duration': '6-12 months', 'phases': 5, 'team_size': '6+ developers'}
        }
        
        return timelines.get(migration_effort, timelines['medium'])
    
    def _generate_compatibility_notes(self, old_tech: str, new_tech: str) -> List[str]:
        """Generate compatibility and migration notes."""
        compatibility_map = {
            ('java 8', 'Java 17 LTS'): [
                'Review deprecated APIs and replace with modern alternatives',
                'Update build tools to support Java 17',
                'Test all third-party libraries for compatibility',
                'Consider using jdeps tool to identify dependencies'
            ],
            ('python 2', 'Python 3.11+'): [
                'Use 2to3 tool for initial conversion',
                'Update print statements to print functions',
                'Handle Unicode strings properly',
                'Update exception handling syntax'
            ],
            ('angular 1', 'Angular 17+'): [
                'Complete rewrite required - no direct upgrade path',
                'Consider gradual migration with hybrid approach',
                'Rewrite components using modern Angular patterns',
                'Update to TypeScript for better type safety'
            ]
        }
        
        key = (old_tech, new_tech)
        return compatibility_map.get(key, [
            'Review breaking changes in documentation',
            'Create migration plan with testing phases',
            'Update dependencies and configurations',
            'Plan for team training and knowledge transfer'
        ])
    
    def _suggest_learning_resources(self, technology: str) -> List[Dict[str, str]]:
        """Suggest learning resources for new technology."""
        resource_map = {
            'Java 17 LTS': [
                {'type': 'documentation', 'title': 'Oracle Java 17 Documentation', 'url': 'https://docs.oracle.com/en/java/javase/17/'},
                {'type': 'course', 'title': 'Modern Java Development', 'url': 'https://www.pluralsight.com/courses/java-17-whats-new'},
                {'type': 'book', 'title': 'Modern Java in Action', 'url': 'https://www.manning.com/books/modern-java-in-action'}
            ],
            'Python 3.11+': [
                {'type': 'documentation', 'title': 'Python 3.11 Documentation', 'url': 'https://docs.python.org/3.11/'},
                {'type': 'guide', 'title': 'Python 2 to 3 Migration Guide', 'url': 'https://docs.python.org/3/howto/pyporting.html'},
                {'type': 'book', 'title': 'Effective Python', 'url': 'https://effectivepython.com/'}
            ]
        }
        
        return resource_map.get(technology, [
            {'type': 'documentation', 'title': f'{technology} Official Documentation', 'url': '#'},
            {'type': 'tutorial', 'title': f'Getting Started with {technology}', 'url': '#'},
            {'type': 'community', 'title': f'{technology} Community Forums', 'url': '#'}
        ])
    
    def _define_success_metrics(self, old_tech: str, new_tech: str) -> List[str]:
        """Define metrics to measure migration success."""
        return [
            'Performance improvement (response time, throughput)',
            'Security vulnerability reduction',
            'Development velocity increase',
            'Maintenance cost reduction',
            'Team satisfaction and productivity',
            'Code quality metrics (complexity, maintainability)',
            'System reliability and uptime',
            'Compliance and audit readiness'
        ]
    
    def generate_modernization_roadmap(self, suggestions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate comprehensive implementation roadmap."""
        if not suggestions:
            return {'phases': [], 'total_timeline': '0 weeks', 'total_effort': 'none'}
        
        # Group by urgency and effort
        phases = {
            'critical': [],
            'high': [],
            'medium': [],
            'low': []
        }
        
        for suggestion in suggestions:
            urgency = suggestion.get('modernization_urgency', 'medium')
            phases[urgency].append(suggestion)
        
        roadmap = {
            'phases': [],
            'total_timeline': '',
            'total_effort': '',
            'resource_requirements': {},
            'risk_mitigation': {},
            'success_criteria': []
        }
        
        phase_counter = 1
        total_weeks = 0
        
        for urgency, phase_suggestions in phases.items():
            if not phase_suggestions:
                continue
            
            phase_duration = self._calculate_phase_duration(phase_suggestions)
            total_weeks += phase_duration
            
            roadmap['phases'].append({
                'phase': f'Phase {phase_counter}',
                'priority': urgency.title(),
                'duration': f'{phase_duration} weeks',
                'technologies': [s['original_technology'] for s in phase_suggestions],
                'modern_alternatives': [s['modern_alternative'] for s in phase_suggestions],
                'deliverables': self._generate_phase_deliverables(phase_suggestions),
                'prerequisites': self._generate_phase_prerequisites(phase_suggestions),
                'risks': self._identify_phase_risks(phase_suggestions),
                'team_requirements': self._calculate_team_requirements(phase_suggestions)
            })
            
            phase_counter += 1
        
        roadmap['total_timeline'] = f'{total_weeks} weeks'
        roadmap['total_effort'] = self._categorize_total_effort(total_weeks)
        
        return roadmap
    
    def _calculate_phase_duration(self, suggestions: List[Dict[str, Any]]) -> int:
        """Calculate duration for a phase in weeks."""
        effort_map = {'low': 3, 'medium': 8, 'high': 16, 'critical': 24}
        
        max_effort = 0
        for suggestion in suggestions:
            effort = suggestion.get('migration_effort', 'medium')
            effort_weeks = effort_map.get(effort, 8)
            max_effort = max(max_effort, effort_weeks)
        
        return max_effort
    
    def _generate_phase_deliverables(self, suggestions: List[Dict[str, Any]]) -> List[str]:
        """Generate deliverables for a phase."""
        base_deliverables = [
            'Migration plan documentation',
            'Updated codebase with modern technology',
            'Comprehensive testing suite',
            'Deployment and rollback procedures',
            'Team training materials',
            'Performance benchmarks and metrics'
        ]
        
        return base_deliverables
    
    def _generate_phase_prerequisites(self, suggestions: List[Dict[str, Any]]) -> List[str]:
        """Generate prerequisites for a phase."""
        return [
            'Stakeholder approval and budget allocation',
            'Development environment setup',
            'Team training and knowledge transfer',
            'Backup and rollback strategies',
            'Testing infrastructure preparation'
        ]
    
    def _identify_phase_risks(self, suggestions: List[Dict[str, Any]]) -> List[str]:
        """Identify risks for a phase."""
        return [
            'Compatibility issues with existing systems',
            'Data migration challenges',
            'Team learning curve and productivity impact',
            'Third-party dependency conflicts',
            'Unexpected technical debt discovery'
        ]
    
    def _calculate_team_requirements(self, suggestions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate team requirements for a phase."""
        effort_levels = [s.get('migration_effort', 'medium') for s in suggestions]
        max_effort = max(effort_levels) if effort_levels else 'medium'
        
        team_map = {
            'low': {'developers': '1-2', 'architect': 'part-time', 'qa': '1'},
            'medium': {'developers': '2-4', 'architect': 'part-time', 'qa': '1-2'},
            'high': {'developers': '4-6', 'architect': 'full-time', 'qa': '2-3'},
            'critical': {'developers': '6+', 'architect': 'full-time', 'qa': '3+'}
        }
        
        return team_map.get(max_effort, team_map['medium'])
    
    def _categorize_total_effort(self, total_weeks: int) -> str:
        """Categorize total effort based on duration."""
        if total_weeks <= 4:
            return 'Small'
        elif total_weeks <= 12:
            return 'Medium'
        elif total_weeks <= 24:
            return 'Large'
        else:
            return 'Enterprise'

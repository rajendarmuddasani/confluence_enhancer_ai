"""
Current best practices database
"""
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class BestPractice:
    """Best practice recommendation"""
    id: str
    title: str
    category: str
    description: str
    technology: str
    implementation_steps: List[str]
    benefits: List[str]
    difficulty_level: str  # 'beginner', 'intermediate', 'advanced'
    time_to_implement: str
    resources: List[Dict[str, str]]
    last_updated: str


@dataclass
class PracticeCategory:
    """Category of best practices"""
    name: str
    description: str
    practices: List[BestPractice]
    priority_level: str


class BestPracticesDatabase:
    """Database of current technology best practices"""
    
    def __init__(self):
        self.practices_db = self._load_best_practices()
        self.categories = self._organize_by_category()
        
    def _load_best_practices(self) -> Dict[str, BestPractice]:
        """Load comprehensive best practices database"""
        practices = {}
        
        # Python Best Practices
        practices['python_virtual_env'] = BestPractice(
            id='python_virtual_env',
            title='Use Virtual Environments',
            category='python_development',
            description='Isolate project dependencies using virtual environments to prevent conflicts and ensure reproducible builds.',
            technology='Python',
            implementation_steps=[
                'Install virtualenv or use built-in venv module',
                'Create virtual environment: python -m venv venv',
                'Activate environment: source venv/bin/activate (Linux/Mac) or venv\\Scripts\\activate (Windows)',
                'Install dependencies: pip install -r requirements.txt',
                'Deactivate when done: deactivate'
            ],
            benefits=[
                'Prevents dependency conflicts between projects',
                'Ensures consistent environments across team',
                'Easier deployment and reproducibility',
                'Cleaner system Python installation'
            ],
            difficulty_level='beginner',
            time_to_implement='15-30 minutes',
            resources=[
                {'type': 'documentation', 'url': 'https://docs.python.org/3/tutorial/venv.html'},
                {'type': 'tutorial', 'url': 'https://realpython.com/python-virtual-environments-a-primer/'}
            ],
            last_updated='2025-01-01'
        )
        
        practices['python_type_hints'] = BestPractice(
            id='python_type_hints',
            title='Use Type Hints',
            category='python_development',
            description='Add type annotations to improve code readability, catch errors early, and enable better IDE support.',
            technology='Python',
            implementation_steps=[
                'Import typing module for complex types',
                'Add type hints to function parameters and return values',
                'Use generic types for collections (List, Dict, etc.)',
                'Install and configure mypy for static type checking',
                'Gradually add types to existing codebase'
            ],
            benefits=[
                'Better IDE support and autocompletion',
                'Catch type-related bugs before runtime',
                'Improved code documentation',
                'Easier refactoring and maintenance'
            ],
            difficulty_level='intermediate',
            time_to_implement='1-2 hours per module',
            resources=[
                {'type': 'documentation', 'url': 'https://docs.python.org/3/library/typing.html'},
                {'type': 'tool', 'url': 'https://mypy.readthedocs.io/'}
            ],
            last_updated='2025-01-01'
        )
        
        # JavaScript/TypeScript Best Practices
        practices['js_use_typescript'] = BestPractice(
            id='js_use_typescript',
            title='Adopt TypeScript',
            category='javascript_development',
            description='Use TypeScript for large-scale JavaScript applications to add static typing and improve maintainability.',
            technology='JavaScript/TypeScript',
            implementation_steps=[
                'Install TypeScript: npm install -D typescript',
                'Create tsconfig.json configuration file',
                'Rename .js files to .ts/.tsx gradually',
                'Add type definitions for dependencies',
                'Configure build tools (webpack, vite, etc.) for TypeScript'
            ],
            benefits=[
                'Static type checking catches errors early',
                'Better IDE support and refactoring',
                'Improved code documentation',
                'Easier team collaboration on large codebases'
            ],
            difficulty_level='intermediate',
            time_to_implement='1-2 weeks for existing project',
            resources=[
                {'type': 'documentation', 'url': 'https://www.typescriptlang.org/docs/'},
                {'type': 'migration_guide', 'url': 'https://www.typescriptlang.org/docs/handbook/migrating-from-javascript.html'}
            ],
            last_updated='2025-01-01'
        )
        
        practices['js_modern_es6'] = BestPractice(
            id='js_modern_es6',
            title='Use Modern ES6+ Features',
            category='javascript_development',
            description='Leverage modern JavaScript features like arrow functions, destructuring, modules, and async/await.',
            technology='JavaScript',
            implementation_steps=[
                'Replace var with const/let for block scoping',
                'Use arrow functions for concise syntax',
                'Implement destructuring for objects and arrays',
                'Use template literals instead of string concatenation',
                'Replace Promise chains with async/await'
            ],
            benefits=[
                'More readable and concise code',
                'Better error handling with async/await',
                'Improved performance with block scoping',
                'Modern development patterns'
            ],
            difficulty_level='beginner',
            time_to_implement='2-4 hours',
            resources=[
                {'type': 'guide', 'url': 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide'},
                {'type': 'tutorial', 'url': 'https://javascript.info/'}
            ],
            last_updated='2025-01-01'
        )
        
        # React Best Practices
        practices['react_hooks'] = BestPractice(
            id='react_hooks',
            title='Use React Hooks',
            category='react_development',
            description='Replace class components with functional components and hooks for simpler, more reusable code.',
            technology='React',
            implementation_steps=[
                'Convert class components to functional components',
                'Replace componentDidMount with useEffect',
                'Use useState for component state management',
                'Create custom hooks for reusable logic',
                'Follow hooks rules (call at top level, only in React functions)'
            ],
            benefits=[
                'Simpler component logic',
                'Better code reuse with custom hooks',
                'Easier testing and debugging',
                'Better performance with React optimizations'
            ],
            difficulty_level='intermediate',
            time_to_implement='1-2 days per component',
            resources=[
                {'type': 'documentation', 'url': 'https://reactjs.org/docs/hooks-intro.html'},
                {'type': 'migration_guide', 'url': 'https://reactjs.org/docs/hooks-faq.html'}
            ],
            last_updated='2025-01-01'
        )
        
        # Database Best Practices
        practices['db_indexing'] = BestPractice(
            id='db_indexing',
            title='Proper Database Indexing',
            category='database_optimization',
            description='Create appropriate indexes to improve query performance while balancing storage and write performance.',
            technology='SQL Databases',
            implementation_steps=[
                'Analyze query patterns and slow queries',
                'Create indexes on frequently queried columns',
                'Use composite indexes for multi-column queries',
                'Monitor index usage and performance impact',
                'Remove unused indexes to improve write performance'
            ],
            benefits=[
                'Significantly faster query performance',
                'Better user experience with responsive applications',
                'Reduced server load and resource usage',
                'Improved scalability'
            ],
            difficulty_level='intermediate',
            time_to_implement='1-3 days',
            resources=[
                {'type': 'guide', 'url': 'https://use-the-index-luke.com/'},
                {'type': 'documentation', 'url': 'https://dev.mysql.com/doc/refman/8.0/en/optimization-indexes.html'}
            ],
            last_updated='2025-01-01'
        )
        
        # Security Best Practices
        practices['security_input_validation'] = BestPractice(
            id='security_input_validation',
            title='Input Validation and Sanitization',
            category='security',
            description='Validate and sanitize all user inputs to prevent injection attacks and ensure data integrity.',
            technology='All Web Technologies',
            implementation_steps=[
                'Implement server-side validation for all inputs',
                'Use parameterized queries to prevent SQL injection',
                'Sanitize HTML content to prevent XSS attacks',
                'Validate file uploads and restrict file types',
                'Implement rate limiting to prevent abuse'
            ],
            benefits=[
                'Protection against injection attacks',
                'Improved data quality and consistency',
                'Better user experience with clear error messages',
                'Compliance with security standards'
            ],
            difficulty_level='intermediate',
            time_to_implement='1-2 weeks',
            resources=[
                {'type': 'guide', 'url': 'https://owasp.org/www-project-top-ten/'},
                {'type': 'checklist', 'url': 'https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html'}
            ],
            last_updated='2025-01-01'
        )
        
        # DevOps Best Practices
        practices['ci_cd_pipeline'] = BestPractice(
            id='ci_cd_pipeline',
            title='Implement CI/CD Pipelines',
            category='devops',
            description='Automate build, test, and deployment processes to improve reliability and reduce manual errors.',
            technology='DevOps Tools',
            implementation_steps=[
                'Choose CI/CD platform (GitHub Actions, GitLab CI, Jenkins)',
                'Set up automated testing on every commit',
                'Implement automated security scanning',
                'Configure deployment to staging and production',
                'Add monitoring and rollback capabilities'
            ],
            benefits=[
                'Faster and more reliable deployments',
                'Early detection of bugs and issues',
                'Consistent deployment process',
                'Reduced manual effort and human errors'
            ],
            difficulty_level='intermediate',
            time_to_implement='1-2 weeks',
            resources=[
                {'type': 'guide', 'url': 'https://docs.github.com/en/actions'},
                {'type': 'tutorial', 'url': 'https://www.atlassian.com/continuous-delivery/principles/continuous-integration-vs-delivery-vs-deployment'}
            ],
            last_updated='2025-01-01'
        )
        
        practices['containerization'] = BestPractice(
            id='containerization',
            title='Use Docker for Containerization',
            category='devops',
            description='Package applications with their dependencies in containers for consistent deployment across environments.',
            technology='Docker',
            implementation_steps=[
                'Create Dockerfile for application',
                'Use multi-stage builds to optimize image size',
                'Configure docker-compose for local development',
                'Implement health checks and proper logging',
                'Use .dockerignore to exclude unnecessary files'
            ],
            benefits=[
                'Consistent environment across development, staging, and production',
                'Easier scaling and orchestration',
                'Simplified dependency management',
                'Better resource utilization'
            ],
            difficulty_level='intermediate',
            time_to_implement='3-5 days',
            resources=[
                {'type': 'documentation', 'url': 'https://docs.docker.com/get-started/'},
                {'type': 'best_practices', 'url': 'https://docs.docker.com/develop/dev-best-practices/'}
            ],
            last_updated='2025-01-01'
        )
        
        # Performance Best Practices
        practices['web_performance'] = BestPractice(
            id='web_performance',
            title='Web Performance Optimization',
            category='performance',
            description='Optimize web applications for faster loading times and better user experience.',
            technology='Web Applications',
            implementation_steps=[
                'Implement code splitting and lazy loading',
                'Optimize images (WebP format, proper sizing)',
                'Use CDN for static assets',
                'Implement caching strategies (browser, server)',
                'Minimize and compress CSS/JavaScript'
            ],
            benefits=[
                'Faster page load times',
                'Better user experience and engagement',
                'Improved SEO rankings',
                'Reduced bandwidth and server costs'
            ],
            difficulty_level='intermediate',
            time_to_implement='1-2 weeks',
            resources=[
                {'type': 'guide', 'url': 'https://web.dev/performance/'},
                {'type': 'tool', 'url': 'https://developers.google.com/speed/pagespeed/insights/'}
            ],
            last_updated='2025-01-01'
        )
        
        # Testing Best Practices
        practices['automated_testing'] = BestPractice(
            id='automated_testing',
            title='Comprehensive Automated Testing',
            category='testing',
            description='Implement a comprehensive testing strategy with unit, integration, and end-to-end tests.',
            technology='All Development',
            implementation_steps=[
                'Set up unit testing framework (Jest, pytest, JUnit)',
                'Write tests for core business logic',
                'Implement integration tests for API endpoints',
                'Add end-to-end tests for critical user flows',
                'Set up test coverage reporting and thresholds'
            ],
            benefits=[
                'Early detection of bugs and regressions',
                'Confidence in code changes and refactoring',
                'Better code design and architecture',
                'Reduced manual testing effort'
            ],
            difficulty_level='intermediate',
            time_to_implement='2-4 weeks',
            resources=[
                {'type': 'guide', 'url': 'https://testing-library.com/docs/guiding-principles'},
                {'type': 'framework', 'url': 'https://jestjs.io/docs/getting-started'}
            ],
            last_updated='2025-01-01'
        )
        
        return practices
    
    def _organize_by_category(self) -> Dict[str, PracticeCategory]:
        """Organize practices by category"""
        categories = {}
        
        for practice in self.practices_db.values():
            category_name = practice.category
            
            if category_name not in categories:
                categories[category_name] = PracticeCategory(
                    name=category_name,
                    description=self._get_category_description(category_name),
                    practices=[],
                    priority_level=self._get_category_priority(category_name)
                )
            
            categories[category_name].practices.append(practice)
        
        return categories
    
    def _get_category_description(self, category: str) -> str:
        """Get description for practice category"""
        descriptions = {
            'python_development': 'Best practices for Python development and project structure',
            'javascript_development': 'Modern JavaScript and TypeScript development practices',
            'react_development': 'React-specific best practices and patterns',
            'database_optimization': 'Database design and performance optimization practices',
            'security': 'Security best practices for web applications',
            'devops': 'DevOps and deployment automation practices',
            'performance': 'Application and web performance optimization',
            'testing': 'Testing strategies and automation best practices'
        }
        return descriptions.get(category, f'Best practices for {category}')
    
    def _get_category_priority(self, category: str) -> str:
        """Get priority level for practice category"""
        priorities = {
            'security': 'critical',
            'testing': 'high',
            'devops': 'high',
            'performance': 'medium',
            'python_development': 'medium',
            'javascript_development': 'medium',
            'react_development': 'medium',
            'database_optimization': 'medium'
        }
        return priorities.get(category, 'medium')
    
    def get_practices_for_technology(self, technology: str) -> List[BestPractice]:
        """Get best practices for specific technology"""
        try:
            tech_lower = technology.lower()
            matching_practices = []
            
            for practice in self.practices_db.values():
                practice_tech = practice.technology.lower()
                
                if (tech_lower in practice_tech or 
                    practice_tech in tech_lower or
                    self._is_related_technology(tech_lower, practice_tech)):
                    matching_practices.append(practice)
            
            return matching_practices
            
        except Exception as e:
            logger.error(f"Error getting practices for technology {technology}: {e}")
            return []
    
    def _is_related_technology(self, target_tech: str, practice_tech: str) -> bool:
        """Check if technologies are related"""
        related_groups = [
            ['python', 'django', 'flask', 'fastapi'],
            ['javascript', 'typescript', 'node.js', 'react', 'angular', 'vue'],
            ['java', 'spring', 'kotlin'],
            ['mysql', 'postgresql', 'sql', 'database'],
            ['docker', 'kubernetes', 'devops'],
            ['html', 'css', 'web', 'frontend']
        ]
        
        for group in related_groups:
            if any(tech in target_tech for tech in group) and any(tech in practice_tech for tech in group):
                return True
        
        return False
    
    def get_practices_by_difficulty(self, difficulty: str) -> List[BestPractice]:
        """Get practices filtered by difficulty level"""
        return [practice for practice in self.practices_db.values() 
                if practice.difficulty_level == difficulty]
    
    def get_quick_wins(self) -> List[BestPractice]:
        """Get practices that are easy to implement with high impact"""
        quick_wins = []
        
        for practice in self.practices_db.values():
            # Quick wins are beginner level with short implementation time
            if (practice.difficulty_level == 'beginner' and 
                ('minutes' in practice.time_to_implement or 
                 'hour' in practice.time_to_implement)):
                quick_wins.append(practice)
        
        return quick_wins
    
    def get_security_practices(self) -> List[BestPractice]:
        """Get all security-related practices"""
        return [practice for practice in self.practices_db.values() 
                if practice.category == 'security' or 'security' in practice.title.lower()]
    
    def get_modernization_practices(self, legacy_tech: str) -> List[BestPractice]:
        """Get practices relevant for modernizing legacy technology"""
        modern_practices = []
        legacy_lower = legacy_tech.lower()
        
        # Map legacy technologies to relevant modern practices
        legacy_mappings = {
            'python_2': ['python_virtual_env', 'python_type_hints'],
            'java_8': ['automated_testing', 'ci_cd_pipeline'],
            'jquery': ['js_use_typescript', 'js_modern_es6'],
            'angular_1': ['react_hooks', 'js_use_typescript'],
            'mysql_5_5': ['db_indexing'],
            'oracle_11g': ['db_indexing', 'containerization']
        }
        
        # Get specific practices for legacy technology
        for legacy_key, practice_ids in legacy_mappings.items():
            if legacy_key in legacy_lower:
                for practice_id in practice_ids:
                    if practice_id in self.practices_db:
                        modern_practices.append(self.practices_db[practice_id])
        
        # Add general modernization practices
        general_modern_practices = [
            'ci_cd_pipeline',
            'containerization',
            'automated_testing',
            'security_input_validation'
        ]
        
        for practice_id in general_modern_practices:
            if practice_id in self.practices_db:
                practice = self.practices_db[practice_id]
                if practice not in modern_practices:
                    modern_practices.append(practice)
        
        return modern_practices
    
    def search_practices(self, query: str) -> List[BestPractice]:
        """Search practices by title, description, or technology"""
        query_lower = query.lower()
        matching_practices = []
        
        for practice in self.practices_db.values():
            if (query_lower in practice.title.lower() or
                query_lower in practice.description.lower() or
                query_lower in practice.technology.lower() or
                any(query_lower in step.lower() for step in practice.implementation_steps)):
                matching_practices.append(practice)
        
        return matching_practices
    
    def generate_practices_report(self, technology_list: List[str]) -> Dict[str, Any]:
        """Generate comprehensive best practices report"""
        try:
            logger.info(f"Generating practices report for {len(technology_list)} technologies")
            
            report = {
                'summary': {
                    'total_technologies': len(technology_list),
                    'applicable_practices': 0,
                    'quick_wins': 0,
                    'security_practices': 0,
                    'categories_covered': set()
                },
                'by_technology': {},
                'quick_wins': [],
                'security_recommendations': [],
                'implementation_roadmap': [],
                'generated_at': datetime.now().isoformat()
            }
            
            all_practices = []
            
            # Get practices for each technology
            for tech in technology_list:
                tech_practices = self.get_practices_for_technology(tech)
                report['by_technology'][tech] = [
                    self._practice_to_dict(practice) for practice in tech_practices
                ]
                all_practices.extend(tech_practices)
                
                for practice in tech_practices:
                    report['summary']['categories_covered'].add(practice.category)
            
            # Remove duplicates
            unique_practices = list({p.id: p for p in all_practices}.values())
            
            # Update summary
            report['summary']['applicable_practices'] = len(unique_practices)
            report['summary']['categories_covered'] = list(report['summary']['categories_covered'])
            
            # Get quick wins
            quick_wins = [p for p in unique_practices if p.difficulty_level == 'beginner']
            report['quick_wins'] = [self._practice_to_dict(p) for p in quick_wins]
            report['summary']['quick_wins'] = len(quick_wins)
            
            # Get security practices
            security_practices = [p for p in unique_practices if p.category == 'security']
            report['security_recommendations'] = [self._practice_to_dict(p) for p in security_practices]
            report['summary']['security_practices'] = len(security_practices)
            
            # Create implementation roadmap
            report['implementation_roadmap'] = self._create_implementation_roadmap(unique_practices)
            
            return report
            
        except Exception as e:
            logger.error(f"Error generating practices report: {e}")
            return {}
    
    def _practice_to_dict(self, practice: BestPractice) -> Dict[str, Any]:
        """Convert BestPractice to dictionary"""
        return {
            'id': practice.id,
            'title': practice.title,
            'category': practice.category,
            'description': practice.description,
            'technology': practice.technology,
            'implementation_steps': practice.implementation_steps,
            'benefits': practice.benefits,
            'difficulty_level': practice.difficulty_level,
            'time_to_implement': practice.time_to_implement,
            'resources': practice.resources,
            'last_updated': practice.last_updated
        }
    
    def _create_implementation_roadmap(self, practices: List[BestPractice]) -> List[Dict[str, Any]]:
        """Create implementation roadmap based on difficulty and dependencies"""
        roadmap = []
        
        # Phase 1: Quick wins (beginner level)
        phase1_practices = [p for p in practices if p.difficulty_level == 'beginner']
        if phase1_practices:
            roadmap.append({
                'phase': 'Phase 1: Quick Wins',
                'duration': '1-2 weeks',
                'description': 'Easy to implement practices with immediate benefits',
                'practices': [p.title for p in phase1_practices],
                'total_practices': len(phase1_practices)
            })
        
        # Phase 2: Foundation (intermediate level, non-security)
        phase2_practices = [p for p in practices 
                           if p.difficulty_level == 'intermediate' and p.category != 'security']
        if phase2_practices:
            roadmap.append({
                'phase': 'Phase 2: Foundation',
                'duration': '2-4 weeks',
                'description': 'Core practices for better development workflow',
                'practices': [p.title for p in phase2_practices],
                'total_practices': len(phase2_practices)
            })
        
        # Phase 3: Security (all security practices)
        security_practices = [p for p in practices if p.category == 'security']
        if security_practices:
            roadmap.append({
                'phase': 'Phase 3: Security',
                'duration': '1-3 weeks',
                'description': 'Critical security practices and hardening',
                'practices': [p.title for p in security_practices],
                'total_practices': len(security_practices)
            })
        
        # Phase 4: Advanced (advanced level)
        phase4_practices = [p for p in practices if p.difficulty_level == 'advanced']
        if phase4_practices:
            roadmap.append({
                'phase': 'Phase 4: Advanced',
                'duration': '3-6 weeks',
                'description': 'Advanced practices for optimization and scaling',
                'practices': [p.title for p in phase4_practices],
                'total_practices': len(phase4_practices)
            })
        
        return roadmap

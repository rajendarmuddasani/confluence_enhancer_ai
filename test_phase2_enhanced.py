#!/usr/bin/env python3
"""
Test script for Phase 2 Enhanced Analysis System
Tests all enhanced components and their integration
"""

import asyncio
import json
import logging
import sys
from pathlib import Path
from typing import Dict, Any

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

from src.processors.data_extractor_simple import DataExtractor
from src.processors.concept_processor_simple import ConceptProcessor
from src.visualizations.dashboard_generator_clean import DashboardGenerator
from src.modernization.modernization_engine_simple import ModernizationEngine

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class Phase2TestSuite:
    """Comprehensive test suite for Phase 2 enhanced analysis system"""
    
    def __init__(self):
        self.test_results = {}
        
    def create_sample_confluence_content(self) -> str:
        """Create sample HTML content for testing"""
        return """
        <html>
        <body>
            <h1>Enterprise System Architecture Overview</h1>
            
            <h2>Current Technology Stack</h2>
            <p>Our system currently uses the following technologies:</p>
            <ul>
                <li>Java 8 for backend services</li>
                <li>JSF for web framework</li>
                <li>Oracle Database 11g</li>
                <li>Apache Tomcat 7</li>
                <li>Struts 1.3 for web layer</li>
                <li>jQuery 1.8 for frontend</li>
            </ul>
            
            <h2>Performance Metrics</h2>
            <table border="1">
                <tr>
                    <th>Service</th>
                    <th>Response Time (ms)</th>
                    <th>Throughput (req/sec)</th>
                    <th>Error Rate (%)</th>
                    <th>Availability (%)</th>
                </tr>
                <tr>
                    <td>User Service</td>
                    <td>250</td>
                    <td>1200</td>
                    <td>0.5</td>
                    <td>99.9</td>
                </tr>
                <tr>
                    <td>Payment Service</td>
                    <td>180</td>
                    <td>800</td>
                    <td>0.2</td>
                    <td>99.99</td>
                </tr>
                <tr>
                    <td>Inventory Service</td>
                    <td>320</td>
                    <td>600</td>
                    <td>1.2</td>
                    <td>99.5</td>
                </tr>
                <tr>
                    <td>Notification Service</td>
                    <td>150</td>
                    <td>2000</td>
                    <td>0.8</td>
                    <td>99.8</td>
                </tr>
            </table>
            
            <h2>Deployment Process</h2>
            <p>Our current deployment process follows these steps:</p>
            <ol>
                <li>Developer commits code to Git repository</li>
                <li>Jenkins builds the application automatically</li>
                <li>QA team performs manual testing</li>
                <li>Operations team deploys to staging environment</li>
                <li>UAT testing is conducted</li>
                <li>Manual deployment to production</li>
                <li>Post-deployment verification</li>
            </ol>
            
            <h2>Integration Architecture</h2>
            <p>The system integrates with multiple external services through various protocols:</p>
            <ul>
                <li>SOAP web services for legacy systems</li>
                <li>REST APIs for modern integrations</li>
                <li>Message queues for asynchronous processing</li>
                <li>File-based data exchange</li>
                <li>Database direct connections</li>
            </ul>
            
            <h2>Security Framework</h2>
            <p>Current security measures include:</p>
            <ul>
                <li>LDAP authentication</li>
                <li>Role-based access control</li>
                <li>SSL/TLS encryption</li>
                <li>Input validation</li>
                <li>SQL injection prevention</li>
            </ul>
            
            <h2>Data Flow</h2>
            <p>Data flows through the system in the following pattern:</p>
            <p>User Request → Load Balancer → Web Server → Application Server → Database → Cache Layer → Response</p>
        </body>
        </html>
        """
    
    async def test_data_extractor(self) -> Dict[str, Any]:
        """Test the enhanced data extractor"""
        logger.info("Testing Data Extractor...")
        
        try:
            extractor = DataExtractor()
            sample_content = self.create_sample_confluence_content()
            
            # Test table extraction and analysis
            tables = await extractor.extract_tables(sample_content)
            logger.info(f"Extracted {len(tables)} tables")
            
            if tables:
                # Test data analysis
                analysis = await extractor.analyze_data_structure(tables[0])
                logger.info(f"Table analysis completed: {analysis['data_quality']}")
                
                # Test visualization suggestions
                viz_suggestions = await extractor.suggest_visualizations(tables[0])
                logger.info(f"Generated {len(viz_suggestions)} visualization suggestions")
                
                return {
                    "status": "success",
                    "tables_extracted": len(tables),
                    "data_quality": analysis.get('data_quality', 'unknown'),
                    "visualization_suggestions": len(viz_suggestions),
                    "sample_analysis": analysis
                }
            else:
                return {"status": "warning", "message": "No tables found"}
                
        except Exception as e:
            logger.error(f"Data extractor test failed: {e}")
            return {"status": "error", "error": str(e)}
    
    async def test_concept_processor(self) -> Dict[str, Any]:
        """Test the enhanced concept processor"""
        logger.info("Testing Concept Processor...")
        
        try:
            processor = ConceptProcessor()
            sample_content = self.create_sample_confluence_content()
            
            # Test concept identification
            concepts = await processor.identify_concepts(sample_content)
            logger.info(f"Identified {len(concepts)} concepts")
            
            # Test diagram generation
            diagrams = []
            for concept in concepts[:3]:  # Test first 3 concepts
                diagram = await processor.generate_diagram(concept)
                if diagram:
                    diagrams.append(diagram)
            
            logger.info(f"Generated {len(diagrams)} diagrams")
            
            return {
                "status": "success",
                "concepts_identified": len(concepts),
                "diagrams_generated": len(diagrams),
                "concept_types": list(set(c.get('type', 'unknown') for c in concepts)),
                "sample_concepts": concepts[:3]
            }
            
        except Exception as e:
            logger.error(f"Concept processor test failed: {e}")
            return {"status": "error", "error": str(e)}
    
    async def test_dashboard_generator(self) -> Dict[str, Any]:
        """Test the enhanced dashboard generator"""
        logger.info("Testing Dashboard Generator...")
        
        try:
            generator = DashboardGenerator()
            
            # Create sample data
            sample_data = {
                'Service': ['User Service', 'Payment Service', 'Inventory Service', 'Notification Service'],
                'Response Time (ms)': [250, 180, 320, 150],
                'Throughput (req/sec)': [1200, 800, 600, 2000],
                'Error Rate (%)': [0.5, 0.2, 1.2, 0.8],
                'Availability (%)': [99.9, 99.99, 99.5, 99.8]
            }
            
            # Test dashboard creation
            sample_suggestions = [
                {'type': 'bar', 'title': 'Service Performance', 'x_column': 'Service', 'y_column': 'Response Time (ms)'},
                {'type': 'line', 'title': 'Throughput Trend', 'x_column': 'Service', 'y_column': 'Throughput (req/sec)'}
            ]
            
            dashboard = await generator.create_interactive_dashboard(
                table_data={'data': sample_data, 'title': 'Service Performance Dashboard'},
                suggestions=sample_suggestions
            )
            
            logger.info("Dashboard generated successfully")
            
            # Test chart generation (dashboard contains charts)
            charts = dashboard.get('charts', []) if dashboard else []
            logger.info(f"Generated {len(charts)} charts")
            
            return {
                "status": "success",
                "dashboard_created": bool(dashboard),
                "charts_generated": len(charts),
                "dashboard_title": dashboard.get('title') if dashboard else None,
                "chart_types": [chart.get('type') for chart in charts] if charts else []
            }
            
        except Exception as e:
            logger.error(f"Dashboard generator test failed: {e}")
            return {"status": "error", "error": str(e)}
    
    async def test_modernization_engine(self) -> Dict[str, Any]:
        """Test the modernization engine"""
        logger.info("Testing Modernization Engine...")
        
        try:
            engine = ModernizationEngine()
            sample_content = self.create_sample_confluence_content()
            
            # Test technology detection
            technologies = await engine.detect_technologies(sample_content)
            logger.info(f"Detected {len(technologies)} technologies")
            
            # Test modernization analysis
            analysis = await engine.analyze_modernization_needs(technologies)
            logger.info("Modernization analysis completed")
            
            # Test roadmap generation
            roadmap = await engine.generate_implementation_roadmap(analysis)
            logger.info("Implementation roadmap generated")
            
            return {
                "status": "success",
                "technologies_detected": len(technologies),
                "outdated_technologies": len([t for t in technologies if t.get('status') == 'outdated']),
                "modernization_suggestions": len(analysis.get('suggestions', [])),
                "roadmap_phases": len(roadmap.get('phases', [])) if roadmap else 0,
                "sample_technologies": technologies[:5]
            }
            
        except Exception as e:
            logger.error(f"Modernization engine test failed: {e}")
            return {"status": "error", "error": str(e)}
    
    async def test_integration(self) -> Dict[str, Any]:
        """Test integration between all components"""
        logger.info("Testing System Integration...")
        
        try:
            sample_content = self.create_sample_confluence_content()
            
            # Initialize all components
            data_extractor = DataExtractor()
            concept_processor = ConceptProcessor()
            dashboard_generator = DashboardGenerator()
            modernization_engine = ModernizationEngine()
            
            # Run integrated analysis
            tables = await data_extractor.extract_tables(sample_content)
            concepts = await concept_processor.identify_concepts(sample_content)
            technologies = await modernization_engine.detect_technologies(sample_content)
            
            # Generate outputs from all components
            integration_results = {
                "tables_found": len(tables),
                "concepts_identified": len(concepts),
                "technologies_detected": len(technologies),
                "status": "success"
            }
            
            # Test cross-component functionality
            if tables:
                table_data = tables[0]
                sample_suggestions = [
                    {'type': 'bar', 'title': 'Data Overview'}
                ]
                dashboard = await dashboard_generator.create_interactive_dashboard(
                    table_data=table_data,
                    suggestions=sample_suggestions
                )
                integration_results["dashboard_generated"] = bool(dashboard)
            
            logger.info("Integration test completed successfully")
            return integration_results
            
        except Exception as e:
            logger.error(f"Integration test failed: {e}")
            return {"status": "error", "error": str(e)}
    
    async def run_all_tests(self) -> Dict[str, Any]:
        """Run all Phase 2 tests"""
        logger.info("Starting Phase 2 Enhanced Analysis System Tests...")
        
        # Run individual component tests
        self.test_results["data_extractor"] = await self.test_data_extractor()
        self.test_results["concept_processor"] = await self.test_concept_processor()
        self.test_results["dashboard_generator"] = await self.test_dashboard_generator()
        self.test_results["modernization_engine"] = await self.test_modernization_engine()
        
        # Run integration test
        self.test_results["integration"] = await self.test_integration()
        
        # Generate summary
        passed_tests = sum(1 for result in self.test_results.values() 
                          if result.get("status") == "success")
        total_tests = len(self.test_results)
        
        summary = {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "success_rate": f"{(passed_tests/total_tests)*100:.1f}%",
            "overall_status": "PASS" if passed_tests == total_tests else "PARTIAL",
            "detailed_results": self.test_results
        }
        
        logger.info(f"Phase 2 Testing Complete: {summary['success_rate']} success rate")
        return summary

def print_test_results(results: Dict[str, Any]):
    """Print formatted test results"""
    print("\n" + "="*60)
    print("PHASE 2 ENHANCED ANALYSIS SYSTEM TEST RESULTS")
    print("="*60)
    
    print(f"\nOverall Status: {results['overall_status']}")
    print(f"Tests Passed: {results['passed_tests']}/{results['total_tests']}")
    print(f"Success Rate: {results['success_rate']}")
    
    print("\nDetailed Results:")
    print("-" * 40)
    
    for component, result in results['detailed_results'].items():
        status_emoji = "✅" if result.get("status") == "success" else "❌" if result.get("status") == "error" else "⚠️"
        print(f"{status_emoji} {component.replace('_', ' ').title()}: {result.get('status', 'unknown')}")
        
        if result.get("status") == "success":
            # Print key metrics for successful tests
            if component == "data_extractor":
                print(f"   - Tables extracted: {result.get('tables_extracted', 0)}")
                print(f"   - Visualization suggestions: {result.get('visualization_suggestions', 0)}")
            elif component == "concept_processor":
                print(f"   - Concepts identified: {result.get('concepts_identified', 0)}")
                print(f"   - Diagrams generated: {result.get('diagrams_generated', 0)}")
            elif component == "dashboard_generator":
                print(f"   - Charts generated: {result.get('charts_generated', 0)}")
                print(f"   - Dashboard created: {result.get('dashboard_created', False)}")
            elif component == "modernization_engine":
                print(f"   - Technologies detected: {result.get('technologies_detected', 0)}")
                print(f"   - Outdated technologies: {result.get('outdated_technologies', 0)}")
            elif component == "integration":
                print(f"   - Cross-component functionality: Working")
        
        elif result.get("status") == "error":
            print(f"   - Error: {result.get('error', 'Unknown error')}")
    
    print("\n" + "="*60)

async def main():
    """Main test execution"""
    test_suite = Phase2TestSuite()
    
    try:
        results = await test_suite.run_all_tests()
        print_test_results(results)
        
        # Save results to file
        results_file = Path("phase2_test_results.json")
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"\nDetailed results saved to: {results_file}")
        
        # Exit with appropriate code
        exit_code = 0 if results['overall_status'] == 'PASS' else 1
        sys.exit(exit_code)
        
    except Exception as e:
        logger.error(f"Test suite execution failed: {e}")
        print(f"\n❌ Test suite execution failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())

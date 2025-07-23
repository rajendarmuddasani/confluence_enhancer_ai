"""
Comprehensive Phase 3 Testing Suite
Tests the complete Interactive Report Generation and Enhanced Page Publishing workflow
🚀 Phase 3: Interactive Reports & Enhanced Page Creation
"""
import pytest
import asyncio
import json
from datetime import datetime
from unittest.mock import Mock, AsyncMock, patch

# Import Phase 3 components
from src.reports.interactive_report import InteractiveReportGenerator
from src.api.page_creator import ConfluencePageCreator
from src.utils.config import Settings

# Mock test data
MOCK_ORIGINAL_PAGE = {
    'page_id': 'test_page_123',
    'title': 'Enterprise Data Architecture Guide',
    'url': 'https://company.atlassian.net/wiki/spaces/ARCH/pages/123456789',
    'space_key': 'ARCH',
    'parent_id': 'parent_123',
    'content': """
    <h1>Data Architecture Overview</h1>
    <p>Our enterprise data architecture follows modern patterns.</p>
    
    <table>
        <tr><th>Component</th><th>Technology</th><th>Version</th></tr>
        <tr><td>Database</td><td>MySQL</td><td>5.7</td></tr>
        <tr><td>Cache</td><td>Redis</td><td>4.0</td></tr>
        <tr><td>Queue</td><td>RabbitMQ</td><td>3.6</td></tr>
    </table>
    
    <p>Data flows through several processing stages...</p>
    """
}

MOCK_PHASE2_RESULTS = {
    'data_extraction': {
        'tables_found': [
            {
                'headers': ['Component', 'Technology', 'Version'],
                'rows': [
                    ['Database', 'MySQL', '5.7'],
                    ['Cache', 'Redis', '4.0'],
                    ['Queue', 'RabbitMQ', '3.6']
                ],
                'analysis': {
                    'total_rows': 3,
                    'data_quality': 'good',
                    'patterns': ['technology_stack']
                }
            }
        ],
        'suggestions': ['Consider upgrading MySQL to 8.0', 'Redis version is outdated']
    },
    'concept_processing': {
        'concepts': [
            {'name': 'Data Flow', 'importance': 0.9, 'category': 'process'},
            {'name': 'Technology Stack', 'importance': 0.8, 'category': 'architecture'},
            {'name': 'Processing Stages', 'importance': 0.7, 'category': 'workflow'}
        ],
        'diagrams': [
            {
                'type': 'flowchart',
                'title': 'Data Architecture Flow',
                'code': 'graph TD\n    A[Data Input] --> B[Processing]\n    B --> C[Storage]',
                'description': 'Data flow through the system'
            }
        ]
    },
    'dashboard_generation': {
        'dashboards': [
            {
                'title': 'Technology Stack Overview',
                'charts': [
                    {
                        'type': 'bar',
                        'data': {'components': ['Database', 'Cache', 'Queue'], 'versions': ['5.7', '4.0', '3.6']},
                        'title': 'Technology Versions'
                    }
                ],
                'html': '<div>Interactive dashboard HTML</div>'
            }
        ]
    },
    'modernization_analysis': {
        'outdated_technologies': [
            {
                'technology': 'MySQL 5.7',
                'modern_alternative': 'MySQL 8.0',
                'urgency': 'high',
                'migration_effort': 'medium',
                'benefits': ['Better performance', 'Security improvements', 'New features']
            }
        ],
        'implementation_roadmap': {
            'phases': [
                {
                    'phase': 'Phase 1: MySQL Upgrade',
                    'duration': '2-3 weeks',
                    'priority': 'high',
                    'tasks': ['Backup preparation', 'Migration testing', 'Production upgrade']
                }
            ]
        }
    }
}

class TestPhase3InteractiveReports:
    """Test the Phase 3 Interactive Report Generation"""
    
    @pytest.fixture
    def report_generator(self):
        """Create mock report generator"""
        return InteractiveReportGenerator()
    
    @pytest.mark.asyncio
    async def test_comprehensive_report_generation(self, report_generator):
        """Test 1: Comprehensive report generation from Phase 2 results"""
        print("🧪 Test 1: Comprehensive Report Generation")
        
        # Generate comprehensive report
        report = await report_generator.generate_comprehensive_report(
            original_page=MOCK_ORIGINAL_PAGE,
            phase2_results=MOCK_PHASE2_RESULTS
        )
        
        # Validate report structure
        assert report is not None
        assert 'executive_summary' in report
        assert 'content_changes' in report
        assert 'interactive_elements' in report
        assert 'implementation_guide' in report
        assert 'enhancement_metrics' in report
        assert 'confluence_formatted_content' in report
        
        # Validate executive summary
        summary = report['executive_summary']
        assert summary['overview'] is not None
        assert len(summary['key_improvements']) > 0
        assert 'business_impact' in summary
        
        print("✅ Report generated with all required sections")
        print(f"   📊 Executive summary: {len(summary['overview'])} characters")
        print(f"   📈 Key improvements: {len(summary['key_improvements'])} items")
        print(f"   💼 Business impact metrics: {len(summary['business_impact'])} items")
        
        return report
    
    @pytest.mark.asyncio 
    async def test_content_change_documentation(self, report_generator):
        """Test 2: Content change tracking and documentation"""
        print("\n🧪 Test 2: Content Change Documentation")
        
        report = await report_generator.generate_comprehensive_report(
            original_page=MOCK_ORIGINAL_PAGE,
            phase2_results=MOCK_PHASE2_RESULTS
        )
        
        changes = report['content_changes']
        
        # Validate change tracking
        assert 'structural_changes' in changes
        assert 'visual_enhancements' in changes
        assert 'modernization_updates' in changes
        
        structural = changes['structural_changes']
        visual = changes['visual_enhancements']
        modernization = changes['modernization_updates']
        
        assert len(structural) > 0
        assert len(visual) > 0
        assert len(modernization) > 0
        
        print(f"✅ Change documentation complete")
        print(f"   🏗️  Structural changes: {len(structural)}")
        print(f"   🎨 Visual enhancements: {len(visual)}")
        print(f"   🚀 Modernization updates: {len(modernization)}")
        
    @pytest.mark.asyncio
    async def test_interactive_elements_creation(self, report_generator):
        """Test 3: Interactive elements and widgets creation"""
        print("\n🧪 Test 3: Interactive Elements Creation")
        
        report = await report_generator.generate_comprehensive_report(
            original_page=MOCK_ORIGINAL_PAGE,
            phase2_results=MOCK_PHASE2_RESULTS
        )
        
        interactive = report['interactive_elements']
        
        # Validate interactive elements
        assert 'comparison_sliders' in interactive
        assert 'visualization_gallery' in interactive
        assert 'diagram_viewer' in interactive
        assert 'modernization_timeline' in interactive
        
        # Check specific elements
        assert len(interactive['comparison_sliders']) > 0
        assert len(interactive['visualization_gallery']) > 0
        assert len(interactive['diagram_viewer']) > 0
        
        print("✅ Interactive elements created successfully")
        print(f"   🎛️  Comparison sliders: {len(interactive['comparison_sliders'])}")
        print(f"   📊 Visualization gallery: {len(interactive['visualization_gallery'])}")
        print(f"   📈 Diagram viewer: {len(interactive['diagram_viewer'])}")
        
    @pytest.mark.asyncio
    async def test_enhancement_metrics_calculation(self, report_generator):
        """Test 4: Enhancement metrics calculation and reporting"""
        print("\n🧪 Test 4: Enhancement Metrics Calculation")
        
        report = await report_generator.generate_comprehensive_report(
            original_page=MOCK_ORIGINAL_PAGE,
            phase2_results=MOCK_PHASE2_RESULTS
        )
        
        metrics = report['enhancement_metrics']
        
        # Validate metrics structure
        assert 'content_metrics' in metrics
        assert 'visualization_metrics' in metrics
        assert 'modernization_metrics' in metrics
        assert 'quality_metrics' in metrics
        
        # Validate specific metrics
        content_metrics = metrics['content_metrics']
        viz_metrics = metrics['visualization_metrics']
        mod_metrics = metrics['modernization_metrics']
        quality_metrics = metrics['quality_metrics']
        
        assert content_metrics['enhanced_sections'] > 0
        assert viz_metrics['total_visualizations'] > 0
        assert mod_metrics['technologies_analyzed'] > 0
        assert quality_metrics['readability_score'] is not None
        
        print("✅ Enhancement metrics calculated")
        print(f"   📝 Sections enhanced: {content_metrics['enhanced_sections']}")
        print(f"   📊 Visualizations added: {viz_metrics['total_visualizations']}")
        print(f"   🔧 Technologies analyzed: {mod_metrics['technologies_analyzed']}")
        print(f"   📖 Readability improvement: {quality_metrics['readability_score']}")
        
    @pytest.mark.asyncio
    async def test_confluence_content_formatting(self, report_generator):
        """Test 5: Confluence markup formatting and structure"""
        print("\n🧪 Test 5: Confluence Content Formatting")
        
        report = await report_generator.generate_comprehensive_report(
            original_page=MOCK_ORIGINAL_PAGE,
            phase2_results=MOCK_PHASE2_RESULTS
        )
        
        confluence_content = report['confluence_formatted_content']
        
        # Validate Confluence markup
        assert confluence_content is not None
        assert len(confluence_content) > 1000  # Should be substantial content
        assert '<h1>' in confluence_content or 'h1.' in confluence_content
        assert '<ac:structured-macro' in confluence_content
        
        # Check for specific Confluence elements
        assert 'ac:parameter' in confluence_content
        assert 'ac:rich-text-body' in confluence_content
        
        print("✅ Confluence formatting applied")
        print(f"   📄 Content length: {len(confluence_content)} characters")
        print(f"   🏷️  Contains macros: {'ac:structured-macro' in confluence_content}")
        
        return confluence_content


class TestPhase3PageCreation:
    """Test the Phase 3 Enhanced Page Creation"""
    
    @pytest.fixture
    def settings(self):
        """Mock settings for testing"""
        mock_settings = Mock(spec=Settings)
        mock_settings.CONFLUENCE_BASE_URL = "https://test.atlassian.net"
        mock_settings.CONFLUENCE_USERNAME = "test_user"
        mock_settings.CONFLUENCE_API_TOKEN = "test_token"
        return mock_settings
    
    @pytest.fixture
    def page_creator(self, settings):
        """Create mock page creator"""
        return ConfluencePageCreator(settings)
    
    @pytest.mark.asyncio
    async def test_page_configuration_preparation(self, page_creator):
        """Test 6: New page configuration preparation"""
        print("\n🧪 Test 6: Page Configuration Preparation")
        
        # Mock enhanced content
        enhanced_content = {
            'title': 'Enhanced Data Architecture',
            'visualizations': [{'type': 'dashboard'}],
            'diagrams': [{'type': 'flowchart'}],
            'modernizations': [{'technology': 'MySQL'}],
            'interactive_elements': [{'type': 'slider'}]
        }
        
        # Mock report data
        report_data = {
            'executive_summary': {'overview': 'Test summary'},
            'metadata': {'report_id': 'test_123'}
        }
        
        # Prepare configuration
        config = await page_creator._prepare_new_page_config(
            enhanced_content, MOCK_ORIGINAL_PAGE, report_data
        )
        
        # Validate configuration
        assert config['title'].endswith('_ENHANCED_' + datetime.now().strftime('%d%m%Y')[-6:])
        assert config['space_key'] == MOCK_ORIGINAL_PAGE['space_key']
        assert config['metadata']['original_page_id'] == MOCK_ORIGINAL_PAGE['page_id']
        assert len(config['labels']) > 0
        
        print("✅ Page configuration prepared")
        print(f"   📝 New title: {config['title']}")
        print(f"   🏷️  Labels: {len(config['labels'])} applied")
        print(f"   📊 Enhancements tracked: {config['metadata']['enhancements_applied']}")
        
    @pytest.mark.asyncio
    async def test_page_configuration_validation(self, page_creator):
        """Test 7: Configuration validation before page creation"""
        print("\n🧪 Test 7: Configuration Validation")
        
        # Test valid configuration
        valid_config = {
            'title': 'Valid Test Page',
            'space_key': 'TEST',
            'content': '<p>Test content</p>'
        }
        
        assert page_creator._validate_page_config(valid_config) == True
        
        # Test invalid configuration - missing title
        invalid_config = {
            'space_key': 'TEST',
            'content': '<p>Test content</p>'
        }
        
        assert page_creator._validate_page_config(invalid_config) == False
        
        # Test invalid configuration - title too long
        long_title_config = {
            'title': 'x' * 300,  # Too long
            'space_key': 'TEST',
            'content': '<p>Test content</p>'
        }
        
        assert page_creator._validate_page_config(long_title_config) == False
        
        print("✅ Configuration validation working")
        print("   ✅ Valid config accepted")
        print("   ❌ Invalid configs rejected")
        
    @pytest.mark.asyncio
    @patch('aiohttp.ClientSession.post')
    async def test_page_creation_execution(self, mock_post, page_creator):
        """Test 8: Actual page creation execution (mocked)"""
        print("\n🧪 Test 8: Page Creation Execution")
        
        # Mock successful API response
        mock_response = Mock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={
            'id': 'new_page_123',
            'title': 'Enhanced Page',
            '_links': {'webui': '/pages/viewpage.action?pageId=new_page_123'}
        })
        
        mock_post.return_value.__aenter__.return_value = mock_response
        
        config = {
            'title': 'Test Enhanced Page',
            'space_key': 'TEST',
            'content': '<p>Enhanced content</p>'
        }
        
        result = await page_creator._execute_page_creation(config)
        
        # Validate successful creation
        assert result['success'] == True
        assert result['page_id'] == 'new_page_123'
        assert 'page_url' in result
        
        print("✅ Page creation execution successful")
        print(f"   📄 New page ID: {result['page_id']}")
        print(f"   🔗 Page URL: {result['page_url']}")
        
    @pytest.mark.asyncio
    async def test_enhancement_summary_generation(self, page_creator):
        """Test 9: Enhancement summary generation"""
        print("\n🧪 Test 9: Enhancement Summary Generation")
        
        enhanced_content = {
            'visualizations': [{'type': 'dashboard'}, {'type': 'chart'}],
            'diagrams': [{'type': 'flowchart'}],
            'modernizations': [{'technology': 'MySQL'}, {'technology': 'Redis'}],
            'interactive_elements': [{'type': 'slider'}],
            'sections': [{'title': 'Section 1'}, {'title': 'Section 2'}]
        }
        
        summary = page_creator._generate_enhancement_summary(enhanced_content)
        
        # Validate summary
        assert summary['visualizations'] == 2
        assert summary['diagrams'] == 1
        assert summary['modernizations'] == 2
        assert summary['sections_enhanced'] == 2
        assert summary['total_enhancements'] == 5  # viz + diagrams + mods
        
        print("✅ Enhancement summary generated")
        print(f"   📊 Total enhancements: {summary['total_enhancements']}")
        print(f"   📈 Visualizations: {summary['visualizations']}")
        print(f"   📋 Sections enhanced: {summary['sections_enhanced']}")


class TestPhase3Integration:
    """Integration tests for complete Phase 3 workflow"""
    
    @pytest.mark.asyncio
    async def test_end_to_end_workflow(self):
        """Test 10: Complete end-to-end Phase 3 workflow"""
        print("\n🧪 Test 10: End-to-End Phase 3 Workflow")
        
        # Step 1: Generate comprehensive report
        report_generator = InteractiveReportGenerator()
        report = await report_generator.generate_comprehensive_report(
            original_page=MOCK_ORIGINAL_PAGE,
            phase2_results=MOCK_PHASE2_RESULTS
        )
        
        # Step 2: Prepare page creation
        mock_settings = Mock(spec=Settings)
        mock_settings.CONFLUENCE_BASE_URL = "https://test.atlassian.net"
        mock_settings.CONFLUENCE_USERNAME = "test_user"
        mock_settings.CONFLUENCE_API_TOKEN = "test_token"
        
        page_creator = ConfluencePageCreator(mock_settings)
        
        # Step 3: Prepare enhanced content for page creation
        enhanced_content = {
            'title': report['metadata']['enhanced_title'],
            'visualizations': MOCK_PHASE2_RESULTS['dashboard_generation']['dashboards'],
            'diagrams': MOCK_PHASE2_RESULTS['concept_processing']['diagrams'],
            'modernizations': MOCK_PHASE2_RESULTS['modernization_analysis']['outdated_technologies'],
            'interactive_elements': report['interactive_elements'],
            'confluence_formatted_content': report['confluence_formatted_content']
        }
        
        # Step 4: Validate complete workflow components
        assert report is not None
        assert enhanced_content['confluence_formatted_content'] is not None
        assert len(enhanced_content['visualizations']) > 0
        assert len(enhanced_content['diagrams']) > 0
        
        # Step 5: Generate page configuration
        config = await page_creator._prepare_new_page_config(
            enhanced_content, MOCK_ORIGINAL_PAGE, report
        )
        
        assert page_creator._validate_page_config(config)
        
        print("✅ End-to-End Phase 3 workflow validated")
        print(f"   📊 Report sections: {len(report.keys())}")
        print(f"   📄 Enhanced content ready: {len(enhanced_content['confluence_formatted_content'])} chars")
        print(f"   ⚙️  Page config valid: {config['title']}")
        print("\n🎉 Phase 3: Interactive Reports & Page Creation - COMPLETE!")


# Test runner function
async def run_phase3_tests():
    """Run all Phase 3 tests"""
    print("🚀 Starting Phase 3 Testing Suite")
    print("=" * 60)
    
    # Test Interactive Reports
    print("\n📊 PHASE 3A: INTERACTIVE REPORT GENERATION")
    print("-" * 50)
    
    report_tests = TestPhase3InteractiveReports()
    generator = report_tests.report_generator()
    
    await report_tests.test_comprehensive_report_generation(generator)
    await report_tests.test_content_change_documentation(generator)
    await report_tests.test_interactive_elements_creation(generator)
    await report_tests.test_enhancement_metrics_calculation(generator)
    await report_tests.test_confluence_content_formatting(generator)
    
    # Test Page Creation
    print("\n📄 PHASE 3B: ENHANCED PAGE CREATION")
    print("-" * 50)
    
    page_tests = TestPhase3PageCreation()
    settings = page_tests.settings()
    creator = page_tests.page_creator(settings)
    
    await page_tests.test_page_configuration_preparation(creator)
    await page_tests.test_page_configuration_validation(creator)
    await page_tests.test_enhancement_summary_generation(creator)
    
    # Test Integration
    print("\n🔗 PHASE 3C: INTEGRATION TESTING")
    print("-" * 50)
    
    integration_tests = TestPhase3Integration()
    await integration_tests.test_end_to_end_workflow()
    
    print("\n" + "=" * 60)
    print("🎊 PHASE 3 TESTING COMPLETE!")
    print("✅ All Phase 3 components validated and ready")
    print("🔗 System ready for complete Confluence enhancement workflow")


if __name__ == "__main__":
    # Run the tests
    asyncio.run(run_phase3_tests())

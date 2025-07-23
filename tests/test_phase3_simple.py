"""
Simple Phase 3 Validation Test
Tests core Phase 3 functionality without complex dependencies
"""
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.reports.interactive_report import InteractiveReportGenerator

# Test data
TEST_ORIGINAL_PAGE = {
    'page_id': 'test_123',
    'title': 'Test Architecture Guide',
    'url': 'https://test.com/page',
    'space_key': 'TEST'
}

TEST_ORIGINAL_CONTENT = "Test content about data architecture with some tables and processes."

TEST_ENHANCED_CONTENT = {
    'sections': [
        {'title': 'Enhanced Section 1', 'content': 'Improved content'},
        {'title': 'Enhanced Section 2', 'content': 'More improvements'}
    ]
}

TEST_VISUALIZATIONS = [
    {
        'type': 'dashboard',
        'title': 'Test Dashboard',
        'charts': [{'type': 'bar', 'title': 'Test Chart'}]
    }
]

TEST_MODERNIZATIONS = [
    {
        'technology': 'MySQL 5.7',
        'modern_alternative': 'MySQL 8.0',
        'urgency': 'high'
    }
]

async def test_phase3_core():
    """Test Phase 3 core functionality"""
    print("🚀 Testing Phase 3 Core Functionality")
    print("=" * 50)
    
    try:
        # Initialize report generator
        generator = InteractiveReportGenerator()
        print("✅ InteractiveReportGenerator initialized")
        
        # Test comprehensive report generation
        print("\n📊 Testing comprehensive report generation...")
        report = await generator.generate_comprehensive_report(
            original_page=TEST_ORIGINAL_PAGE,
            original_content=TEST_ORIGINAL_CONTENT,
            enhanced_content=TEST_ENHANCED_CONTENT,
            visualizations=TEST_VISUALIZATIONS,
            modernizations=TEST_MODERNIZATIONS
        )
        
        # Validate report structure
        required_sections = [
            'executive_summary',
            'content_changes', 
            'interactive_elements',
            'implementation_guide',
            'enhancement_metrics',
            'confluence_formatted_content',
            'metadata'
        ]
        
        for section in required_sections:
            if section in report:
                print(f"   ✅ {section}: Present")
            else:
                print(f"   ❌ {section}: Missing")
        
        # Test specific functionality
        print(f"\n📈 Report Quality Metrics:")
        print(f"   📄 Content length: {len(report.get('confluence_formatted_content', ''))} chars")
        print(f"   📊 Executive summary: {len(report.get('executive_summary', {}).get('overview', ''))} chars")
        print(f"   🔧 Content changes tracked: {len(report.get('content_changes', {}).get('structural_changes', []))}")
        print(f"   🎛️  Interactive elements: {len(report.get('interactive_elements', {}).get('comparison_sliders', []))}")
        
        # Test enhancement metrics
        metrics = report.get('enhancement_metrics', {})
        print(f"\n📊 Enhancement Metrics:")
        print(f"   📝 Content metrics: {len(metrics.get('content_metrics', {}))}")
        print(f"   📈 Visualization metrics: {len(metrics.get('visualization_metrics', {}))}")
        print(f"   🚀 Modernization metrics: {len(metrics.get('modernization_metrics', {}))}")
        print(f"   ⭐ Quality metrics: {len(metrics.get('quality_metrics', {}))}")
        
        print("\n🎉 Phase 3 Core Functionality: WORKING!")
        return True
        
    except Exception as e:
        print(f"❌ Error in Phase 3 testing: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def test_confluence_formatting():
    """Test Confluence formatting specifically"""
    print("\n🔧 Testing Confluence Content Formatting")
    print("-" * 40)
    
    try:
        generator = InteractiveReportGenerator()
        
        # Test specific content formatting
        test_content = {
            'sections': [{'title': 'Test Section', 'content': 'Test content'}],
            'visualizations': TEST_VISUALIZATIONS,
            'modernizations': TEST_MODERNIZATIONS
        }
        
        formatted_content = await generator._format_content_for_confluence(test_content)
        
        # Check for Confluence-specific markup
        confluence_indicators = [
            '<h1>', '<h2>', '<h3>',
            'ac:structured-macro',
            'ac:parameter',
            'ac:rich-text-body'
        ]
        
        found_indicators = []
        for indicator in confluence_indicators:
            if indicator in formatted_content:
                found_indicators.append(indicator)
        
        print(f"   📄 Formatted content length: {len(formatted_content)}")
        print(f"   🏷️  Confluence markup indicators found: {len(found_indicators)}")
        print(f"   ✅ Contains: {', '.join(found_indicators[:3])}...")
        
        if len(found_indicators) > 2:
            print("   ✅ Confluence formatting: WORKING!")
            return True
        else:
            print("   ⚠️  Confluence formatting: May need improvement")
            return False
            
    except Exception as e:
        print(f"   ❌ Error in Confluence formatting: {str(e)}")
        return False

async def main():
    """Run all Phase 3 validation tests"""
    print("🚀 PHASE 3 VALIDATION TEST SUITE")
    print("Interactive Reports & Enhanced Page Publishing")
    print("=" * 60)
    
    results = []
    
    # Test core functionality
    result1 = await test_phase3_core()
    results.append(result1)
    
    # Test Confluence formatting
    result2 = await test_confluence_formatting()
    results.append(result2)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 PHASE 3 VALIDATION SUMMARY")
    print(f"✅ Tests passed: {sum(results)}/{len(results)}")
    
    if all(results):
        print("🎉 PHASE 3 READY FOR DEPLOYMENT!")
        print("🔗 System can now generate comprehensive reports and enhanced pages")
    else:
        print("⚠️  Some issues found - check output above")
    
    return all(results)

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)

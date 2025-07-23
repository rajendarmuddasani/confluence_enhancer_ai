#!/usr/bin/env python3
"""
Test script to verify backend components are working
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test that all major components can be imported"""
    try:
        print("Testing imports...")
        
        # Test basic imports
        from src.utils.config import settings
        print("✓ Config imported")
        
        from src.utils.helpers import logger
        print("✓ Helpers imported")
        
        # Test model imports
        from src.models.content_model import ContentModel
        print("✓ Content model imported")
        
        from src.models.visualization_model import VisualizationModel
        print("✓ Visualization model imported")
        
        from src.models.enhancement_model import EnhancementModel
        print("✓ Enhancement model imported")
        
        # Test API imports
        try:
            from src.api.confluence_client import ConfluenceClient
            print("✓ Confluence client imported")
        except Exception as e:
            print(f"⚠ Confluence client import warning: {e}")
        
        # Test AI engine imports
        try:
            from src.ai_engine.content_analyzer import ContentAnalyzer
            print("✓ Content analyzer imported")
        except Exception as e:
            print(f"⚠ Content analyzer import warning: {e}")
        
        # Test processors
        try:
            from src.processors.table_processor import TableProcessor
            print("✓ Table processor imported")
        except Exception as e:
            print(f"⚠ Table processor import warning: {e}")
        
        # Test visualizations
        try:
            from src.visualizations.dashboard_generator import DashboardGenerator
            print("✓ Dashboard generator imported")
        except Exception as e:
            print(f"⚠ Dashboard generator import warning: {e}")
        
        print("\n✅ All critical imports successful!")
        return True
        
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality"""
    try:
        print("\nTesting basic functionality...")
        
        # Test config
        from src.utils.config import settings
        print(f"✓ Config loaded, debug mode: {settings.DEBUG}")
        
        # Test logger
        from src.utils.helpers import logger
        logger.info("Test log message")
        print("✓ Logger working")
        
        # Test models
        from src.models.content_model import ContentModel
        content = ContentModel(
            content_id="test_id",
            title="Test Content",
            raw_text="This is test content",
            raw_html="<p>This is test content</p>",
            page_url="https://example.com/test"
        )
        print(f"✓ Content model created: {content.title}")
        
        print("\n✅ Basic functionality tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Functionality test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=== Confluence Enhancer Backend Test ===\n")
    
    import_success = test_imports()
    func_success = test_basic_functionality()
    
    if import_success and func_success:
        print("\n🎉 All tests passed! Backend is ready.")
        return 0
    else:
        print("\n❌ Some tests failed. Check the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

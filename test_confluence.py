#!/usr/bin/env python3
"""
Test script to verify Confluence API connection
Run this after setting up your .env file
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.utils.config import settings
from src.api.confluence_client import ConfluenceClient
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_confluence_connection():
    """Test Confluence API connection"""
    print("🔍 Testing Confluence API Connection...")
    print(f"Base URL: {settings.CONFLUENCE_BASE_URL}")
    print(f"Username: {settings.CONFLUENCE_USERNAME}")
    print(f"API Token: {'*' * (len(settings.CONFLUENCE_API_TOKEN) - 4) + settings.CONFLUENCE_API_TOKEN[-4:] if settings.CONFLUENCE_API_TOKEN else 'NOT SET'}")
    print("-" * 50)
    
    # Check if credentials are set
    if not settings.CONFLUENCE_BASE_URL:
        print("❌ CONFLUENCE_BASE_URL not set in .env file")
        return False
    
    if not settings.CONFLUENCE_USERNAME:
        print("❌ CONFLUENCE_USERNAME not set in .env file")
        return False
    
    if not settings.CONFLUENCE_API_TOKEN:
        print("❌ CONFLUENCE_API_TOKEN not set in .env file")
        return False
    
    try:
        # Create client
        client = ConfluenceClient()
        
        # Test connection
        print("🔗 Testing connection...")
        is_valid = client.validate_connection()
        
        if is_valid:
            print("✅ SUCCESS: Confluence API connection established!")
            
            # Test page access
            test_url = "https://rajendarmuddasani.atlassian.net/wiki/spaces/SD/pages/2949124/Claudee"
            print(f"🔍 Testing access to specific page: {test_url}")
            
            page_id = client.extract_page_id_from_url(test_url)
            if page_id:
                print(f"✅ Page ID extracted: {page_id}")
                
                # Try to fetch page content
                content = client.get_page_content(page_id)
                if content:
                    print("✅ SUCCESS: Page content retrieved!")
                    print(f"Page title: {content.get('title', 'Unknown')}")
                    return True
                else:
                    print("❌ FAILED: Could not retrieve page content")
                    return False
            else:
                print("❌ FAILED: Could not extract page ID from URL")
                return False
        else:
            print("❌ FAILED: Could not connect to Confluence API")
            print("Check your credentials and try again")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

def main():
    """Main function"""
    print("=" * 60)
    print("🚀 Confluence API Connection Test")
    print("=" * 60)
    
    success = test_confluence_connection()
    
    print("-" * 60)
    if success:
        print("🎉 All tests passed! Your Confluence setup is working.")
        print("You can now use the application at: http://localhost:3002")
    else:
        print("❌ Tests failed. Please check your .env configuration.")
        print("See CONFLUENCE_SETUP.md for detailed setup instructions.")
    print("=" * 60)

if __name__ == "__main__":
    main()

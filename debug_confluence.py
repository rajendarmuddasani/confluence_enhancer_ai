#!/usr/bin/env python3
"""
Detailed Confluence API test with debugging
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import requests
from src.utils.config import settings
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def test_confluence_detailed():
    """Detailed test of Confluence API with debugging"""
    print("=" * 60)
    print("🔍 DETAILED CONFLUENCE API TEST")
    print("=" * 60)
    
    base_url = settings.CONFLUENCE_BASE_URL
    username = settings.CONFLUENCE_USERNAME  
    api_token = settings.CONFLUENCE_API_TOKEN
    
    print(f"Base URL: {base_url}")
    print(f"Username: {username}")
    print(f"API Token: {api_token[:10]}...{api_token[-4:] if len(api_token) > 10 else api_token}")
    print("-" * 60)
    
    # Test 1: Basic authentication
    print("🔗 Test 1: Basic Authentication")
    session = requests.Session()
    session.auth = (username, api_token)
    session.headers.update({
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    })
    
    try:
        # Try different endpoints to find what works
        endpoints_to_test = [
            "/wiki/rest/api/user/current",  # Get current user info (Confluence Cloud)
            "/wiki/rest/api/space",          # List spaces (Confluence Cloud)
            "/wiki/rest/api/content",        # List content (Confluence Cloud)
        ]
        
        for endpoint in endpoints_to_test:
            url = base_url + endpoint
            print(f"  Testing: {url}")
            
            try:
                response = session.get(url, timeout=10)
                print(f"  Status: {response.status_code}")
                
                if response.status_code == 200:
                    print("  ✅ SUCCESS!")
                    data = response.json()
                    if 'username' in data:
                        print(f"  Authenticated as: {data.get('username', 'Unknown')}")
                    elif 'results' in data:
                        print(f"  Results: {len(data['results'])} items")
                    break
                elif response.status_code == 401:
                    print("  ❌ UNAUTHORIZED - Check credentials")
                elif response.status_code == 403:
                    print("  ❌ FORBIDDEN - Check permissions")
                else:
                    print(f"  ❌ ERROR: {response.status_code}")
                    try:
                        error_data = response.json()
                        print(f"  Error details: {error_data}")
                    except:
                        print(f"  Response text: {response.text[:200]}")
                        
            except requests.exceptions.RequestException as e:
                print(f"  ❌ REQUEST ERROR: {e}")
                
    except Exception as e:
        print(f"❌ SETUP ERROR: {e}")
        return False
    
    print("-" * 60)
    
    # Test 2: Test specific page access
    print("🔗 Test 2: Specific Page Access")
    page_url = "https://rajendarmuddasani.atlassian.net/wiki/spaces/SD/pages/2949124/Claudee"
    page_id = "2949124"
    
    try:
        content_url = f"{base_url}/wiki/rest/api/content/{page_id}"
        print(f"  Testing page: {content_url}")
        
        response = session.get(content_url, timeout=10)
        print(f"  Status: {response.status_code}")
        
        if response.status_code == 200:
            print("  ✅ SUCCESS! Page accessible")
            data = response.json()
            print(f"  Page title: {data.get('title', 'Unknown')}")
            print(f"  Space key: {data.get('space', {}).get('key', 'Unknown')}")
            return True
        else:
            print(f"  ❌ FAILED: {response.status_code}")
            try:
                error_data = response.json()
                print(f"  Error: {error_data}")
            except:
                print(f"  Response: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ PAGE TEST ERROR: {e}")
        return False

if __name__ == "__main__":
    success = test_confluence_detailed()
    print("=" * 60)
    if success:
        print("🎉 Connection successful! You should be able to use the application.")
    else:
        print("❌ Connection failed. Please check your API token and permissions.")
    print("=" * 60)

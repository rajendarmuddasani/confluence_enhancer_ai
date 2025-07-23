#!/usr/bin/env python3

import sys
import traceback
sys.path.append('.')

try:
    print("1. Starting imports...")
    import requests
    import json
    from typing import Dict, Any, Optional, List
    from urllib.parse import urljoin, urlparse
    from bs4 import BeautifulSoup
    import logging
    print("2. Basic imports successful")

    try:
        from src.utils.config import settings
        print("3. Config import successful")
    except Exception as e:
        print(f"3. Config import failed: {e}")

    try:
        from src.utils.helpers import clean_text, extract_table_data
        print("4. Helpers import successful")
    except Exception as e:
        print(f"4. Helpers import failed: {e}")

    print("5. Attempting to import ConfluenceClient...")
    from src.api.confluence_client import ConfluenceClient
    print("6. ConfluenceClient import successful")
    
    print("7. Creating instance...")
    client = ConfluenceClient()
    print("8. Instance created successfully")
    
    print("9. Testing methods...")
    print(f"   Has extract_space_key_from_url: {hasattr(client, 'extract_space_key_from_url')}")
    print(f"   Has create_page: {hasattr(client, 'create_page')}")
    
    if hasattr(client, 'extract_space_key_from_url'):
        print("10. Testing extract_space_key_from_url...")
        test_url = "https://rajendarmuddasani.atlassian.net/wiki/spaces/SD/pages/2949124/Claudee"
        space_key = client.extract_space_key_from_url(test_url) 
        print(f"    Space key: {space_key}")
    
    print("✓ All tests passed!")

except Exception as e:
    print(f"✗ Error: {e}")
    traceback.print_exc()

"""
Confluence API client for content extraction
"""
import requests
import json
from typing import Dict, Any, Optional, List
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import logging

from ..utils.config import settings
from ..utils.helpers import clean_text, extract_table_data


logger = logging.getLogger(__name__)


class ConfluenceClient:
    """Client for interacting with Confluence API"""
    
    def __init__(self, base_url: str = None, username: str = None, api_token: str = None):
        self.base_url = base_url or settings.CONFLUENCE_BASE_URL
        self.username = username or settings.CONFLUENCE_USERNAME
        self.api_token = api_token or settings.CONFLUENCE_API_TOKEN
        
        if not all([self.base_url, self.username, self.api_token]):
            logger.warning("Confluence credentials not fully configured")
        
        self.session = requests.Session()
        self.session.auth = (self.username, self.api_token)
        self.session.headers.update({
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
    
    def extract_page_id_from_url(self, page_url: str) -> Optional[str]:
        """Extract page ID from Confluence URL"""
        try:
            import re
            patterns = [
                r'/pages/(\d+)/',
                r'pageId=(\d+)',
                r'/(\d+)$'
            ]
            
            for pattern in patterns:
                match = re.search(pattern, page_url)
                if match:
                    return match.group(1)
            
            parsed = urlparse(page_url)
            path_parts = parsed.path.split('/')
            
            for part in path_parts:
                if part.isdigit():
                    return part
            
            return None
            
        except Exception as e:
            logger.error(f"Error extracting page ID from URL: {e}")
            return None
    
    def get_page_content(self, page_id: str) -> Dict[str, Any]:
        """Get page content by page ID"""
        try:
            url = urljoin(self.base_url, f"/wiki/rest/api/content/{page_id}")
            params = {
                'expand': 'body.storage,version,space,metadata.labels'
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            logger.error(f"Error getting page content: {e}")
            return {}
    
    def validate_connection(self) -> bool:
        """Validate connection to Confluence"""
        try:
            url = urljoin(self.base_url, "/wiki/rest/api/space")
            response = self.session.get(url, timeout=10)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Connection validation failed: {e}")
            return False

    def get_page_content_by_url(self, page_url: str) -> Dict[str, Any]:
        """Get page content by URL (compatibility method for content extractor)"""
        try:
            page_id = self.extract_page_id_from_url(page_url)
            if not page_id:
                logger.error("Could not extract page ID from URL")
                return {}
            
            page_data = self.get_page_content(page_id)
            if not page_data:
                logger.error("Could not fetch page content")
                return {}
            
            # Return the raw API response
            return page_data
            
        except Exception as e:
            logger.error(f"Error getting page content by URL: {e}")
            return {}

    def extract_content_structure(self, raw_content):
        """Extract structured content from raw page data"""
        try:
            if not raw_content:
                return {}
            
            # Extract storage content
            storage_content = raw_content.get('body', {}).get('storage', {}).get('value', '')
            
            # Parse HTML content with BeautifulSoup
            soup = BeautifulSoup(storage_content, 'html.parser')
            
            # Extract structured content
            structured = {
                'title': raw_content.get('title', ''),
                'page_id': raw_content.get('id', ''),
                'space_key': raw_content.get('space', {}).get('key', ''),
                'space_name': raw_content.get('space', {}).get('name', ''),
                'version': raw_content.get('version', {}).get('number', 1),
                'raw_html': storage_content,
                'raw_text': soup.get_text(strip=True) if soup else '',
                'text_content': soup.get_text(strip=True) if soup else '',
                'tables': [],
                'headings': [],
                'metadata': {
                    'created': raw_content.get('history', {}).get('createdDate', ''),
                    'modified': raw_content.get('version', {}).get('when', ''),
                    'created_by': raw_content.get('history', {}).get('createdBy', {}).get('displayName', ''),
                    'modified_by': raw_content.get('version', {}).get('by', {}).get('displayName', '')
                }
            }
            
            return structured
            
        except Exception as e:
            logger.error(f"Error extracting content structure: {e}")
            return {}

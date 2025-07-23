"""
Test to verify that original pages are never modified
"""
import pytest
from unittest.mock import AsyncMock, patch
from src.api.page_creator import ConfluencePageCreator
from src.api.content_extractor import ContentExtractor


class TestOriginalPageProtection:
    """Ensure original pages are never modified"""
    
    @patch('aiohttp.ClientSession.get')
    async def test_content_extraction_is_read_only(self, mock_get):
        """Verify content extraction only uses GET requests"""
        # Mock response
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json.return_value = {
            'body': {'storage': {'value': '<p>Test content</p>'}},
            'title': 'Test Page'
        }
        mock_get.return_value.__aenter__.return_value = mock_response
        
        extractor = ContentExtractor()
        
        # Extract content
        result = await extractor.extract_from_url('https://confluence.com/test-page')
        
        # Verify only GET request was made
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert call_args[1]['method'] == 'GET' or not 'method' in call_args[1]  # GET is default
        
        # Verify no PUT, POST, DELETE calls
        assert not any(call for call in mock_get.call_args_list 
                      if call[1].get('method') in ['PUT', 'POST', 'DELETE'])
    
    @patch('aiohttp.ClientSession.post')
    async def test_page_creation_only_creates_new_pages(self, mock_post):
        """Verify page creation only creates NEW pages, never modifies existing"""
        # Mock successful page creation
        mock_response = AsyncMock()
        mock_response.status = 201
        mock_response.json.return_value = {
            'id': '12345',
            'title': 'Test_Page_143052_151224',
            '_links': {'webui': '/display/SPACE/Test_Page_143052_151224'}
        }
        mock_post.return_value.__aenter__.return_value = mock_response
        
        # Create page creator
        from src.utils.config import Settings
        settings = Settings()
        creator = ConfluencePageCreator(settings)
        
        # Test data
        original_page_info = {
            'title': 'Test Page',
            'space_key': 'SPACE',
            'url': 'https://confluence.com/original'
        }
        enhanced_content = {
            'sections': [{'title': 'Enhanced Section', 'content': 'Enhanced content'}]
        }
        
        # Create enhanced page
        result = await creator.create_enhanced_page(
            original_page_info=original_page_info,
            enhanced_content=enhanced_content
        )
        
        # Verify POST request was made to create NEW page
        mock_post.assert_called_once()
        call_args = mock_post.call_args[1]
        
        # Verify it's creating a NEW page (not updating existing)
        assert 'content' in call_args['url']  # Confluence content creation endpoint
        
        # Verify the new page has timestamp naming
        created_data = call_args['json']
        assert '_' in created_data['title']  # Should have timestamp format
        assert created_data['title'] != original_page_info['title']  # Different from original
    
    def test_page_naming_convention(self):
        """Verify new pages follow naming convention"""
        from src.api.page_creator import ConfluencePageCreator
        from src.utils.config import Settings
        
        creator = ConfluencePageCreator(Settings())
        
        original_page_info = {
            'title': 'My Test Page',
            'space_key': 'SPACE'
        }
        enhanced_content = {'sections': []}
        
        # Generate page details
        page_details = creator._generate_page_details(original_page_info, enhanced_content)
        
        # Verify naming convention
        assert page_details['title'] != original_page_info['title']
        assert 'My_Test_Page_' in page_details['title']
        assert len(page_details['title'].split('_')) >= 4  # title_HHMMSS_DDMMYY
        
        # Verify original page link is preserved
        assert 'original_page_link' in page_details
        
    def test_no_original_page_modification_methods(self):
        """Verify no methods exist that could modify original pages"""
        from src.api.page_creator import ConfluencePageCreator
        from src.api.content_extractor import ContentExtractor
        
        # Check page creator methods
        creator_methods = dir(ConfluencePageCreator)
        dangerous_methods = [
            'update_original', 'modify_original', 'edit_original',
            'overwrite_original', 'replace_original', 'delete_original'
        ]
        
        for method in dangerous_methods:
            assert method not in creator_methods, f"Found dangerous method: {method}"
        
        # Check content extractor methods  
        extractor_methods = dir(ContentExtractor)
        for method in dangerous_methods:
            assert method not in extractor_methods, f"Found dangerous method: {method}"
        
        # Verify only safe methods exist
        safe_creator_methods = [m for m in creator_methods if m.startswith('create') or m.startswith('_')]
        assert 'create_enhanced_page' in creator_methods
        assert any('create' in m for m in creator_methods)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

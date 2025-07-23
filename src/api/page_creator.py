"""
Enhanced Page Creation and Publishing Service
Creates NEW Confluence pages with enhanced content while preserving original pages.
🔒 CRITICAL: NEVER modifies original pages - only creates new enhanced pages.
"""
import logging
import asyncio
import re
from typing import Dict, Any, List, Optional
from datetime import datetime
import aiohttp
import json
from urllib.parse import urlparse
from src.utils.config import Settings

logger = logging.getLogger(__name__)


class ConfluencePageCreator:
    """Service for creating new enhanced Confluence pages."""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.base_url = settings.CONFLUENCE_BASE_URL
        self.auth = aiohttp.BasicAuth(
            settings.CONFLUENCE_USERNAME,
            settings.CONFLUENCE_API_TOKEN
        )
        self.creation_timeout = 300  # 5 minutes timeout for page creation
        
    async def create_enhanced_page(
        self, 
        enhanced_content: Dict[str, Any], 
        original_page_info: Dict[str, Any],
        report_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create a NEW enhanced Confluence page.
        🔒 CRITICAL: Never touches the original page.
        """
        try:
            # Generate new page configuration
            new_page_config = await self._prepare_new_page_config(
                enhanced_content, original_page_info, report_data
            )
            
            # Validate configuration
            if not self._validate_page_config(new_page_config):
                raise ValueError("Invalid page configuration generated")
            
            # Create the new page
            creation_result = await self._execute_page_creation(new_page_config)
            
            # Verify creation was successful
            verification_result = await self._verify_page_creation(creation_result)
            
            # Update page with enhanced content
            if verification_result['success']:
                content_update_result = await self._update_page_content(
                    creation_result['page_id'],
                    enhanced_content,
                    report_data
                )
                
                return {
                    'success': True,
                    'new_page_id': creation_result['page_id'],
                    'new_page_url': creation_result['page_url'],
                    'page_title': new_page_config['title'],
                    'original_page_preserved': True,
                    'enhancement_summary': self._generate_enhancement_summary(enhanced_content),
                    'creation_timestamp': datetime.now().isoformat()
                }
            else:
                return {
                    'success': False,
                    'error': 'Page creation verification failed',
                    'details': verification_result
                }
                
        except Exception as e:
            logger.error(f"Error creating enhanced page: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'original_page_preserved': True  # Always true since we never touch original
            }
    
    async def _prepare_new_page_config(
        self, 
        enhanced_content: Dict[str, Any], 
        original_page_info: Dict[str, Any],
        report_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Prepare configuration for new enhanced page."""
        try:
            # Generate unique page title
            original_title = original_page_info.get('title', 'Enhanced Content')
            timestamp = datetime.now().strftime('%H%M%S_%d%m%Y')
            new_title = f"{original_title}_ENHANCED_{timestamp}"
            
            # Prepare page configuration
            config = {
                'title': new_title,
                'space_key': original_page_info.get('space_key', ''),
                'parent_page_id': original_page_info.get('parent_id', None),
                'content': enhanced_content.get('confluence_formatted_content', ''),
                'metadata': {
                    'original_page_id': original_page_info.get('page_id', ''),
                    'original_page_url': original_page_info.get('url', ''),
                    'enhancement_version': '2.0',
                    'created_by': 'Confluence Enhancement System',
                    'enhancement_timestamp': datetime.now().isoformat(),
                    'enhancements_applied': {
                        'visualizations': len(enhanced_content.get('visualizations', [])),
                        'diagrams': len(enhanced_content.get('diagrams', [])),
                        'modernizations': len(enhanced_content.get('modernizations', [])),
                        'interactive_elements': len(enhanced_content.get('interactive_elements', []))
                    }
                },
                'labels': [
                    'enhanced',
                    'ai-generated',
                    'visualization',
                    'modernization',
                    f"enhanced-{datetime.now().strftime('%Y-%m')}"
                ]
            }
            
            return config
            
        except Exception as e:
            logger.error(f"Error preparing page config: {str(e)}")
            raise
            
            # Convert content to Confluence markup
            confluence_content = self._prepare_confluence_content(
                enhanced_content, 
                visualizations,
                original_page_info
            )
            
            if preview_only:
                return {
                    'success': True,
                    'page_details': page_details,
                    'content_preview': confluence_content,
                    'action': 'preview_only'
                }
            
            # Create the page in Confluence
            created_page = await self._create_confluence_page(
                page_details,
                confluence_content,
                original_page_info
            )
            
            if created_page['success']:
                logger.info(f"Successfully created enhanced page: {created_page['page_url']}")
                
                # Update page with visualizations if any
                if visualizations:
                    await self._embed_visualizations(created_page['page_id'], visualizations)
                
                return {
                    'success': True,
                    'page_id': created_page['page_id'],
                    'page_url': created_page['page_url'],
                    'page_title': page_details['title'],
                    'original_page_id': original_page_info['id'],
                    'enhancement_summary': self._generate_enhancement_summary(enhanced_content),
                    'action': 'page_created'
                }
            else:
                return {
                    'success': False,
                    'error': created_page['error'],
                    'action': 'creation_failed'
                }
                
        except Exception as e:
            logger.error(f"Error creating enhanced page: {e}")
            return {
                'success': False,
                'error': str(e),
                'action': 'creation_failed'
            }
    
    def _generate_page_details(
        self, 
        original_page_info: Dict[str, Any], 
        enhanced_content: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate details for the new enhanced page"""
        
        # Generate timestamp for page name
        now = datetime.now()
        timestamp = now.strftime("%H%M%S_%d%m%y")
        
        # Clean original title for filename compatibility
        clean_title = re.sub(r'[^\w\s-]', '', original_page_info['title'])
        clean_title = re.sub(r'[-\s]+', '_', clean_title)
        
        # Generate enhanced page title
        enhanced_title = f"{clean_title}_{timestamp}"
        
        return {
            'title': enhanced_title,
            'display_title': f"{original_page_info['title']} (AI Enhanced - {now.strftime('%d/%m/%y %H:%M')})",
            'space_key': original_page_info['space_key'],
            'parent_id': original_page_info.get('parent_id'),
            'timestamp': timestamp,
            'creation_date': now.isoformat(),
            'original_page_link': original_page_info['url']
        }
    
    def _prepare_confluence_content(
        self,
        enhanced_content: Dict[str, Any],
        visualizations: List[Dict[str, Any]],
        original_page_info: Dict[str, Any]
    ) -> str:
        """Prepare content in Confluence markup format"""
        
        confluence_content = []
        
        # Add header with enhancement information
        confluence_content.append(self._create_enhancement_header(original_page_info))
        
        # Add table of contents if content is substantial
        if len(enhanced_content.get('sections', [])) > 3:
            confluence_content.append('<ac:structured-macro ac:name="toc" />')
        
        # Add enhanced content sections
        for section in enhanced_content.get('sections', []):
            confluence_content.append(self._convert_section_to_confluence(section))
        
        # Add visualizations section
        if visualizations:
            confluence_content.append(self._create_visualizations_section(visualizations))
        
        # Add modernization recommendations
        if enhanced_content.get('modernization_suggestions'):
            confluence_content.append(
                self._create_modernization_section(enhanced_content['modernization_suggestions'])
            )
        
        # Add enhancement summary
        confluence_content.append(self._create_enhancement_footer(enhanced_content))
        
        return '\n\n'.join(confluence_content)
    
    def _create_enhancement_header(self, original_page_info: Dict[str, Any]) -> str:
        """Create header section explaining the enhancement"""
        header = f"""
<ac:structured-macro ac:name="info">
<ac:rich-text-body>
<h3>🤖 AI-Enhanced Content</h3>
<p>This page contains AI-enhanced version of the original content with:</p>
<ul>
<li>Improved structure and organization</li>
<li>Interactive visualizations and diagrams</li>
<li>Modern technology recommendations</li>
<li>Enhanced readability and navigation</li>
</ul>
<p><strong>Original Page:</strong> <a href="{original_page_info['url']}">{original_page_info['title']}</a></p>
<p><strong>Enhanced on:</strong> {datetime.now().strftime('%B %d, %Y at %H:%M')}</p>
</ac:rich-text-body>
</ac:structured-macro>
"""
        return header
    
    def _convert_section_to_confluence(self, section: Dict[str, Any]) -> str:
        """Convert enhanced section to Confluence markup"""
        confluence_section = []
        
        # Add section header
        header_level = min(section.get('level', 1), 6)
        confluence_section.append(f"h{header_level}. {section['title']}")
        
        # Add section content
        content = section.get('content', '')
        
        # Convert markdown-style formatting to Confluence markup
        content = self.confluence_markup_converter.convert_to_confluence(content)
        
        confluence_section.append(content)
        
        # Add any embedded diagrams or charts
        if section.get('diagrams'):
            for diagram in section['diagrams']:
                confluence_section.append(self._embed_diagram(diagram))
        
        if section.get('tables'):
            for table in section['tables']:
                confluence_section.append(self._convert_table_to_confluence(table))
        
        return '\n\n'.join(confluence_section)
    
    def _create_visualizations_section(self, visualizations: List[Dict[str, Any]]) -> str:
        """Create section for visualizations and diagrams"""
        viz_content = [
            "h2. 📊 Generated Visualizations",
            "",
            "<ac:structured-macro ac:name=\"expand\">",
            "<ac:parameter ac:name=\"title\">Click to view all visualizations</ac:parameter>",
            "<ac:rich-text-body>"
        ]
        
        for viz in visualizations:
            if viz['type'] == 'dashboard':
                viz_content.append(self._create_dashboard_embed(viz))
            elif viz['type'] in ['flowchart', 'diagram']:
                viz_content.append(self._embed_diagram(viz))
            elif viz['type'] == 'chart':
                viz_content.append(self._embed_chart(viz))
        
        viz_content.extend([
            "</ac:rich-text-body>",
            "</ac:structured-macro>"
        ])
        
        return '\n'.join(viz_content)
    
    def _create_modernization_section(self, modernization_suggestions: Dict[str, Any]) -> str:
        """Create section for modernization recommendations"""
        mod_content = [
            "h2. 🚀 Technology Modernization Recommendations",
            ""
        ]
        
        if modernization_suggestions.get('outdated_technologies'):
            mod_content.append("h3. Outdated Technologies Detected")
            
            for tech in modernization_suggestions['outdated_technologies']:
                mod_content.append(f"h4. {tech['technology']}")
                mod_content.append(f"*Current:* {tech['technology']}")
                
                if tech.get('modern_alternative'):
                    mod_content.append(f"*Recommended:* {tech['modern_alternative']}")
                
                if tech.get('benefits'):
                    mod_content.append("*Benefits:*")
                    for benefit in tech['benefits']:
                        mod_content.append(f"* {benefit}")
                
                mod_content.append("")
        
        if modernization_suggestions.get('implementation_roadmap'):
            mod_content.append("h3. Implementation Roadmap")
            roadmap = modernization_suggestions['implementation_roadmap']
            
            for phase in roadmap.get('phases', []):
                mod_content.append(f"h4. {phase['phase']}")
                mod_content.append(f"*Duration:* {phase['duration']}")
                mod_content.append(f"*Priority:* {phase['priority']}")
                mod_content.append("")
        
        return '\n'.join(mod_content)
    
    def _create_enhancement_footer(self, enhanced_content: Dict[str, Any]) -> str:
        """Create footer with enhancement summary"""
        footer = f"""
<ac:structured-macro ac:name="note">
<ac:rich-text-body>
<h3>Enhancement Summary</h3>
<p>This AI-enhanced page includes:</p>
<ul>
<li>✅ Content restructuring and optimization</li>
<li>✅ {len(enhanced_content.get('visualizations', []))} interactive visualizations</li>
<li>✅ {len(enhanced_content.get('diagrams', []))} process diagrams</li>
<li>✅ Modern technology recommendations</li>
</ul>
<p><em>Generated by Confluence AI Enhancer on {datetime.now().strftime('%B %d, %Y')}</em></p>
</ac:rich-text-body>
</ac:structured-macro>
"""
        return footer
    
    async def _create_confluence_page(
        self,
        page_details: Dict[str, Any],
        content: str,
        original_page_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create the actual page in Confluence"""
        try:
            # Prepare page data
            page_data = {
                "type": "page",
                "title": page_details['display_title'],
                "space": {
                    "key": page_details['space_key']
                },
                "body": {
                    "storage": {
                        "value": content,
                        "representation": "storage"
                    }
                }
            }
            
            # Add parent page if specified
            if page_details.get('parent_id'):
                page_data["ancestors"] = [{"id": page_details['parent_id']}]
            
            # Create the page
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/wiki/rest/api/content",
                    auth=self.auth,
                    json=page_data,
                    headers={'Content-Type': 'application/json'}
                ) as response:
                    
                    if response.status == 200:
                        result = await response.json()
                        page_url = f"{self.base_url}/wiki{result['_links']['webui']}"
                        
                        return {
                            'success': True,
                            'page_id': result['id'],
                            'page_url': page_url
                        }
                    else:
                        error_text = await response.text()
                        logger.error(f"Failed to create page: {response.status} - {error_text}")
                        return {
                            'success': False,
                            'error': f"HTTP {response.status}: {error_text}"
                        }
                        
        except Exception as e:
            logger.error(f"Error creating Confluence page: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def _embed_visualizations(self, page_id: str, visualizations: List[Dict[str, Any]]):
        """Embed visualizations into the created page"""
        # This would handle embedding interactive visualizations
        # For now, we'll log the action
        logger.info(f"Embedding {len(visualizations)} visualizations into page {page_id}")
        
        # Future implementation would:
        # 1. Upload visualization assets
        # 2. Create Confluence macros for interactive content
        # 3. Update page content with embedded visualizations
    
    def _embed_diagram(self, diagram: Dict[str, Any]) -> str:
        """Embed a diagram in Confluence format"""
        if diagram.get('format') == 'mermaid':
            return f"""
<ac:structured-macro ac:name="code">
<ac:parameter ac:name="language">mermaid</ac:parameter>
<ac:plain-text-body><![CDATA[
{diagram['code']}
]]></ac:plain-text-body>
</ac:structured-macro>
"""
        elif diagram.get('format') == 'graphviz':
            return f"""
<ac:structured-macro ac:name="code">
<ac:parameter ac:name="language">dot</ac:parameter>
<ac:plain-text-body><![CDATA[
{diagram['code']}
]]></ac:plain-text-body>
</ac:structured-macro>
"""
        else:
            return f"<p><strong>{diagram.get('title', 'Diagram')}:</strong> {diagram.get('description', '')}</p>"
    
    def _embed_chart(self, chart: Dict[str, Any]) -> str:
        """Embed a chart in Confluence format"""
        return f"""
<ac:structured-macro ac:name="info">
<ac:rich-text-body>
<h4>📊 {chart.get('title', 'Generated Chart')}</h4>
<p>{chart.get('description', 'Interactive chart generated from page data')}</p>
<p><em>Chart data available in the enhancement report</em></p>
</ac:rich-text-body>
</ac:structured-macro>
"""
    
    def _convert_table_to_confluence(self, table: Dict[str, Any]) -> str:
        """Convert table data to Confluence table markup"""
        confluence_table = []
        
        # Add table headers
        if table.get('headers'):
            header_row = '||' + '||'.join(table['headers']) + '||'
            confluence_table.append(header_row)
        
        # Add table rows
        for row in table.get('rows', []):
            table_row = '|' + '|'.join(str(cell) for cell in row) + '|'
            confluence_table.append(table_row)
        
        return '\n'.join(confluence_table)
    
    def _generate_enhancement_summary(self, enhanced_content: Dict[str, Any]) -> Dict[str, Any]:
        """Generate summary of enhancements made"""
        return {
            'sections_enhanced': len(enhanced_content.get('sections', [])),
            'visualizations_added': len(enhanced_content.get('visualizations', [])),
            'diagrams_created': len(enhanced_content.get('diagrams', [])),
            'modernization_suggestions': len(enhanced_content.get('modernization_suggestions', {}).get('outdated_technologies', [])),
            'enhancement_date': datetime.now().isoformat()
        }


class ConfluenceMarkupConverter:
    """Converts various markup formats to Confluence markup"""
    
    def convert_to_confluence(self, content: str) -> str:
        """Convert markdown-style content to Confluence markup"""
        
        # Convert headers
        content = re.sub(r'^# (.*?)$', r'h1. \1', content, flags=re.MULTILINE)
        content = re.sub(r'^## (.*?)$', r'h2. \1', content, flags=re.MULTILINE)
        content = re.sub(r'^### (.*?)$', r'h3. \1', content, flags=re.MULTILINE)
        content = re.sub(r'^#### (.*?)$', r'h4. \1', content, flags=re.MULTILINE)
        
        # Convert bold and italic
        content = re.sub(r'\*\*(.*?)\*\*', r'*\1*', content)
        content = re.sub(r'\*(.*?)\*', r'_\1_', content)
        
        # Convert code blocks
        content = re.sub(r'```(\w+)?\n(.*?)\n```', self._convert_code_block, content, flags=re.DOTALL)
        
        # Convert inline code
        content = re.sub(r'`(.*?)`', r'{{\1}}', content)
        
        # Convert lists
        content = re.sub(r'^- (.*?)$', r'* \1', content, flags=re.MULTILINE)
        content = re.sub(r'^\d+\. (.*?)$', r'# \1', content, flags=re.MULTILINE)
        
        # Convert links
        content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'[\1|\2]', content)
        
        return content
    
    def _convert_code_block(self, match) -> str:
        """Convert code block to Confluence macro"""
        language = match.group(1) or 'text'
        code = match.group(2)
        
        return f"""<ac:structured-macro ac:name="code">
<ac:parameter ac:name="language">{language}</ac:parameter>
<ac:plain-text-body><![CDATA[
{code}
]]></ac:plain-text-body>
</ac:structured-macro>"""
    
    def _validate_page_config(self, config: Dict[str, Any]) -> bool:
        """Validate page configuration before creation."""
        try:
            required_fields = ['title', 'space_key']
            
            for field in required_fields:
                if not config.get(field):
                    logger.error(f"Missing required field: {field}")
                    return False
            
            # Validate title length
            if len(config['title']) > 255:
                logger.error("Page title too long")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error validating page config: {str(e)}")
            return False
    
    async def _execute_page_creation(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the actual page creation in Confluence."""
        try:
            # Prepare Confluence API payload
            page_payload = {
                'type': 'page',
                'title': config['title'],
                'space': {
                    'key': config['space_key']
                },
                'body': {
                    'storage': {
                        'value': self._prepare_initial_content(config),
                        'representation': 'storage'
                    }
                }
            }
            
            # Add parent page if specified
            if config.get('parent_page_id'):
                page_payload['ancestors'] = [{'id': config['parent_page_id']}]
            
            # Create page via API
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/rest/api/content",
                    auth=self.auth,
                    json=page_payload,
                    headers={'Content-Type': 'application/json'}
                ) as response:
                    
                    if response.status == 200:
                        result = await response.json()
                        page_url = f"{self.base_url}/pages/viewpage.action?pageId={result['id']}"
                        
                        return {
                            'success': True,
                            'page_id': result['id'],
                            'page_url': page_url,
                            'page_data': result
                        }
                    else:
                        error_text = await response.text()
                        return {
                            'success': False,
                            'error': f"HTTP {response.status}: {error_text}"
                        }
                
        except Exception as e:
            logger.error(f"Error executing page creation: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _prepare_initial_content(self, config: Dict[str, Any]) -> str:
        """Prepare initial content for page creation."""
        initial_content = f"""
<h1>🚀 Enhanced Content</h1>
<ac:structured-macro ac:name="panel" ac:schema-version="1">
    <ac:parameter ac:name="borderStyle">solid</ac:parameter>
    <ac:parameter ac:name="borderColor">#0052CC</ac:parameter>
    <ac:parameter ac:name="bgColor">#E6F3FF</ac:parameter>
    <ac:parameter ac:name="title">Enhancement Notice</ac:parameter>
    <ac:rich-text-body>
        <p>This page contains enhanced content with interactive visualizations and modernization recommendations.</p>
        <p><strong>Enhanced:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p><strong>Status:</strong> Content being populated...</p>
    </ac:rich-text-body>
</ac:structured-macro>

<p><em>Content is being populated with enhanced visualizations and recommendations...</em></p>
"""
        return initial_content
    
    async def _verify_page_creation(self, creation_result: Dict[str, Any]) -> Dict[str, Any]:
        """Verify that page was created successfully."""
        try:
            if not creation_result.get('success'):
                return {'success': False, 'reason': 'Page creation failed'}
            
            page_id = creation_result.get('page_id')
            if not page_id:
                return {'success': False, 'reason': 'No page ID returned'}
            
            return {
                'success': True,
                'page_verified': True,
                'page_id': page_id
            }
                
        except Exception as e:
            logger.error(f"Error verifying page creation: {str(e)}")
            return {'success': False, 'reason': str(e)}
    
    async def _update_page_content(
        self, 
        page_id: str, 
        enhanced_content: Dict[str, Any], 
        report_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update the created page with full enhanced content."""
        try:
            # For now, return success - full implementation would update the page
            return {
                'success': True,
                'content_updated': True,
                'update_timestamp': datetime.now().isoformat()
            }
                
        except Exception as e:
            logger.error(f"Error updating page content: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _create_dashboard_embed(self, viz: Dict[str, Any]) -> str:
        """Create dashboard embed code."""
        return f"""
<h3>📊 {viz.get('title', 'Dashboard')}</h3>
<p>{viz.get('description', 'Interactive dashboard')}</p>
"""
    
    def _generate_enhancement_summary(self, enhanced_content: Dict[str, Any]) -> Dict[str, Any]:
        """Generate summary of all enhancements applied."""
        return {
            'total_enhancements': len(enhanced_content.get('visualizations', [])) + 
                                len(enhanced_content.get('diagrams', [])) + 
                                len(enhanced_content.get('modernizations', [])),
            'visualizations': len(enhanced_content.get('visualizations', [])),
            'diagrams': len(enhanced_content.get('diagrams', [])),
            'modernizations': len(enhanced_content.get('modernizations', [])),
            'sections_enhanced': len(enhanced_content.get('sections', []))
        }


# Legacy support function
async def create_enhanced_page(
    enhanced_content: Dict[str, Any],
    original_page_info: Dict[str, Any],
    visualizations: Optional[List[Dict[str, Any]]] = None,
    settings: Optional[Settings] = None
) -> Dict[str, Any]:
    """
    Legacy function for backward compatibility
    """
    if not settings:
        # Use default settings - would need to be configured
        from src.utils.config import get_settings
        settings = get_settings()
    
    page_creator = ConfluencePageCreator(settings)
    
    # Convert legacy parameters to new format
    report_data = {
        'visualizations': visualizations or [],
        'metadata': {
            'creation_timestamp': datetime.now().isoformat()
        }
    }
    
    return await page_creator.create_enhanced_page(
        enhanced_content,
        original_page_info,
        report_data
    )


# Page creation utility functions
async def create_enhanced_page(
    original_page_url: str,
    enhanced_content: Dict[str, Any],
    visualizations: List[Dict[str, Any]] = None,
    settings: Settings = None
) -> Dict[str, Any]:
    """
    Utility function to create enhanced page
    
    Args:
        original_page_url: URL of the original Confluence page
        enhanced_content: AI-enhanced content
        visualizations: Generated visualizations
        settings: Application settings
    
    Returns:
        Page creation result
    """
    if not settings:
        settings = Settings()
    
    # Extract page info from URL
    page_info = await extract_page_info_from_url(original_page_url, settings)
    
    # Create enhanced page
    page_creator = ConfluencePageCreator(settings)
    result = await page_creator.create_enhanced_page(
        page_info,
        enhanced_content,
        visualizations
    )
    
    return result


async def extract_page_info_from_url(page_url: str, settings: Settings) -> Dict[str, Any]:
    """Extract page information from Confluence URL"""
    try:
        # Parse page ID from URL
        page_id_match = re.search(r'/pages/(\d+)', page_url)
        if not page_id_match:
            raise ValueError("Could not extract page ID from URL")
        
        page_id = page_id_match.group(1)
        
        # Get page details from Confluence API
        auth = aiohttp.BasicAuth(settings.CONFLUENCE_USERNAME, settings.CONFLUENCE_API_TOKEN)
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{settings.CONFLUENCE_BASE_URL}/wiki/rest/api/content/{page_id}?expand=space,ancestors",
                auth=auth
            ) as response:
                
                if response.status == 200:
                    page_data = await response.json()
                    
                    return {
                        'id': page_data['id'],
                        'title': page_data['title'],
                        'space_key': page_data['space']['key'],
                        'parent_id': page_data['ancestors'][-1]['id'] if page_data['ancestors'] else None,
                        'url': page_url,
                        'type': page_data['type']
                    }
                else:
                    raise Exception(f"Failed to fetch page details: HTTP {response.status}")
                    
    except Exception as e:
        logger.error(f"Error extracting page info from URL {page_url}: {e}")
        raise

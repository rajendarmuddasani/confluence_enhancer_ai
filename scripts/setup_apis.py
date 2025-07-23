"""
API Configuration and Credential Management for Confluence Enhancer
"""
import os
import logging
from typing import Dict, Optional, Any
import asyncio
import aiohttp
from dataclasses import dataclass
from src.utils.config import Settings

logger = logging.getLogger(__name__)


@dataclass
class APICredentials:
    """API credentials container"""
    service_name: str
    api_key: str
    base_url: str
    additional_params: Dict[str, Any]
    is_valid: bool = False
    last_validated: Optional[str] = None


class APIConfigurationService:
    """Manage and validate API configurations"""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.credentials: Dict[str, APICredentials] = {}
        self._initialize_credentials()
    
    def _initialize_credentials(self):
        """Initialize API credentials from settings"""
        
        # OpenAI Configuration
        if self.settings.OPENAI_API_KEY:
            self.credentials['openai'] = APICredentials(
                service_name='OpenAI',
                api_key=self.settings.OPENAI_API_KEY,
                base_url='https://api.openai.com/v1',
                additional_params={
                    'model': getattr(self.settings, 'OPENAI_MODEL', 'gpt-4'),
                    'max_tokens': getattr(self.settings, 'OPENAI_MAX_TOKENS', 4000),
                    'temperature': getattr(self.settings, 'OPENAI_TEMPERATURE', 0.3)
                }
            )
        
        # Anthropic Configuration
        if self.settings.ANTHROPIC_API_KEY:
            self.credentials['anthropic'] = APICredentials(
                service_name='Anthropic',
                api_key=self.settings.ANTHROPIC_API_KEY,
                base_url='https://api.anthropic.com/v1',
                additional_params={
                    'model': getattr(self.settings, 'ANTHROPIC_MODEL', 'claude-3-sonnet-20240229'),
                    'max_tokens': getattr(self.settings, 'ANTHROPIC_MAX_TOKENS', 4000)
                }
            )
        
        # Confluence Configuration
        if self.settings.CONFLUENCE_BASE_URL and self.settings.CONFLUENCE_API_TOKEN:
            self.credentials['confluence'] = APICredentials(
                service_name='Confluence',
                api_key=self.settings.CONFLUENCE_API_TOKEN,
                base_url=self.settings.CONFLUENCE_BASE_URL,
                additional_params={
                    'username': self.settings.CONFLUENCE_USERNAME,
                    'auth_type': 'api_token'
                }
            )
    
    async def validate_openai_api(self) -> bool:
        """Validate OpenAI API connection"""
        try:
            if 'openai' not in self.credentials:
                logger.error("OpenAI credentials not configured")
                return False
            
            creds = self.credentials['openai']
            headers = {
                'Authorization': f'Bearer {creds.api_key}',
                'Content-Type': 'application/json'
            }
            
            async with aiohttp.ClientSession() as session:
                # Test with a simple models list request
                async with session.get(
                    f"{creds.base_url}/models",
                    headers=headers,
                    timeout=10
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        logger.info(f"OpenAI API validated successfully. Available models: {len(data.get('data', []))}")
                        creds.is_valid = True
                        return True
                    else:
                        logger.error(f"OpenAI API validation failed: {response.status}")
                        return False
        
        except Exception as e:
            logger.error(f"OpenAI API validation error: {e}")
            return False
    
    async def validate_confluence_api(self) -> bool:
        """Validate Confluence API connection"""
        try:
            if 'confluence' not in self.credentials:
                logger.error("Confluence credentials not configured")
                return False
            
            creds = self.credentials['confluence']
            auth = aiohttp.BasicAuth(
                creds.additional_params['username'],
                creds.api_key
            )
            
            async with aiohttp.ClientSession() as session:
                # Test with user info request
                async with session.get(
                    f"{creds.base_url}/wiki/rest/api/user/current",
                    auth=auth,
                    timeout=10
                ) as response:
                    if response.status == 200:
                        user_data = await response.json()
                        logger.info(f"Confluence API validated successfully. User: {user_data.get('displayName', 'Unknown')}")
                        creds.is_valid = True
                        return True
                    else:
                        logger.error(f"Confluence API validation failed: {response.status}")
                        return False
        
        except Exception as e:
            logger.error(f"Confluence API validation error: {e}")
            return False
    
    async def validate_anthropic_api(self) -> bool:
        """Validate Anthropic API connection"""
        try:
            if 'anthropic' not in self.credentials:
                logger.warning("Anthropic credentials not configured (optional)")
                return True  # Optional service
            
            creds = self.credentials['anthropic']
            headers = {
                'x-api-key': creds.api_key,
                'Content-Type': 'application/json',
                'anthropic-version': '2023-06-01'
            }
            
            # Test with a simple message request
            test_payload = {
                'model': creds.additional_params['model'],
                'max_tokens': 10,
                'messages': [{'role': 'user', 'content': 'Hello'}]
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{creds.base_url}/messages",
                    headers=headers,
                    json=test_payload,
                    timeout=10
                ) as response:
                    if response.status == 200:
                        logger.info("Anthropic API validated successfully")
                        creds.is_valid = True
                        return True
                    else:
                        logger.error(f"Anthropic API validation failed: {response.status}")
                        return False
        
        except Exception as e:
            logger.error(f"Anthropic API validation error: {e}")
            return False
    
    async def validate_all_apis(self) -> Dict[str, bool]:
        """Validate all configured APIs"""
        results = {}
        
        # Validate APIs concurrently
        tasks = [
            ('openai', self.validate_openai_api()),
            ('confluence', self.validate_confluence_api()),
            ('anthropic', self.validate_anthropic_api())
        ]
        
        for service_name, task in tasks:
            try:
                results[service_name] = await task
            except Exception as e:
                logger.error(f"Error validating {service_name}: {e}")
                results[service_name] = False
        
        return results
    
    def get_api_status(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all configured APIs"""
        status = {}
        
        for service_name, creds in self.credentials.items():
            status[service_name] = {
                'configured': bool(creds.api_key),
                'valid': creds.is_valid,
                'base_url': creds.base_url,
                'last_validated': creds.last_validated,
                'additional_info': {
                    k: v for k, v in creds.additional_params.items()
                    if k not in ['api_key', 'password', 'secret']
                }
            }
        
        return status
    
    def get_required_environment_variables(self) -> Dict[str, Dict[str, Any]]:
        """Get list of required environment variables with current status"""
        required_vars = {
            'OPENAI_API_KEY': {
                'description': 'OpenAI API key for AI content analysis',
                'required': True,
                'configured': bool(self.settings.OPENAI_API_KEY),
                'example': 'sk-...',
                'help_url': 'https://platform.openai.com/api-keys'
            },
            'CONFLUENCE_BASE_URL': {
                'description': 'Base URL for your Confluence instance',
                'required': True,
                'configured': bool(self.settings.CONFLUENCE_BASE_URL),
                'example': 'https://your-company.atlassian.net',
                'help_url': 'https://support.atlassian.com/atlassian-account/docs/manage-api-tokens-for-your-atlassian-account/'
            },
            'CONFLUENCE_API_TOKEN': {
                'description': 'Confluence API token for authentication',
                'required': True,
                'configured': bool(self.settings.CONFLUENCE_API_TOKEN),
                'example': 'ATT...',
                'help_url': 'https://support.atlassian.com/atlassian-account/docs/manage-api-tokens-for-your-atlassian-account/'
            },
            'CONFLUENCE_USERNAME': {
                'description': 'Your Confluence username/email',
                'required': True,
                'configured': bool(self.settings.CONFLUENCE_USERNAME),
                'example': 'user@company.com',
                'help_url': None
            },
            'ORACLE_HOST': {
                'description': 'Oracle database host',
                'required': True,
                'configured': bool(self.settings.ORACLE_HOST),
                'example': 'localhost',
                'help_url': 'https://docs.oracle.com/en/database/oracle/oracle-database/'
            },
            'ORACLE_PASSWORD': {
                'description': 'Oracle database password',
                'required': True,
                'configured': bool(self.settings.ORACLE_PASSWORD),
                'example': 'your_password',
                'help_url': None
            },
            'SECRET_KEY': {
                'description': 'Secret key for JWT token generation',
                'required': True,
                'configured': bool(self.settings.SECRET_KEY and self.settings.SECRET_KEY != 'your-secret-key-here'),
                'example': 'your-32-character-secret-key',
                'help_url': None
            },
            'ANTHROPIC_API_KEY': {
                'description': 'Anthropic API key (optional backup AI)',
                'required': False,
                'configured': bool(self.settings.ANTHROPIC_API_KEY),
                'example': 'sk-ant-...',
                'help_url': 'https://docs.anthropic.com/claude/reference/getting-started-with-the-api'
            }
        }
        
        return required_vars


class SetupWizard:
    """Interactive setup wizard for API configuration"""
    
    def __init__(self):
        self.api_service = APIConfigurationService(Settings())
    
    def display_welcome(self):
        """Display welcome message"""
        print("🚀 Confluence Enhancer AI - Setup Wizard")
        print("=" * 50)
        print("This wizard will help you configure the external services")
        print("required for the Confluence Enhancer AI system.")
        print()
    
    def display_requirements(self):
        """Display configuration requirements"""
        print("📋 Required Configuration:")
        print("-" * 30)
        
        required_vars = self.api_service.get_required_environment_variables()
        
        for var_name, var_info in required_vars.items():
            status = "✅" if var_info['configured'] else "❌"
            required_text = "Required" if var_info['required'] else "Optional"
            
            print(f"{status} {var_name} ({required_text})")
            print(f"   {var_info['description']}")
            if var_info['help_url']:
                print(f"   Help: {var_info['help_url']}")
            print()
    
    async def test_connections(self):
        """Test API connections"""
        print("🔧 Testing API Connections:")
        print("-" * 30)
        
        results = await self.api_service.validate_all_apis()
        
        for service, is_valid in results.items():
            status = "✅ Connected" if is_valid else "❌ Failed"
            print(f"{service.title()}: {status}")
        
        print()
        
        # Display overall status
        all_required_valid = results.get('openai', False) and results.get('confluence', False)
        
        if all_required_valid:
            print("🎉 All required services are configured and connected!")
            print("You're ready to proceed with Phase 2 integration.")
        else:
            print("⚠️  Some required services are not properly configured.")
            print("Please check your .env file and API credentials.")
        
        return all_required_valid
    
    def display_next_steps(self):
        """Display next steps"""
        print("📝 Next Steps:")
        print("-" * 15)
        print("1. Copy .env.development to .env and fill in your credentials")
        print("2. Run: python scripts/setup_database.py")
        print("3. Run: python main.py (to start the backend)")
        print("4. Run: cd frontend && npm install && npm run dev")
        print("5. Open http://localhost:3000 in your browser")
        print()


async def main():
    """Main setup function"""
    wizard = SetupWizard()
    
    wizard.display_welcome()
    wizard.display_requirements()
    
    print("Testing current configuration...")
    await wizard.test_connections()
    
    wizard.display_next_steps()


if __name__ == "__main__":
    asyncio.run(main())

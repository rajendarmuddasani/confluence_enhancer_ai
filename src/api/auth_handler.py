"""
Authentication handler for Confluence API
"""
import logging
from typing import Optional, Dict, Any
import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext

from ..utils.config import settings


logger = logging.getLogger(__name__)


class AuthHandler:
    """Handle authentication for Confluence API and application"""
    
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.secret_key = settings.SECRET_KEY
        self.algorithm = "HS256"
        self.access_token_expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
    
    def verify_confluence_credentials(self, username: str, api_token: str) -> bool:
        """Verify Confluence API credentials"""
        try:
            from .confluence_client import ConfluenceClient
            
            client = ConfluenceClient(
                base_url=settings.CONFLUENCE_BASE_URL,
                username=username,
                api_token=api_token
            )
            
            return client.validate_connection()
            
        except Exception as e:
            logger.error(f"Error verifying Confluence credentials: {e}")
            return False
    
    def create_access_token(self, data: Dict[str, Any]) -> str:
        """Create JWT access token"""
        try:
            to_encode = data.copy()
            expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
            to_encode.update({"exp": expire})
            
            encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
            return encoded_jwt
            
        except Exception as e:
            logger.error(f"Error creating access token: {e}")
            return ""
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
            
        except jwt.ExpiredSignatureError:
            logger.warning("Token has expired")
            return None
        except jwt.JWTError as e:
            logger.error(f"JWT error: {e}")
            return None
    
    def hash_password(self, password: str) -> str:
        """Hash password"""
        return self.pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate user (placeholder for user management)"""
        # This is a placeholder - in a real application, you'd check against a user database
        # For now, we'll use a simple check
        if username == "admin" and password == "admin":
            return {
                "username": username,
                "email": f"{username}@example.com",
                "is_active": True
            }
        return None

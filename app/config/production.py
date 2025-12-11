"""
Production environment configuration
"""
from .base import BaseConfig


class ProductionConfig(BaseConfig):
    """Production environment specific configuration"""
    
    # Flask
    DEBUG = False
    TESTING = False
    
    # Database - no logging in production
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_RECORD_QUERIES = False
    
    # Session - maximum security
    SESSION_COOKIE_SECURE = True  # HTTPS only
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Strict'
    
    # CSRF - enabled and strict
    WTF_CSRF_ENABLED = True
    WTF_CSRF_SSL_STRICT = True
    
    # Security Headers
    SEND_FILE_MAX_AGE_DEFAULT = 31536000  # 1 year for static files
    
    # Logging
    LOG_LEVEL = 'WARNING'
    
    # Production specific
    PREFERRED_URL_SCHEME = 'https'
    
    # Error handling
    PROPAGATE_EXCEPTIONS = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False

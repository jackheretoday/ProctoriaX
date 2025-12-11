"""
Testing environment configuration
"""
from .base import BaseConfig


class TestingConfig(BaseConfig):
    """Testing environment specific configuration"""
    
    # Flask
    DEBUG = True
    TESTING = True
    
    # Database - use in-memory SQLite for tests
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_ECHO = False
    
    # Session - simplified for testing
    SESSION_COOKIE_SECURE = False
    WTF_CSRF_ENABLED = False
    
    # Disable rate limiting in tests
    RATELIMIT_ENABLED = False
    
    # Logging - minimal in tests
    LOG_LEVEL = 'ERROR'
    
    # Fast password hashing for tests
    BCRYPT_LOG_ROUNDS = 4
    
    # Testing specific
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SERVER_NAME = 'localhost:5000'

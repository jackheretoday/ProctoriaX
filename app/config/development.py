"""
Development environment configuration
"""
from .base import BaseConfig


class DevelopmentConfig(BaseConfig):
    """Development environment specific configuration"""
    
    # Flask
    DEBUG = True
    TESTING = False
    
    # Database - more verbose logging
    SQLALCHEMY_ECHO = True
    
    # Session - less secure for development
    SESSION_COOKIE_SECURE = False  # Allow HTTP for local development
    
    # CSRF - disabled for easier testing (enable in production)
    WTF_CSRF_ENABLED = False
    
    # Debug Toolbar
    DEBUG_TB_ENABLED = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    
    # Logging
    LOG_LEVEL = 'DEBUG'
    
    # Development specific
    TEMPLATES_AUTO_RELOAD = True
    EXPLAIN_TEMPLATE_LOADING = False

"""
Base configuration class
All environments inherit from this
"""
import os
from datetime import timedelta


class BaseConfig:
    """Base configuration with common settings"""
    
    # Flask Core
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Database
    # Use absolute path to avoid database connection issues
    # Get the project root directory (app/config/base.py -> app -> project root)
    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    DB_PATH = os.path.join(BASE_DIR, 'instance', 'testing_platform.db')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', f'sqlite:///{DB_PATH}')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_RECORD_QUERIES = True
    
    # Session Configuration
    SESSION_TYPE = os.getenv('SESSION_TYPE', 'filesystem')
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    PERMANENT_SESSION_LIFETIME = timedelta(
        seconds=int(os.getenv('PERMANENT_SESSION_LIFETIME', 3600))
    )
    SESSION_COOKIE_NAME = 'testing_platform_session'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Security
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None
    
    # File Upload
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 10485760))  # 10MB
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'storage/uploads')
    ALLOWED_EXTENSIONS = {
        'docx', 'pptx', 'xlsx', 'doc', 'ppt', 'xls'
    }
    
    # Encryption
    ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY', 'change-this-encryption-key-32b')
    
    # Application Settings
    ORGANIZATION_NAME = os.getenv('ORGANIZATION_NAME', 'ProctoriaX')
    MAX_TERMS_BULLETS = int(os.getenv('MAX_TERMS_BULLETS', 10))
    PASSWORD_MIN_LENGTH = int(os.getenv('PASSWORD_MIN_LENGTH', 8))
    
    # Rate Limiting
    RATELIMIT_STORAGE_URL = os.getenv('RATELIMIT_STORAGE_URL', 'memory://')
    RATELIMIT_STRATEGY = os.getenv('RATELIMIT_STRATEGY', 'fixed-window')
    RATELIMIT_HEADERS_ENABLED = True
    
    # Pagination
    ITEMS_PER_PAGE = 20
    
    # Timezone
    TIMEZONE = 'UTC'
    
    # Flask-Login
    REMEMBER_COOKIE_DURATION = timedelta(days=7)
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_REFRESH_EACH_REQUEST = False
    
    # Email (optional)
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True') == 'True'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'noreply@testingplatform.com')
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = 'logs/app.log'
    SECURITY_LOG_FILE = 'logs/security.log'
    AUDIT_LOG_FILE = 'logs/audit.log'

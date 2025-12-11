"""
Security-specific configuration and constants
"""

# Password Policy
PASSWORD_MIN_LENGTH = 8
PASSWORD_REQUIRE_UPPERCASE = True
PASSWORD_REQUIRE_LOWERCASE = True
PASSWORD_REQUIRE_NUMBERS = True
PASSWORD_REQUIRE_SPECIAL = False

# Session Security
SESSION_TIMEOUT_MINUTES = 60  # 1 hour
SESSION_REFRESH_EACH_REQUEST = True
MAX_SESSION_AGE_DAYS = 7

# Rate Limiting Rules
RATE_LIMIT_LOGIN = "5 per minute"
RATE_LIMIT_API = "100 per hour"
RATE_LIMIT_FILE_UPLOAD = "10 per hour"

# Encryption
AES_MODE = 'GCM'  # Galois/Counter Mode
AES_KEY_SIZE = 256  # bits
SALT_LENGTH = 16  # bytes

# CSRF Protection
CSRF_TOKEN_LENGTH = 32
CSRF_TIME_LIMIT = 3600  # 1 hour

# File Upload Security
MAX_FILE_SIZE_MB = 10
ALLOWED_QUESTION_FORMATS = ['docx', 'pptx']
ALLOWED_EXCEL_FORMATS = ['xlsx', 'xls']
SCAN_UPLOADED_FILES = False  # Set to True if antivirus scanning available

# Login Security
MAX_LOGIN_ATTEMPTS = 5
LOGIN_LOCKOUT_DURATION_MINUTES = 15
TRACK_LOGIN_ATTEMPTS = True

# Audit Logging
LOG_ALL_ACCESS = True
LOG_FAILED_LOGINS = True
LOG_DATA_MODIFICATIONS = True
LOG_FILE_OPERATIONS = True

# Security Headers
SECURITY_HEADERS = {
    'X-Frame-Options': 'SAMEORIGIN',
    'X-Content-Type-Options': 'nosniff',
    'X-XSS-Protection': '1; mode=block',
    'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
    'Content-Security-Policy': "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';"
}

# Allowed Origins (for CORS if needed)
ALLOWED_ORIGINS = [
    'http://localhost:5000',
    'http://127.0.0.1:5000'
]

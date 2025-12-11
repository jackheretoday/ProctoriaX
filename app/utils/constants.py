"""
Application constants
"""

# User Roles
USER_ROLES = ['admin', 'teacher', 'student']
ROLE_ADMIN = 'admin'
ROLE_TEACHER = 'teacher'
ROLE_STUDENT = 'student'

# Test Status
TEST_STATUS_PENDING = 'pending'
TEST_STATUS_IN_PROGRESS = 'in_progress'
TEST_STATUS_COMPLETED = 'completed'
TEST_STATUS_EXPIRED = 'expired'

# Assignment Status
ASSIGNMENT_STATUS = [
    TEST_STATUS_PENDING,
    TEST_STATUS_IN_PROGRESS,
    TEST_STATUS_COMPLETED,
    TEST_STATUS_EXPIRED
]

# Question Difficulty
DIFFICULTY_EASY = 'easy'
DIFFICULTY_MEDIUM = 'medium'
DIFFICULTY_HARD = 'hard'

# File Upload
ALLOWED_QUESTION_FORMATS = ['docx', 'pptx', 'doc', 'ppt']
ALLOWED_EXCEL_FORMATS = ['xlsx', 'xls']
MAX_FILE_SIZE_MB = 10
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

# Terms and Conditions
MAX_TERMS_BULLETS = 10

# Password Policy
PASSWORD_MIN_LENGTH = 8
PASSWORD_REQUIRE_UPPERCASE = True
PASSWORD_REQUIRE_LOWERCASE = True
PASSWORD_REQUIRE_NUMBERS = True

# Session
SESSION_TIMEOUT_MINUTES = 60
MAX_LOGIN_ATTEMPTS = 5
LOGIN_LOCKOUT_MINUTES = 15

# Audit Actions
ACTION_LOGIN = 'login'
ACTION_LOGOUT = 'logout'
ACTION_CREATE_USER = 'create_user'
ACTION_UPDATE_USER = 'update_user'
ACTION_DELETE_USER = 'delete_user'
ACTION_CREATE_TEST = 'create_test'
ACTION_UPLOAD_QUESTIONS = 'upload_questions'
ACTION_START_TEST = 'start_test'
ACTION_SUBMIT_TEST = 'submit_test'
ACTION_VIEW_RESULTS = 'view_results'
ACTION_EXPORT_RESULTS = 'export_results'

# Pagination
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

# Encryption
AES_KEY_SIZE = 256  # bits
AES_MODE = 'GCM'

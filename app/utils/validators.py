"""
Input validation functions
"""
import re
from app.utils.constants import PASSWORD_MIN_LENGTH


def validate_email(email):
    """
    Validate email format
    
    Args:
        email: Email address
        
    Returns:
        True if valid, False otherwise
    """
    if not email:
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_password_strength(password):
    """
    Validate password strength
    
    Args:
        password: Password string
        
    Returns:
        Tuple (is_valid, error_message)
    """
    if not password:
        return False, "Password cannot be empty"
    
    if len(password) < PASSWORD_MIN_LENGTH:
        return False, f"Password must be at least {PASSWORD_MIN_LENGTH} characters"
    
    # Check for uppercase
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    # Check for lowercase
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    # Check for numbers
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    
    return True, None


def validate_username(username):
    """
    Validate username format
    
    Args:
        username: Username string
        
    Returns:
        Tuple (is_valid, error_message)
    """
    if not username:
        return False, "Username cannot be empty"
    
    if len(username) < 3:
        return False, "Username must be at least 3 characters"
    
    if len(username) > 80:
        return False, "Username must not exceed 80 characters"
    
    # Only alphanumeric and underscore
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "Username can only contain letters, numbers, and underscore"
    
    return True, None


def validate_file_extension(filename, allowed_extensions):
    """
    Validate file extension
    
    Args:
        filename: File name
        allowed_extensions: List of allowed extensions
        
    Returns:
        True if valid, False otherwise
    """
    if not filename or '.' not in filename:
        return False
    
    extension = filename.rsplit('.', 1)[1].lower()
    return extension in allowed_extensions


def validate_file_size(file, max_size_bytes):
    """
    Validate file size
    
    Args:
        file: File object
        max_size_bytes: Maximum size in bytes
        
    Returns:
        True if valid, False otherwise
    """
    if not file:
        return False
    
    # Seek to end to get file size
    file.seek(0, 2)
    size = file.tell()
    file.seek(0)  # Reset to beginning
    
    return size <= max_size_bytes


def sanitize_filename(filename):
    """
    Sanitize filename to prevent security issues
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    # Remove path components
    filename = filename.split('/')[-1].split('\\')[-1]
    
    # Remove dangerous characters
    filename = re.sub(r'[^\w\s.-]', '', filename)
    
    # Replace spaces with underscores
    filename = filename.replace(' ', '_')
    
    return filename


def validate_role(role):
    """
    Validate user role
    
    Args:
        role: Role string
        
    Returns:
        True if valid, False otherwise
    """
    from app.utils.constants import USER_ROLES
    return role in USER_ROLES

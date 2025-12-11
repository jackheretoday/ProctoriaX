"""Common validators for API inputs"""
import re
from flask import jsonify
from functools import wraps


def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password(password):
    """Validate password strength
    - Minimum 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    - At least one special character
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one digit"
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character"
    
    return True, "Password is valid"


def validate_username(username):
    """Validate username format"""
    if len(username) < 3:
        return False, "Username must be at least 3 characters"
    
    if len(username) > 50:
        return False, "Username cannot exceed 50 characters"
    
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "Username can only contain letters, numbers, and underscores"
    
    return True, "Username is valid"


def validate_test_duration(duration):
    """Validate test duration in minutes"""
    try:
        duration = int(duration)
        if duration < 1:
            return False, "Duration must be at least 1 minute"
        if duration > 300:
            return False, "Duration cannot exceed 300 minutes (5 hours)"
        return True, "Duration is valid"
    except (ValueError, TypeError):
        return False, "Duration must be a valid number"


def validate_file_upload(file, allowed_extensions, max_size_mb=10):
    """Validate file upload"""
    if not file:
        return False, "No file provided"
    
    if file.filename == '':
        return False, "No file selected"
    
    # Check extension
    ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
    if ext not in allowed_extensions:
        return False, f"File type not allowed. Allowed: {', '.join(allowed_extensions)}"
    
    # Check size
    file.seek(0, 2)  # Seek to end
    size = file.tell()
    file.seek(0)  # Reset
    
    max_size_bytes = max_size_mb * 1024 * 1024
    if size > max_size_bytes:
        return False, f"File size exceeds {max_size_mb}MB limit"
    
    return True, "File is valid"


def validate_json_request(required_fields):
    """Decorator to validate JSON request has required fields"""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            from flask import request
            
            if not request.is_json:
                return jsonify({
                    'success': False,
                    'error': 'Request must be JSON'
                }), 400
            
            data = request.get_json()
            
            missing = [field for field in required_fields if field not in data]
            if missing:
                return jsonify({
                    'success': False,
                    'error': f"Missing required fields: {', '.join(missing)}"
                }), 400
            
            return f(*args, **kwargs)
        return wrapper
    return decorator
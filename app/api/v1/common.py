"""Common API utilities and helpers"""
from flask import jsonify
from functools import wraps
from datetime import datetime


def success_response(data=None, message="Success", status=200):
    """Standard success response format"""
    response = {
        'success': True,
        'message': message
    }
    if data is not None:
        response['data'] = data
    return jsonify(response), status


def error_response(error="An error occurred", details=None, status=400):
    """Standard error response format"""
    response = {
        'success': False,
        'error': error
    }
    if details:
        response['details'] = details
    return jsonify(response), status


def paginate_query(query, page=1, per_page=20):
    """Paginate SQLAlchemy query"""
    try:
        page = int(page)
        per_page = int(per_page)
    except (ValueError, TypeError):
        page = 1
        per_page = 20
    
    if page < 1:
        page = 1
    if per_page < 1 or per_page > 100:
        per_page = 20
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return {
        'items': pagination.items,
        'total': pagination.total,
        'page': page,
        'per_page': per_page,
        'pages': pagination.pages,
        'has_next': pagination.has_next,
        'has_prev': pagination.has_prev
    }


def format_datetime(dt):
    """Format datetime for API response"""
    if isinstance(dt, datetime):
        return dt.isoformat()
    return dt


def sanitize_filename(filename):
    """Sanitize filename for safe storage"""
    import re
    import os
    from datetime import datetime
    
    # Get extension
    name, ext = os.path.splitext(filename)
    
    # Remove non-alphanumeric characters
    name = re.sub(r'[^a-zA-Z0-9_-]', '_', name)
    
    # Add timestamp to make unique
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    return f"{name}_{timestamp}{ext}"


def require_fields(*fields):
    """Decorator to require specific fields in request"""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            from flask import request
            
            if request.is_json:
                data = request.get_json()
            else:
                data = request.form
            
            missing = [field for field in fields if field not in data]
            
            if missing:
                return error_response(
                    error="Missing required fields",
                    details={"missing": missing},
                    status=400
                )
            
            return f(*args, **kwargs)
        return wrapper
    return decorator
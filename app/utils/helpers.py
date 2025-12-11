"""
Helper utility functions
"""
from datetime import datetime
from flask import request


def get_client_ip():
    """
    Get client IP address from request
    
    Returns:
        IP address string
    """
    if request.environ.get('HTTP_X_FORWARDED_FOR'):
        return request.environ['HTTP_X_FORWARDED_FOR'].split(',')[0]
    return request.environ.get('REMOTE_ADDR', 'unknown')


def get_user_agent():
    """
    Get user agent from request
    
    Returns:
        User agent string
    """
    return request.headers.get('User-Agent', 'unknown')


def format_datetime(dt, format_str='%Y-%m-%d %H:%M:%S'):
    """
    Format datetime object
    
    Args:
        dt: Datetime object
        format_str: Format string
        
    Returns:
        Formatted date string
    """
    if not dt:
        return ''
    return dt.strftime(format_str)


def format_date(dt):
    """
    Format datetime as date only
    
    Args:
        dt: Datetime object
        
    Returns:
        Formatted date string
    """
    return format_datetime(dt, '%Y-%m-%d')


def format_time(dt):
    """
    Format datetime as time only
    
    Args:
        dt: Datetime object
        
    Returns:
        Formatted time string
    """
    return format_datetime(dt, '%H:%M:%S')


def seconds_to_minutes(seconds):
    """
    Convert seconds to minutes
    
    Args:
        seconds: Number of seconds
        
    Returns:
        Minutes (rounded)
    """
    if not seconds:
        return 0
    return round(seconds / 60, 2)


def format_duration(seconds):
    """
    Format duration in human-readable format
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted duration string (e.g., "1h 23m 45s")
    """
    if not seconds:
        return "0s"
    
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    parts = []
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if secs > 0 or not parts:
        parts.append(f"{secs}s")
    
    return " ".join(parts)


def truncate_string(text, length=50, suffix='...'):
    """
    Truncate string to specified length
    
    Args:
        text: Text to truncate
        length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated string
    """
    if not text or len(text) <= length:
        return text
    
    return text[:length - len(suffix)] + suffix


def generate_random_string(length=32):
    """
    Generate random string
    
    Args:
        length: Length of string
        
    Returns:
        Random string
    """
    import secrets
    import string
    
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def is_safe_url(target):
    """
    Check if URL is safe for redirect
    
    Args:
        target: Target URL
        
    Returns:
        True if safe, False otherwise
    """
    from urllib.parse import urlparse, urljoin
    from flask import request
    
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def calculate_percentage(part, total):
    """
    Calculate percentage
    
    Args:
        part: Part value
        total: Total value
        
    Returns:
        Percentage (0-100)
    """
    if total == 0:
        return 0
    return round((part / total) * 100, 2)

"""
Rate limiting middleware
Protects against brute force attacks
"""
from flask import request
from app.extensions.limiter import limiter
from app.config.security import RATE_LIMIT_LOGIN, RATE_LIMIT_API


def setup_rate_limiting(app):
    """
    Setup rate limiting for the application
    
    Args:
        app: Flask application
    """
    # Apply rate limiting to login endpoint
    @app.before_request
    def check_rate_limit():
        """Check rate limits for specific endpoints"""
        if request.endpoint == 'auth.login':
            # This will be checked by the limiter decorator on the route
            pass
        
        return None


def get_rate_limit_key():
    """
    Get rate limit key based on IP address
    
    Returns:
        Rate limit key
    """
    from app.utils.helpers import get_client_ip
    return get_client_ip()


def rate_limit_exceeded_handler(e):
    """
    Handle rate limit exceeded
    
    Args:
        e: Rate limit exception
        
    Returns:
        Error response
    """
    from flask import jsonify, render_template, request
    
    # For API requests, return JSON
    if request.path.startswith('/api/'):
        return jsonify({
            'success': False,
            'message': 'Rate limit exceeded. Please try again later.',
            'retry_after': str(e.description)
        }), 429
    
    # For web requests, render error page
    return render_template('errors/429.html'), 429

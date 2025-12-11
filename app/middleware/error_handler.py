"""
Error handling middleware
Handles application errors and exceptions
"""
from flask import render_template, jsonify, request
from werkzeug.exceptions import HTTPException
import logging


def handle_error(error):
    """
    Generic error handler
    
    Args:
        error: Exception object
        
    Returns:
        Error response (HTML or JSON)
    """
    # Log the error
    logger = logging.getLogger(__name__)
    logger.error(f"Error occurred: {str(error)}", exc_info=True)
    
    # Handle HTTP exceptions
    if isinstance(error, HTTPException):
        code = error.code
        message = error.description
    else:
        code = 500
        message = "An internal server error occurred"
    
    # For API requests, return JSON
    if request.path.startswith('/api/'):
        return jsonify({
            'success': False,
            'error': message,
            'code': code
        }), code
    
    # For web requests, render error template
    return render_template(f'errors/{code}.html'), code


def handle_403(error):
    """Handle 403 Forbidden errors"""
    if request.path.startswith('/api/'):
        return jsonify({
            'success': False,
            'error': 'Access forbidden',
            'code': 403
        }), 403
    return render_template('errors/403.html'), 403


def handle_404(error):
    """Handle 404 Not Found errors"""
    if request.path.startswith('/api/'):
        return jsonify({
            'success': False,
            'error': 'Resource not found',
            'code': 404
        }), 404
    return render_template('errors/404.html'), 404


def handle_500(error):
    """Handle 500 Internal Server errors"""
    # Rollback database session on error
    try:
        from app.extensions.database import db
        db.session.rollback()
    except Exception:
        pass
    
    # Log error details (but not in production logs sent to users)
    logger = logging.getLogger(__name__)
    logger.error(f"Internal server error: {str(error)}", exc_info=True)
    
    if request.path.startswith('/api/'):
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'code': 500
        }), 500
    return render_template('errors/500.html'), 500


def handle_429(error):
    """Handle 429 Rate Limit Exceeded errors"""
    if request.path.startswith('/api/'):
        return jsonify({
            'success': False,
            'error': 'Rate limit exceeded. Please try again later.',
            'code': 429
        }), 429
    return render_template('errors/429.html'), 429


def register_error_handlers(app):
    """
    Register all error handlers with the application
    
    Args:
        app: Flask application
    """
    app.register_error_handler(403, handle_403)
    app.register_error_handler(404, handle_404)
    app.register_error_handler(500, handle_500)
    app.register_error_handler(429, handle_429)
    
    # Generic handler for all other HTTP exceptions
    app.register_error_handler(Exception, handle_error)

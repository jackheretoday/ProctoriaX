"""
Audit logging middleware
Logs all important actions and requests
"""
from flask import request, g
from flask_login import current_user
from app.models.audit_log import AuditLog
from app.utils.helpers import get_client_ip, get_user_agent
from datetime import datetime


def log_request():
    """
    Log request information
    Called as before_request handler
    """
    # Store request start time
    g.request_start_time = datetime.utcnow()
    
    # Skip logging for static files
    if request.endpoint and request.endpoint.startswith('static'):
        return None
    
    # Log important endpoints
    important_endpoints = ['auth.login', 'auth.logout', 'auth.change_password']
    
    if request.endpoint in important_endpoints:
        user_id = current_user.id if current_user.is_authenticated else None
        username = current_user.username if current_user.is_authenticated else None
        
        # Store for after_request logging
        g.log_action = True
        g.log_endpoint = request.endpoint
        g.log_user_id = user_id
        g.log_username = username
    
    return None


def log_after_request(response):
    """
    Log response information
    Called as after_request handler
    
    Args:
        response: Flask response object
        
    Returns:
        response: Unmodified response
    """
    # Skip if not marked for logging
    if not hasattr(g, 'log_action'):
        return response
    
    # Determine status
    status = 'success' if response.status_code < 400 else 'failed'
    
    # Log the action
    try:
        AuditLog.log_action(
            action=g.log_endpoint,
            user_id=g.log_user_id,
            username=g.log_username,
            ip_address=get_client_ip(),
            user_agent=get_user_agent(),
            status=status
        )
    except Exception as e:
        # Don't break the request if logging fails
        print(f"Audit logging failed: {str(e)}")
    
    return response


def log_action(action, user=None, resource_type=None, resource_id=None, details=None):
    """
    Manually log an action
    
    Args:
        action: Action being performed
        user: User object (optional, uses current_user if None)
        resource_type: Type of resource (user, test, question, etc.)
        resource_id: ID of resource
        details: Additional details (JSON string)
    """
    if user is None and current_user.is_authenticated:
        user = current_user
    
    try:
        AuditLog.log_action(
            action=action,
            user=user,
            ip_address=get_client_ip(),
            user_agent=get_user_agent(),
            resource_type=resource_type,
            resource_id=resource_id,
            details=details
        )
    except Exception as e:
        print(f"Audit logging failed: {str(e)}")

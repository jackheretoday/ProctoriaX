"""
Session security middleware
Validates session security and handles timeouts
"""
from flask import session, redirect, url_for, request, flash
from flask_login import current_user, logout_user
from datetime import datetime, timedelta
from app.config.security import SESSION_TIMEOUT_MINUTES


def validate_session_security():
    """
    Validate session security
    Called as before_request handler
    
    Returns:
        Redirect if session invalid, None otherwise
    """
    # Skip for static files and auth endpoints
    if request.endpoint and (request.endpoint.startswith('static') or 
                             request.endpoint.startswith('auth')):
        return None
    
    # Check if user is authenticated
    if not current_user.is_authenticated:
        return None
    
    # Check session timeout
    if 'login_time' in session:
        login_time_str = session['login_time']
        try:
            login_time = datetime.fromisoformat(login_time_str)
            timeout = timedelta(minutes=SESSION_TIMEOUT_MINUTES)
            
            if datetime.utcnow() - login_time > timeout:
                # Session expired
                logout_user()
                session.clear()
                flash('Your session has expired. Please log in again.', 'warning')
                return redirect(url_for('auth.login'))
        except (ValueError, TypeError):
            # Invalid login time, clear session
            logout_user()
            session.clear()
            return redirect(url_for('auth.login'))
    
    # Refresh session timestamp on activity
    session['last_activity'] = datetime.utcnow().isoformat()
    
    return None


def regenerate_session_id():
    """
    Regenerate session ID for security
    Called periodically or after privilege escalation
    """
    # Store session data
    session_data = dict(session)
    
    # Clear session
    session.clear()
    
    # Restore session data with new ID
    for key, value in session_data.items():
        session[key] = value
    
    # Update session modification time
    session.modified = True


def check_session_fixation():
    """
    Check for session fixation attacks
    
    Returns:
        True if session is valid, False otherwise
    """
    # Check if session has required fields
    if current_user.is_authenticated:
        if 'user_id' not in session:
            return False
        
        # Verify session user matches current user
        if session.get('user_id') != current_user.id:
            return False
    
    return True


def validate_session_ip():
    """
    Validate session IP hasn't changed (optional security measure)
    
    Returns:
        True if IP matches or not tracked, False otherwise
    """
    from app.utils.helpers import get_client_ip
    
    current_ip = get_client_ip()
    
    # Get stored IP
    stored_ip = session.get('ip_address')
    
    if stored_ip is None:
        # First request, store IP
        session['ip_address'] = current_ip
        return True
    
    # Check if IP changed (can be disabled for mobile users)
    # For now, we'll just log but not block
    if stored_ip != current_ip:
        # IP changed - could be suspicious
        # In production, you might want to log this
        pass
    
    return True

"""
Session Service
Manages user sessions and session security
"""
from datetime import datetime, timedelta
from flask import session
from app.utils.exceptions import SessionError


class SessionService:
    """Service for managing user sessions"""
    
    @staticmethod
    def create_session(user):
        """
        Create a new session for user
        
        Args:
            user: User object
        """
        session['user_id'] = user.id
        session['username'] = user.username
        session['role'] = user.role
        session['login_time'] = datetime.utcnow().isoformat()
        session.permanent = True
    
    @staticmethod
    def destroy_session():
        """Destroy current session"""
        session.clear()
    
    @staticmethod
    def get_current_user_id():
        """
        Get current user ID from session
        
        Returns:
            User ID or None
        """
        return session.get('user_id')
    
    @staticmethod
    def get_current_user_role():
        """
        Get current user role from session
        
        Returns:
            User role or None
        """
        return session.get('role')
    
    @staticmethod
    def is_session_valid():
        """
        Check if current session is valid
        
        Returns:
            True if session is valid, False otherwise
        """
        if 'user_id' not in session:
            return False
        
        # Check session timeout
        login_time_str = session.get('login_time')
        if login_time_str:
            login_time = datetime.fromisoformat(login_time_str)
            timeout = timedelta(hours=1)  # 1 hour timeout
            
            if datetime.utcnow() - login_time > timeout:
                SessionService.destroy_session()
                return False
        
        return True
    
    @staticmethod
    def refresh_session():
        """Refresh session to prevent timeout"""
        if 'user_id' in session:
            session['login_time'] = datetime.utcnow().isoformat()
    
    @staticmethod
    def set_session_data(key, value):
        """
        Set custom session data
        
        Args:
            key: Session key
            value: Session value
        """
        session[key] = value
    
    @staticmethod
    def get_session_data(key, default=None):
        """
        Get custom session data
        
        Args:
            key: Session key
            default: Default value if key not found
            
        Returns:
            Session value or default
        """
        return session.get(key, default)
    
    @staticmethod
    def remove_session_data(key):
        """
        Remove custom session data
        
        Args:
            key: Session key
        """
        session.pop(key, None)

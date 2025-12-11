"""
Flask-Login manager for user authentication
"""
from flask_login import LoginManager

# Initialize LoginManager
login_manager = LoginManager()


def init_login_manager(app):
    """
    Initialize login manager with Flask app
    
    Args:
        app: Flask application instance
    """
    login_manager.init_app(app)
    
    # Set login view
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    # Session protection
    login_manager.session_protection = 'strong'
    
    # User loader callback
    @login_manager.user_loader
    def load_user(user_id):
        """
        Load user by ID
        
        Args:
            user_id: User ID
            
        Returns:
            User object or None
        """
        from app.models.user import User
        return User.query.get(int(user_id))
    
    # Unauthorized callback
    @login_manager.unauthorized_handler
    def unauthorized():
        """Handle unauthorized access"""
        from flask import flash, redirect, url_for, request
        flash('You must be logged in to view that page.', 'warning')
        return redirect(url_for('auth.login', next=request.endpoint))
    
    return login_manager

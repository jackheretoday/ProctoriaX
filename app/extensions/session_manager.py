"""
Flask-Session manager for server-side sessions
"""
from flask_session import Session

# Initialize Session
session = Session()


def init_session(app):
    """
    Initialize session with Flask app
    
    Args:
        app: Flask application instance
    """
    session.init_app(app)
    return session

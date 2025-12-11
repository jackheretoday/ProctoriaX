"""
Flask-Limiter for rate limiting
"""
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Initialize Limiter
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)


def init_limiter(app):
    """
    Initialize rate limiter with Flask app
    
    Args:
        app: Flask application instance
    """
    limiter.init_app(app)
    return limiter

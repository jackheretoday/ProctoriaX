"""
CORS (Cross-Origin Resource Sharing) configuration
"""
from flask_cors import CORS

# Initialize CORS
cors = CORS()


def init_cors(app):
    """
    Initialize CORS with Flask app
    
    Args:
        app: Flask application instance
    """
    cors.init_app(
        app,
        resources={
            r"/api/*": {
                "origins": ["http://localhost:5000", "http://127.0.0.1:5000"],
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization"],
                "supports_credentials": True
            }
        }
    )
    
    return cors

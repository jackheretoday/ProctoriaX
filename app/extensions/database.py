"""
SQLAlchemy database instance
"""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize SQLAlchemy
db = SQLAlchemy()

# Initialize Flask-Migrate
migrate = Migrate()


def init_db(app):
    """
    Initialize database with Flask app
    
    Args:
        app: Flask application instance
    """
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Import all models to ensure they are registered
    with app.app_context():
        from app.models import (
            User, Test, Question, Assignment, 
            Result, TermsConditions, AuditLog
        )
        
        # Create tables if they don't exist
        db.create_all()
    
    return db

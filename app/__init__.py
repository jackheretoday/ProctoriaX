"""
Application Factory
Creates and configures the Flask application
"""
import os
from flask import Flask, render_template, redirect, url_for
from flask_login import current_user


def create_app(config_name='development'):
    """
    Create Flask application
    
    Args:
        config_name: Configuration name (development, production, testing)
        
    Returns:
        Flask application instance
    """
    # Create Flask app
    app = Flask(__name__)
    
    # Load configuration
    from app.config import config_by_name
    app.config.from_object(config_by_name.get(config_name, config_by_name['default']))
    
    # Initialize extensions
    init_extensions(app)
    
    # Register middleware
    register_middleware(app)
    
    # Register blueprints
    register_blueprints(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Register template filters
    register_template_filters(app)
    
    # Register routes
    register_routes(app)
    
    return app


def init_extensions(app):
    """Initialize Flask extensions"""
    from app.extensions import (
        init_db,
        init_login_manager,
        init_session,
        init_cache,
        init_limiter,
        init_cors
    )
    
    # Database
    init_db(app)
    
    # Login Manager
    init_login_manager(app)
    
    # Session
    # Initialize server-side sessions only in production to avoid
    # potential cookie value type issues during development.
    if app.config.get('ENV') == 'production' or app.config.get('FLASK_ENV') == 'production':
        init_session(app)
    
    # Cache
    init_cache(app)
    
    # Rate Limiter
    init_limiter(app)
    
    # CORS
    init_cors(app)


def register_middleware(app):
    """Register application middleware"""
    from app.middleware.audit_logger import log_after_request
    from app.middleware import validate_session_security
    
    # Initialize traffic monitoring
    try:
        from app.services.traffic_service import TrafficMiddleware
        traffic_middleware = TrafficMiddleware(app)
        print("Traffic monitoring middleware initialized")
    except Exception as e:
        print(f"Traffic monitoring not available: {e}")
    
    # Initialize user session tracking table
    try:
        from app.models.user_session import UserSession
        from app.extensions.database import db
        with app.app_context():
            UserSession.__table__.create(db.engine, checkfirst=True)
            print("User session tracking initialized")
    except Exception as e:
        print(f"User session tracking not available: {e}")
    
    # Register before_request handlers
    @app.before_request
    def before_request_handler():
        """Handle request preprocessing"""
        # Validate session security
        validate_session_security()
    
    # Register after_request handlers
    @app.after_request
    def after_request_handler(response):
        """Handle request postprocessing"""
        # Log request
        log_after_request(response)
        return response


def register_blueprints(app):
    """Register Flask blueprints"""
    from app.api.v1.auth import auth_bp
    from app.api.v1.admin import admin_bp
    from app.api.v1.teacher import teacher_bp
    from app.api.v1.student import student_bp
    
    # Register authentication blueprint
    app.register_blueprint(auth_bp)
    
    # Register admin blueprint
    app.register_blueprint(admin_bp)
    
    # Register teacher blueprint
    app.register_blueprint(teacher_bp)
    
    # Register student blueprint
    app.register_blueprint(student_bp)


def register_error_handlers(app):
    """Register error handlers"""
    
    @app.errorhandler(403)
    def forbidden(e):
        """Handle 403 Forbidden"""
        return render_template('errors/403.html'), 403
    
    @app.errorhandler(404)
    def not_found(e):
        """Handle 404 Not Found"""
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(e):
        """Handle 500 Internal Server Error"""
        from app.extensions.database import db
        db.session.rollback()
        return render_template('errors/500.html'), 500


def register_template_filters(app):
    """Register custom template filters"""
    from app.utils.helpers import format_datetime, format_date, format_duration
    
    app.jinja_env.filters['datetime'] = format_datetime
    app.jinja_env.filters['date'] = format_date
    app.jinja_env.filters['duration'] = format_duration


def register_routes(app):
    """Register application routes"""
    
    @app.route('/')
    def index():
        """Home/Index page"""
        # Redirect based on login status and role
        if current_user.is_authenticated:
            if current_user.is_admin():
                return redirect(url_for('admin.dashboard'))
            elif current_user.is_teacher():
                return redirect(url_for('teacher.dashboard'))
            elif current_user.is_student():
                return redirect(url_for('student.dashboard'))
        
        # Not logged in, redirect to login
        return redirect(url_for('auth.login'))
    
    @app.route('/health')
    def health():
        """Health check endpoint"""
        from datetime import datetime
        return {
            'status': 'ok',
            'timestamp': datetime.utcnow().isoformat(),
            'environment': app.config.get('FLASK_ENV', 'unknown')
        }

"""
Audit Log model for security and tracking
"""
from datetime import datetime
from app.extensions.database import db


class AuditLog(db.Model):
    """Audit log for tracking all important actions"""
    
    __tablename__ = 'audit_logs'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # User
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    username = db.Column(db.String(80))  # Store username for deleted users
    
    # Action
    action = db.Column(db.String(50), nullable=False, index=True)
    # Examples: login, logout, create_user, update_user, delete_user,
    # upload_questions, start_test, submit_test, view_results, etc.
    
    # Details
    details = db.Column(db.Text)  # JSON string with additional details
    
    # Request Info
    ip_address = db.Column(db.String(45))  # IPv4 or IPv6
    user_agent = db.Column(db.String(255))
    
    # Resource
    resource_type = db.Column(db.String(50))  # user, test, question, result, etc.
    resource_id = db.Column(db.Integer)
    
    # Status
    status = db.Column(db.String(20))  # success, failed, error
    error_message = db.Column(db.Text)
    
    # Timestamp
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)
    
    def __init__(self, action, **kwargs):
        """Initialize audit log"""
        self.action = action
        self.user_id = kwargs.get('user_id')
        self.username = kwargs.get('username')
        self.details = kwargs.get('details')
        self.ip_address = kwargs.get('ip_address')
        self.user_agent = kwargs.get('user_agent')
        self.resource_type = kwargs.get('resource_type')
        self.resource_id = kwargs.get('resource_id')
        self.status = kwargs.get('status', 'success')
        self.error_message = kwargs.get('error_message')
        self.timestamp = kwargs.get('timestamp', datetime.utcnow())
    
    def __repr__(self):
        return f'<AuditLog {self.action} by {self.username or self.user_id}>'
    
    @classmethod
    def log_action(cls, action, user=None, **kwargs):
        """
        Create an audit log entry
        
        Args:
            action: Action being performed
            user: User object (optional)
            **kwargs: Additional fields
        """
        # Extract username from kwargs to avoid duplicate keyword argument
        username = kwargs.pop('username', None)
        
        log = cls(
            action=action,
            user_id=user.id if user else None,
            username=user.username if user else username,
            **kwargs
        )
        db.session.add(log)
        db.session.commit()
        return log
    
    @classmethod
    def log_login(cls, user, ip_address, status='success'):
        """Log a login attempt"""
        return cls.log_action(
            action='login',
            user=user,
            ip_address=ip_address,
            status=status
        )
    
    @classmethod
    def log_logout(cls, user, ip_address):
        """Log a logout"""
        return cls.log_action(
            action='logout',
            user=user,
            ip_address=ip_address
        )
    
    @classmethod
    def log_failed_login(cls, username, ip_address, error_message):
        """Log a failed login attempt"""
        return cls.log_action(
            action='login',
            username=username,
            ip_address=ip_address,
            status='failed',
            error_message=error_message
        )
    
    def to_dict(self):
        """Convert audit log to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.username,
            'action': self.action,
            'details': self.details,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'resource_type': self.resource_type,
            'resource_id': self.resource_id,
            'status': self.status,
            'error_message': self.error_message,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }

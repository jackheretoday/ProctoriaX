"""
User model for authentication and role management
"""
from flask_login import UserMixin
from app.extensions.database import db
from app.models.mixins import TimestampMixin, SoftDeleteMixin


class User(UserMixin, TimestampMixin, SoftDeleteMixin, db.Model):
    """User model with role-based access"""
    
    __tablename__ = 'users'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Authentication
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Role: admin, teacher, student
    role = db.Column(db.String(20), nullable=False, index=True)
    
    # Status
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_verified = db.Column(db.Boolean, default=False, nullable=False)
    
    # Profile
    full_name = db.Column(db.String(120))
    student_id = db.Column(db.String(50), unique=True, nullable=True)  # For students
    
    # Login tracking
    last_login = db.Column(db.DateTime)
    login_count = db.Column(db.Integer, default=0)
    failed_login_attempts = db.Column(db.Integer, default=0)
    locked_until = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    created_tests = db.relationship('Test', backref='creator', lazy='dynamic',
                                   foreign_keys='Test.created_by')
    assignments = db.relationship('Assignment', backref='student', lazy='dynamic',
                                 foreign_keys='Assignment.student_id')
    results = db.relationship('Result', backref='student', lazy='dynamic',
                             foreign_keys='Result.student_id')
    audit_logs = db.relationship('AuditLog', backref='user', lazy='dynamic',
                                foreign_keys='AuditLog.user_id')
    
    def __init__(self, username, email, password_hash, role, **kwargs):
        """Initialize user"""
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.role = role
        self.full_name = kwargs.get('full_name')
        self.student_id = kwargs.get('student_id')
        self.is_active = kwargs.get('is_active', True)
        self.is_verified = kwargs.get('is_verified', False)
    
    def __repr__(self):
        return f'<User {self.username} ({self.role})>'
    
    def is_admin(self):
        """Check if user is admin"""
        return self.role == 'admin'
    
    def is_teacher(self):
        """Check if user is teacher"""
        return self.role == 'teacher'
    
    def is_student(self):
        """Check if user is student"""
        return self.role == 'student'
    
    def has_role(self, role):
        """Check if user has specific role"""
        return self.role == role
    
    def update_last_login(self):
        """Update last login timestamp"""
        from datetime import datetime
        self.last_login = datetime.utcnow()
        self.login_count += 1
        self.failed_login_attempts = 0  # Reset on successful login
        db.session.commit()
    
    def increment_failed_login(self):
        """Increment failed login attempts"""
        self.failed_login_attempts += 1
        db.session.commit()
    
    def lock_account(self, minutes=15):
        """Lock account for specified minutes"""
        from datetime import datetime, timedelta
        self.locked_until = datetime.utcnow() + timedelta(minutes=minutes)
        db.session.commit()
    
    def is_locked(self):
        """Check if account is locked"""
        from datetime import datetime
        if self.locked_until and self.locked_until > datetime.utcnow():
            return True
        return False
    
    def to_dict(self, include_sensitive=False):
        """Convert user to dictionary"""
        data = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'full_name': self.full_name,
            'student_id': self.student_id,
            'is_active': self.is_active,
            'is_verified': self.is_verified,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        if include_sensitive:
            data.update({
                'login_count': self.login_count,
                'failed_login_attempts': self.failed_login_attempts,
                'is_locked': self.is_locked()
            })
        
        return data

"""
Assignment model for assigning tests to students
"""
from datetime import datetime
from app.extensions.database import db
from app.models.mixins import TimestampMixin


class Assignment(TimestampMixin, db.Model):
    """Assignment model linking students to tests"""
    
    __tablename__ = 'assignments'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign Keys
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    test_id = db.Column(db.Integer, db.ForeignKey('tests.id'), nullable=False)
    
    # Assignment Details
    assigned_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=True)
    
    # Status
    status = db.Column(db.String(20), default='pending')  # pending, in_progress, completed, expired
    
    # Test Session
    started_at = db.Column(db.DateTime, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)
    time_spent = db.Column(db.Integer, nullable=True)  # seconds
    
    # Assigned by
    assigned_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # Constraints
    __table_args__ = (
        db.UniqueConstraint('student_id', 'test_id', name='uq_student_test'),
    )
    
    def __init__(self, student_id, test_id, assigned_date=None, **kwargs):
        """Initialize assignment"""
        self.student_id = student_id
        self.test_id = test_id
        self.assigned_date = assigned_date or datetime.utcnow()
        self.due_date = kwargs.get('due_date')
        self.assigned_by = kwargs.get('assigned_by')
        self.status = kwargs.get('status', 'pending')
    
    def __repr__(self):
        return f'<Assignment Student:{self.student_id} Test:{self.test_id}>'
    
    def is_available_today(self):
        """Check if assignment is available today"""
        from datetime import date
        if self.assigned_date:
            return self.assigned_date.date() == date.today()
        return False
    
    def is_expired(self):
        """Check if assignment has expired"""
        if self.due_date and datetime.utcnow() > self.due_date:
            return True
        return False
    
    def start_test(self):
        """Mark test as started"""
        self.status = 'in_progress'
        self.started_at = datetime.utcnow()
        db.session.commit()
    
    def complete_test(self):
        """Mark test as completed"""
        self.status = 'completed'
        self.completed_at = datetime.utcnow()
        if self.started_at:
            self.time_spent = int((self.completed_at - self.started_at).total_seconds())
        db.session.commit()
    
    def to_dict(self):
        """Convert assignment to dictionary"""
        return {
            'id': self.id,
            'student_id': self.student_id,
            'student_name': self.student.username if self.student else None,
            'test_id': self.test_id,
            'test_name': self.test.name if self.test else None,
            'assigned_date': self.assigned_date.isoformat() if self.assigned_date else None,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'status': self.status,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'time_spent': self.time_spent,
            'is_expired': self.is_expired(),
            'is_available_today': self.is_available_today(),
            'assigned_by': self.assigned_by
        }

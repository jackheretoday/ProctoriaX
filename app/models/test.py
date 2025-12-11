"""
Test model for managing tests/exams
"""
from app.extensions.database import db
from app.models.mixins import TimestampMixin


class Test(TimestampMixin, db.Model):
    """Test/Exam model"""
    
    __tablename__ = 'tests'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Test Information
    name = db.Column(db.String(200), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    
    # Timing
    duration = db.Column(db.Integer, nullable=False)  # Duration in minutes
    start_date = db.Column(db.DateTime, nullable=True)
    end_date = db.Column(db.DateTime, nullable=True)
    
    # Creator
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Status
    is_active = db.Column(db.Boolean, default=True, nullable=True)
    is_published = db.Column(db.Boolean, default=True, nullable=False)
    
    # Statistics
    total_questions = db.Column(db.Integer, default=0)
    pass_percentage = db.Column(db.Float, default=50.0)
    
    # Relationships
    questions = db.relationship('Question', backref='test', lazy='dynamic', 
                               cascade='all, delete-orphan')
    assignments = db.relationship('Assignment', backref='test', lazy='dynamic',
                                 cascade='all, delete-orphan')
    results = db.relationship('Result', backref='test', lazy='dynamic',
                             cascade='all, delete-orphan')
    terms_conditions = db.relationship('TermsConditions', backref='test', 
                                      uselist=False, cascade='all, delete-orphan')
    
    def __init__(self, name, subject, duration, created_by, **kwargs):
        """Initialize test"""
        self.name = name
        self.subject = subject
        self.duration = duration
        self.created_by = created_by
        self.description = kwargs.get('description')
        self.start_date = kwargs.get('start_date')
        self.end_date = kwargs.get('end_date')
        self.pass_percentage = kwargs.get('pass_percentage', 50.0)
    
    def __repr__(self):
        return f'<Test {self.name} ({self.subject})>'
    
    def update_question_count(self):
        """Update total questions count"""
        self.total_questions = self.questions.count()
        db.session.commit()
    
    def get_question_count(self):
        """Get total questions"""
        return self.questions.count()
    
    def is_available(self):
        """Check if test is currently available"""
        from datetime import datetime
        now = datetime.utcnow()
        
        if not self.is_active or not self.is_published:
            return False
        
        if self.start_date and now < self.start_date:
            return False
        
        if self.end_date and now > self.end_date:
            return False
        
        return True
    
    def get_statistics(self):
        """Get test statistics"""
        total_attempts = self.results.count()
        
        if total_attempts == 0:
            return {
                'total_attempts': 0,
                'average_score': 0,
                'highest_score': 0,
                'lowest_score': 0,
                'pass_count': 0,
                'fail_count': 0,
                'pass_rate': 0
            }
        
        all_results = self.results.all()
        scores = [r.percentage for r in all_results]
        
        pass_count = sum(1 for s in scores if s >= self.pass_percentage)
        fail_count = total_attempts - pass_count
        
        return {
            'total_attempts': total_attempts,
            'average_score': sum(scores) / total_attempts,
            'highest_score': max(scores),
            'lowest_score': min(scores),
            'pass_count': pass_count,
            'fail_count': fail_count,
            'pass_rate': (pass_count / total_attempts) * 100
        }
    
    def to_dict(self, include_stats=False):
        """Convert test to dictionary"""
        data = {
            'id': self.id,
            'name': self.name,
            'subject': self.subject,
            'description': self.description,
            'duration': self.duration,
            'total_questions': self.total_questions,
            'pass_percentage': self.pass_percentage,
            'is_active': self.is_active,
            'is_published': self.is_published,
            'is_available': self.is_available(),
            'created_by': self.created_by,
            'creator_name': self.creator.username if self.creator else None,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        if include_stats:
            data['statistics'] = self.get_statistics()
        
        return data

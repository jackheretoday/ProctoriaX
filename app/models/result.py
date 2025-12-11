"""
Result model for storing test results
"""
from datetime import datetime
from app.extensions.database import db
from app.models.mixins import TimestampMixin


class Result(TimestampMixin, db.Model):
    """Result model for test scores"""
    
    __tablename__ = 'results'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign Keys
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    test_id = db.Column(db.Integer, db.ForeignKey('tests.id'), nullable=False)
    
    # Scores
    total_questions = db.Column(db.Integer, nullable=False)
    correct_answers = db.Column(db.Integer, nullable=False)
    incorrect_answers = db.Column(db.Integer, nullable=False)
    unanswered = db.Column(db.Integer, default=0)
    
    # Score and percentage
    score = db.Column(db.Float, nullable=False)
    percentage = db.Column(db.Float, nullable=False)
    
    # Status
    passed = db.Column(db.Boolean, nullable=False)
    
    # Timing
    completed_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    time_taken = db.Column(db.Integer, nullable=True)  # seconds
    
    # Encrypted answers (store student's submitted answers)
    encrypted_answers = db.Column(db.LargeBinary, nullable=True)
    
    # Result viewed flag
    result_viewed = db.Column(db.Boolean, default=False)
    viewed_at = db.Column(db.DateTime, nullable=True)
    
    # Constraints
    __table_args__ = (
        db.UniqueConstraint('student_id', 'test_id', name='uq_student_test_result'),
    )
    
    def __init__(self, student_id, test_id, total_questions, correct_answers, **kwargs):
        """Initialize result"""
        self.student_id = student_id
        self.test_id = test_id
        self.total_questions = total_questions
        self.correct_answers = correct_answers
        self.unanswered = kwargs.get('unanswered', 0)
        # Calculate incorrect answers (total - correct - unanswered)
        self.incorrect_answers = total_questions - correct_answers - self.unanswered
        
        # Calculate percentage
        if total_questions > 0:
            self.percentage = (correct_answers / total_questions) * 100
        else:
            self.percentage = 0
        
        # Calculate score (assuming each question is 1 point)
        self.score = float(correct_answers)
        
        # Determine if passed
        pass_percentage = kwargs.get('pass_percentage', 50.0)
        self.passed = self.percentage >= pass_percentage
        
        self.completed_at = kwargs.get('completed_at', datetime.utcnow())
        self.time_taken = kwargs.get('time_taken')
        self.encrypted_answers = kwargs.get('encrypted_answers')
    
    def __repr__(self):
        return f'<Result Student:{self.student_id} Test:{self.test_id} Score:{self.percentage}%>'
    
    def mark_viewed(self):
        """Mark result as viewed"""
        self.result_viewed = True
        self.viewed_at = datetime.utcnow()
        db.session.commit()
    
    def get_grade(self):
        """Get letter grade based on percentage"""
        if self.percentage >= 90:
            return 'A'
        elif self.percentage >= 80:
            return 'B'
        elif self.percentage >= 70:
            return 'C'
        elif self.percentage >= 60:
            return 'D'
        else:
            return 'F'
    
    def to_dict(self, include_answers=False):
        """Convert result to dictionary"""
        data = {
            'id': self.id,
            'student_id': self.student_id,
            'student_name': self.student.username if self.student else None,
            'student_email': self.student.email if self.student else None,
            'test_id': self.test_id,
            'test_name': self.test.name if self.test else None,
            'total_questions': self.total_questions,
            'correct_answers': self.correct_answers,
            'incorrect_answers': self.incorrect_answers,
            'unanswered': self.unanswered,
            'score': self.score,
            'percentage': round(self.percentage, 2),
            'grade': self.get_grade(),
            'passed': self.passed,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'time_taken': self.time_taken,
            'result_viewed': self.result_viewed,
            'viewed_at': self.viewed_at.isoformat() if self.viewed_at else None
        }
        
        if include_answers and self.encrypted_answers:
            # Decrypt answers if requested
            from app.services.encryption_service import EncryptionService
            import json
            encryption = EncryptionService()
            answers_json = encryption.decrypt_data(self.encrypted_answers)
            data['answers'] = json.loads(answers_json)
        
        return data

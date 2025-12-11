"""
Question model for storing encrypted test questions
"""
from app.extensions.database import db
from app.models.mixins import TimestampMixin


class Question(TimestampMixin, db.Model):
    """Question model with encrypted content"""
    
    __tablename__ = 'questions'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign Key
    test_id = db.Column(db.Integer, db.ForeignKey('tests.id'), nullable=False)
    
    # Question Number
    question_number = db.Column(db.Integer, nullable=False)
    
    # Encrypted Content (stored as binary)
    encrypted_question_text = db.Column(db.LargeBinary, nullable=False)
    encrypted_options = db.Column(db.LargeBinary, nullable=False)  # JSON stored encrypted
    encrypted_correct_answer = db.Column(db.LargeBinary, nullable=False)
    encrypted_explanation = db.Column(db.LargeBinary, nullable=True)
    
    # Metadata
    difficulty = db.Column(db.String(20), default='medium')  # easy, medium, hard
    points = db.Column(db.Integer, default=1)
    
    # Constraints
    __table_args__ = (
        db.UniqueConstraint('test_id', 'question_number', name='uq_test_question'),
    )
    
    def __init__(self, test_id, question_number, encrypted_question_text, 
                 encrypted_options, encrypted_correct_answer, **kwargs):
        """Initialize question"""
        self.test_id = test_id
        self.question_number = question_number
        self.encrypted_question_text = encrypted_question_text
        self.encrypted_options = encrypted_options
        self.encrypted_correct_answer = encrypted_correct_answer
        self.encrypted_explanation = kwargs.get('encrypted_explanation')
        self.difficulty = kwargs.get('difficulty', 'medium')
        self.points = kwargs.get('points', 1)
    
    def get_decrypted_content(self):
        """Get decrypted content of the question"""
        return self.to_dict(decrypt=True, include_answer=False)
    
    def __repr__(self):
        return f'<Question {self.id} - Test {self.test_id} - Q{self.question_number}>'
    
    def to_dict(self, decrypt=False, include_answer=False):
        """
        Convert question to dictionary
        
        Args:
            decrypt: If True, decrypt the content
            include_answer: If True, include correct answer
        """
        data = {
            'id': self.id,
            'test_id': self.test_id,
            'question_number': self.question_number,
            'difficulty': self.difficulty,
            'points': self.points,
        }
        
        if decrypt:
            # Import encryption service to decrypt
            from app.services.encryption_service import EncryptionService
            encryption = EncryptionService()
            
            # Decrypt question text
            data['question_text'] = encryption.decrypt_data(
                self.encrypted_question_text
            )
            
            # Decrypt options (stored as JSON)
            import json
            options_json = encryption.decrypt_data(self.encrypted_options)
            data['options'] = json.loads(options_json)
            
            # Decrypt explanation if exists
            if self.encrypted_explanation:
                data['explanation'] = encryption.decrypt_data(
                    self.encrypted_explanation
                )
            
            # Only include answer if explicitly requested
            if include_answer:
                data['correct_answer'] = encryption.decrypt_data(
                    self.encrypted_correct_answer
                )
        else:
            # Return encrypted data as base64 for transport
            import base64
            data['encrypted_question_text'] = base64.b64encode(
                self.encrypted_question_text
            ).decode('utf-8')
            data['encrypted_options'] = base64.b64encode(
                self.encrypted_options
            ).decode('utf-8')
            
            if include_answer:
                data['encrypted_correct_answer'] = base64.b64encode(
                    self.encrypted_correct_answer
                ).decode('utf-8')
        
        return data

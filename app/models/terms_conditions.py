"""
Terms and Conditions model for storing encrypted T&C
"""
from app.extensions.database import db
from app.models.mixins import TimestampMixin


class TermsConditions(TimestampMixin, db.Model):
    """Terms and Conditions model with encrypted content"""
    
    __tablename__ = 'terms_conditions'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign Key
    test_id = db.Column(db.Integer, db.ForeignKey('tests.id'), nullable=False, unique=True)
    
    # Encrypted Content (stored as binary)
    encrypted_content = db.Column(db.LargeBinary, nullable=False)
    
    # Metadata
    bullet_count = db.Column(db.Integer, nullable=False)
    
    def __init__(self, test_id, encrypted_content, bullet_count):
        """Initialize terms and conditions"""
        self.test_id = test_id
        self.encrypted_content = encrypted_content
        self.bullet_count = bullet_count
    
    def __repr__(self):
        return f'<TermsConditions Test:{self.test_id} Bullets:{self.bullet_count}>'
    
    def to_dict(self, decrypt=False):
        """Convert terms to dictionary"""
        data = {
            'id': self.id,
            'test_id': self.test_id,
            'bullet_count': self.bullet_count,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        if decrypt:
            # Decrypt terms
            from app.services.encryption_service import EncryptionService
            import json
            encryption = EncryptionService()
            terms_json = encryption.decrypt_data(self.encrypted_content)
            data['terms'] = json.loads(terms_json)
        else:
            # Return encrypted data as base64
            import base64
            data['encrypted_content'] = base64.b64encode(
                self.encrypted_content
            ).decode('utf-8')
        
        return data

"""
Terms & Conditions Service
Handles encrypted terms and conditions for tests
"""
from app.models.terms_conditions import TermsConditions
from app.models.audit_log import AuditLog
from app.services.encryption_service import EncryptionService
from app.extensions.database import db
from app.utils.exceptions import ValidationError, DatabaseError
from app.utils.constants import MAX_TERMS_BULLETS
import json


class TermsService:
    """Service for managing terms and conditions"""
    
    @staticmethod
    def create_terms(test_id, terms_list):
        """
        Create encrypted terms and conditions for a test
        
        Args:
            test_id: ID of the test
            terms_list: List of terms (max 10)
            
        Returns:
            TermsConditions object
            
        Raises:
            ValidationError: If validation fails
            DatabaseError: If database error occurs
        """
        try:
            # Validate maximum 10 bullets
            if len(terms_list) > MAX_TERMS_BULLETS:
                raise ValidationError(f"Maximum {MAX_TERMS_BULLETS} terms allowed, found {len(terms_list)}")
            
            if not terms_list:
                raise ValidationError("At least one term is required")
            
            # Check if terms already exist for this test
            existing_terms = TermsConditions.query.filter_by(test_id=test_id).first()
            if existing_terms:
                raise ValidationError("Terms already exist for this test. Use update instead.")
            
            # Convert list to JSON string
            terms_json = json.dumps(terms_list)
            
            # Encrypt the JSON
            encrypted_content = EncryptionService.encrypt_data(terms_json)
            
            # Create terms record
            terms = TermsConditions(
                test_id=test_id,
                encrypted_content=encrypted_content
            )
            
            db.session.add(terms)
            db.session.commit()
            
            # Log creation
            AuditLog.log_action(
                action='create_terms',
                details=f'Created terms for test {test_id} with {len(terms_list)} items'
            )
            
            return terms
            
        except ValidationError:
            raise
        except Exception as e:
            db.session.rollback()
            raise DatabaseError(f"Error creating terms: {str(e)}")
    
    @staticmethod
    def get_terms_for_test(test_id, decrypt=True):
        """
        Get terms and conditions for a test
        
        Args:
            test_id: ID of the test
            decrypt: Whether to decrypt and return list
            
        Returns:
            List of terms (if decrypt=True) or TermsConditions object
        """
        terms = TermsConditions.query.filter_by(test_id=test_id).first()
        
        if not terms:
            return None
        
        if decrypt:
            try:
                # Decrypt content
                decrypted_json = EncryptionService.decrypt_data(terms.encrypted_content)
                # Parse JSON to list
                terms_list = json.loads(decrypted_json)
                return terms_list
            except Exception as e:
                raise DatabaseError(f"Error decrypting terms: {str(e)}")
        
        return terms
    
    @staticmethod
    def update_terms(test_id, terms_list):
        """
        Update terms and conditions for a test
        
        Args:
            test_id: ID of the test
            terms_list: New list of terms (max 10)
            
        Returns:
            Updated TermsConditions object
            
        Raises:
            ValidationError: If validation fails
            DatabaseError: If update fails
        """
        try:
            # Validate maximum 10 bullets
            if len(terms_list) > MAX_TERMS_BULLETS:
                raise ValidationError(f"Maximum {MAX_TERMS_BULLETS} terms allowed, found {len(terms_list)}")
            
            if not terms_list:
                raise ValidationError("At least one term is required")
            
            # Get existing terms
            terms = TermsConditions.query.filter_by(test_id=test_id).first()
            
            if not terms:
                raise ValidationError("Terms not found for this test. Use create instead.")
            
            # Convert list to JSON and encrypt
            terms_json = json.dumps(terms_list)
            encrypted_content = EncryptionService.encrypt_data(terms_json)
            
            # Update encrypted content
            terms.encrypted_content = encrypted_content
            
            db.session.commit()
            
            # Log update
            AuditLog.log_action(
                action='update_terms',
                details=f'Updated terms for test {test_id} with {len(terms_list)} items'
            )
            
            return terms
            
        except ValidationError:
            raise
        except Exception as e:
            db.session.rollback()
            raise DatabaseError(f"Error updating terms: {str(e)}")
    
    @staticmethod
    def delete_terms(test_id):
        """
        Delete terms and conditions for a test
        
        Args:
            test_id: ID of the test
            
        Raises:
            ValidationError: If terms not found
            DatabaseError: If delete fails
        """
        try:
            terms = TermsConditions.query.filter_by(test_id=test_id).first()
            
            if not terms:
                raise ValidationError("Terms not found for this test")
            
            db.session.delete(terms)
            db.session.commit()
            
            # Log deletion
            AuditLog.log_action(
                action='delete_terms',
                details=f'Deleted terms for test {test_id}'
            )
            
        except ValidationError:
            raise
        except Exception as e:
            db.session.rollback()
            raise DatabaseError(f"Error deleting terms: {str(e)}")
    
    @staticmethod
    def terms_exist(test_id):
        """
        Check if terms exist for a test
        
        Args:
            test_id: ID of the test
            
        Returns:
            bool: True if terms exist
        """
        return TermsConditions.query.filter_by(test_id=test_id).first() is not None
    
    @staticmethod
    def create_or_update_terms(test_id, terms_list):
        """
        Create terms if they don't exist, otherwise update
        
        Args:
            test_id: ID of the test
            terms_list: List of terms
            
        Returns:
            TermsConditions object
        """
        if TermsService.terms_exist(test_id):
            return TermsService.update_terms(test_id, terms_list)
        else:
            return TermsService.create_terms(test_id, terms_list)

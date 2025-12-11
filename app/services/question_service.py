# """
# Question Service
# Handles question CRUD operations with encryption
# """
# from app.models.question import Question
# from app.models.audit_log import AuditLog
# from app.services.encryption_service import EncryptionService
# from app.extensions.database import db
# from app.utils.exceptions import ValidationError, DatabaseError
# import json


# class QuestionService:
#     """Service for managing questions"""
    
#     @staticmethod
#     def create_question(test_id, question_data):
#         """
#         Create a single encrypted question
        
#         Args:
#             test_id: ID of the test
#             question_data: Dictionary with question details
            
#         Returns:
#             Question object
            
#         Raises:
#             ValidationError: If validation fails
#             DatabaseError: If database error occurs
#         """
#         try:
#             # Validate question data
#             if not question_data.get('question_text'):
#                 raise ValidationError("Question text is required")
            
#             if not question_data.get('options'):
#                 raise ValidationError("Question options are required")
            
#             if not question_data.get('correct_answer'):
#                 raise ValidationError("Correct answer is required")
            
#             # Prepare question content for encryption
#             question_content = {
#                 'question_text': question_data['question_text'],
#                 'options': question_data['options']
#             }
            
#             # Encrypt question content
#             encrypted_content = EncryptionService.encrypt_data(json.dumps(question_content))
            
#             # Encrypt correct answer
#             encrypted_answer = EncryptionService.encrypt_data(question_data['correct_answer'])
            
#             # Encrypt explanation (if provided)
#             explanation = question_data.get('explanation', '')
#             encrypted_explanation = EncryptionService.encrypt_data(explanation) if explanation else None
            
#             # Create question
#             question = Question(
#                 test_id=test_id,
#                 question_number=question_data.get('question_number', 0),
#                 encrypted_content=encrypted_content,
#                 encrypted_answer=encrypted_answer,
#                 encrypted_explanation=encrypted_explanation,
#                 marks=question_data.get('marks', 1)
#             )
            
#             db.session.add(question)
#             db.session.commit()
            
#             return question
            
#         except ValidationError:
#             raise
#         except Exception as e:
#             db.session.rollback()
#             raise DatabaseError(f"Error creating question: {str(e)}")
    
#     @staticmethod
#     def bulk_create_questions(test_id, questions_list):
#         """
#         Create multiple questions in a transaction
        
#         Args:
#             test_id: ID of the test
#             questions_list: List of question dictionaries
            
#         Returns:
#             int: Count of created questions
            
#         Raises:
#             DatabaseError: If transaction fails
#         """
#         try:
#             created_count = 0
            
#             for question_data in questions_list:
#                 QuestionService.create_question(test_id, question_data)
#                 created_count += 1
            
#             # Log bulk creation
#             AuditLog.log_action(
#                 action='bulk_create_questions',
#                 details=f'Created {created_count} questions for test {test_id}'
#             )
            
#             return created_count
            
#         except Exception as e:
#             db.session.rollback()
#             raise DatabaseError(f"Error in bulk question creation: {str(e)}")
    
#     @staticmethod
#     def get_questions_for_test(test_id, decrypt=False):
#         """
#         Get all questions for a test
        
#         Args:
#             test_id: ID of the test
#             decrypt: Whether to decrypt questions
            
#         Returns:
#             List of question objects or dictionaries
#         """
#         questions = Question.query.filter_by(test_id=test_id).order_by(Question.question_number).all()
        
#         if not decrypt:
#             return questions
        
#         # Decrypt questions
#         decrypted_questions = []
#         for question in questions:
#             try:
#                 decrypted_questions.append(question.get_decrypted_content())
#             except:
#                 continue
        
#         return decrypted_questions
    
#     @staticmethod
#     def get_question_by_id(question_id, decrypt=False):
#         """
#         Get a single question by ID
        
#         Args:
#             question_id: Question ID
#             decrypt: Whether to decrypt
            
#         Returns:
#             Question object or decrypted dictionary
#         """
#         question = Question.query.get(question_id)
        
#         if not question:
#             return None
        
#         if decrypt:
#             return question.get_decrypted_content()
        
#         return question
    
#     @staticmethod
#     def update_question(question_id, question_data):
#         """
#         Update a question
        
#         Args:
#             question_id: ID of question to update
#             question_data: New question data
            
#         Returns:
#             Updated question object
            
#         Raises:
#             ValidationError: If question not found
#             DatabaseError: If update fails
#         """
#         try:
#             question = Question.query.get(question_id)
            
#             if not question:
#                 raise ValidationError("Question not found")
            
#             # Update question number if provided
#             if 'question_number' in question_data:
#                 question.question_number = question_data['question_number']
            
#             # Update marks if provided
#             if 'marks' in question_data:
#                 question.marks = question_data['marks']
            
#             # Update encrypted content if question text or options changed
#             if 'question_text' in question_data or 'options' in question_data:
#                 # Get current decrypted content
#                 current_content = question.get_decrypted_content()
                
#                 # Update with new values
#                 question_content = {
#                     'question_text': question_data.get('question_text', current_content['question_text']),
#                     'options': question_data.get('options', current_content['options'])
#                 }
                
#                 # Re-encrypt
#                 question.encrypted_content = EncryptionService.encrypt_data(json.dumps(question_content))
            
#             # Update correct answer if provided
#             if 'correct_answer' in question_data:
#                 question.encrypted_answer = EncryptionService.encrypt_data(question_data['correct_answer'])
            
#             # Update explanation if provided
#             if 'explanation' in question_data:
#                 explanation = question_data['explanation']
#                 question.encrypted_explanation = EncryptionService.encrypt_data(explanation) if explanation else None
            
#             db.session.commit()
            
#             # Log update
#             AuditLog.log_action(
#                 action='update_question',
#                 details=f'Updated question {question_id}'
#             )
            
#             return question
            
#         except ValidationError:
#             raise
#         except Exception as e:
#             db.session.rollback()
#             raise DatabaseError(f"Error updating question: {str(e)}")
    
#     @staticmethod
#     def delete_question(question_id):
#         """
#         Delete a question
        
#         Args:
#             question_id: ID of question to delete
            
#         Raises:
#             ValidationError: If question not found
#             DatabaseError: If delete fails
#         """
#         try:
#             question = Question.query.get(question_id)
            
#             if not question:
#                 raise ValidationError("Question not found")
            
#             test_id = question.test_id
            
#             db.session.delete(question)
#             db.session.commit()
            
#             # Log deletion
#             AuditLog.log_action(
#                 action='delete_question',
#                 details=f'Deleted question {question_id} from test {test_id}'
#             )
            
#         except ValidationError:
#             raise
#         except Exception as e:
#             db.session.rollback()
#             raise DatabaseError(f"Error deleting question: {str(e)}")
    
#     @staticmethod
#     def delete_all_questions_for_test(test_id):
#         """
#         Delete all questions for a test
        
#         Args:
#             test_id: ID of the test
            
#         Returns:
#             int: Number of deleted questions
#         """
#         try:
#             count = Question.query.filter_by(test_id=test_id).delete()
#             db.session.commit()
            
#             # Log deletion
#             AuditLog.log_action(
#                 action='delete_test_questions',
#                 details=f'Deleted {count} questions from test {test_id}'
#             )
            
#             return count
            
#         except Exception as e:
#             db.session.rollback()
#             raise DatabaseError(f"Error deleting questions: {str(e)}")
    
#     @staticmethod
#     def get_question_count(test_id):
#         """
#         Get total number of questions for a test
        
#         Args:
#             test_id: ID of the test
            
#         Returns:
#             int: Question count
#         """
#         return Question.query.filter_by(test_id=test_id).count()
    
#     @staticmethod
#     def reorder_questions(test_id, question_order):
#         """
#         Reorder questions for a test
        
#         Args:
#             test_id: ID of the test
#             question_order: List of question IDs in desired order
            
#         Raises:
#             DatabaseError: If reorder fails
#         """
#         try:
#             for index, question_id in enumerate(question_order, start=1):
#                 question = Question.query.get(question_id)
#                 if question and question.test_id == test_id:
#                     question.question_number = index
            
#             db.session.commit()
            
#         except Exception as e:
#             db.session.rollback()
#             raise DatabaseError(f"Error reordering questions: {str(e)}")

"""
Question Service
Handles question CRUD operations with encryption
"""
from app.models.question import Question
from app.models.audit_log import AuditLog
from app.models.test import Test
from app.services.encryption_service import EncryptionService
from app.extensions.database import db
from app.utils.exceptions import ValidationError, DatabaseError
import json


class QuestionService:
    """Service for managing questions"""
    
    @staticmethod
    def create_question(test_id, question_data):
        """
        Create a single encrypted question
        
        Args:
            test_id: ID of the test
            question_data: Dictionary with question details
            
        Returns:
            Question object
            
        Raises:
            ValidationError: If validation fails
            DatabaseError: If database error occurs
        """
        try:
            # Validate question data
            if not question_data.get('question_text'):
                raise ValidationError("Question text is required")
            
            if not question_data.get('options'):
                raise ValidationError("Question options are required")
            
            if not question_data.get('correct_answer'):
                raise ValidationError("Correct answer is required")
            
            # Encrypt question text
            encrypted_question_text = EncryptionService.encrypt_data(question_data['question_text'])
            
            # Encrypt options (as JSON)
            encrypted_options = EncryptionService.encrypt_data(json.dumps(question_data['options']))
            
            # Encrypt correct answer
            encrypted_correct_answer = EncryptionService.encrypt_data(question_data['correct_answer'])
            
            # Encrypt explanation (if provided)
            explanation = question_data.get('explanation', '')
            encrypted_explanation = EncryptionService.encrypt_data(explanation) if explanation else None
            
            # Create question
            question = Question(
                test_id=test_id,
                question_number=question_data.get('question_number', 0),
                encrypted_question_text=encrypted_question_text,
                encrypted_options=encrypted_options,
                encrypted_correct_answer=encrypted_correct_answer,
                encrypted_explanation=encrypted_explanation,
                difficulty=question_data.get('difficulty', 'medium'),
                points=question_data.get('points', 1)
            )
            
            db.session.add(question)
            db.session.commit()
            
            return question
            
        except ValidationError:
            raise
        except Exception as e:
            db.session.rollback()
            raise DatabaseError(f"Error creating question: {str(e)}")
    
    @staticmethod
    def bulk_create_questions(test_id, questions_list):
        """
        Create multiple questions in a transaction
        
        Args:
            test_id: ID of the test
            questions_list: List of question dictionaries
            
        Returns:
            int: Count of created questions
            
        Raises:
            DatabaseError: If transaction fails
        """
        try:
            created_count = 0
            skipped_count = 0
            
            # Get the highest existing question number for this test
            existing_questions = Question.query.filter_by(test_id=test_id).all()
            if existing_questions:
                max_question_num = max(q.question_number for q in existing_questions)
                next_question_num = max_question_num + 1
            else:
                next_question_num = 1
            
            # Create questions with adjusted numbering
            for idx, question_data in enumerate(questions_list):
                try:
                    # Override question number to avoid conflicts
                    question_data['question_number'] = next_question_num + idx
                    
                    # Encrypt question data
                    encrypted_question_text = EncryptionService.encrypt_data(question_data['question_text'])
                    encrypted_options = EncryptionService.encrypt_data(json.dumps(question_data['options']))
                    encrypted_correct_answer = EncryptionService.encrypt_data(question_data['correct_answer'])
                    
                    explanation = question_data.get('explanation', '')
                    encrypted_explanation = EncryptionService.encrypt_data(explanation) if explanation else None
                    
                    # Create question object
                    question = Question(
                        test_id=test_id,
                        question_number=question_data['question_number'],
                        encrypted_question_text=encrypted_question_text,
                        encrypted_options=encrypted_options,
                        encrypted_correct_answer=encrypted_correct_answer,
                        encrypted_explanation=encrypted_explanation,
                        difficulty=question_data.get('difficulty', 'medium'),
                        points=question_data.get('points', 1)
                    )
                    
                    db.session.add(question)
                    created_count += 1
                    
                except Exception as e:
                    skipped_count += 1
                    continue
            
            # Commit all questions at once
            db.session.commit()
            
            # Update test's total question count
            test = Test.query.get(test_id)
            if test:
                test.update_question_count()
            
            # Log bulk creation
            AuditLog.log_action(
                action='bulk_create_questions',
                details=f'Created {created_count} questions for test {test_id}, skipped {skipped_count}'
            )
            
            return created_count
            
        except Exception as e:
            db.session.rollback()
            raise DatabaseError(f"Error in bulk question creation: {str(e)}")
    
    @staticmethod
    def get_questions_for_test(test_id, decrypt=False, include_answers=False):
        """
        Get all questions for a test
        
        Args:
            test_id: ID of the test
            decrypt: Whether to decrypt questions
            include_answers: Whether to include correct answers (for grading)
            
        Returns:
            List of question objects or dictionaries
        """
        questions = Question.query.filter_by(test_id=test_id).order_by(Question.question_number).all()
        
        if not decrypt:
            return questions
        
        # Decrypt questions
        decrypted_questions = []
        for question in questions:
            try:
                # Use to_dict with include_answer parameter for grading
                decrypted_content = question.to_dict(decrypt=True, include_answer=include_answers)
                if decrypted_content and 'question_text' in decrypted_content:
                    decrypted_questions.append(decrypted_content)
            except Exception as e:
                # Log error but continue with other questions
                continue
        
        return decrypted_questions
    
    @staticmethod
    def get_question_by_id(question_id, decrypt=False):
        """
        Get a single question by ID
        
        Args:
            question_id: Question ID
            decrypt: Whether to decrypt
            
        Returns:
            Question object or decrypted dictionary
        """
        question = Question.query.get(question_id)
        
        if not question:
            return None
        
        if decrypt:
            return question.get_decrypted_content()
        
        return question
    
    @staticmethod
    def decrypt_question(question):
        """
        Decrypt a single question object
        
        Args:
            question: Question object to decrypt
            
        Returns:
            Decrypted question dictionary
        """
        if not question:
            return None
        
        try:
            return question.to_dict(decrypt=True, include_answer=False)
        except Exception as e:
            print(f"Error decrypting question {question.id}: {str(e)}")
            return None
    
    @staticmethod
    def update_question(question_id, question_data):
        """
        Update a question
        
        Args:
            question_id: ID of question to update
            question_data: New question data
            
        Returns:
            Updated question object
            
        Raises:
            ValidationError: If question not found
            DatabaseError: If update fails
        """
        try:
            question = Question.query.get(question_id)
            
            if not question:
                raise ValidationError("Question not found")
            
            # Update question number if provided
            if 'question_number' in question_data:
                question.question_number = question_data['question_number']
            
            # Update marks if provided
            if 'marks' in question_data:
                question.marks = question_data['marks']
            
            # Update encrypted question text if provided
            if 'question_text' in question_data:
                question.encrypted_question_text = EncryptionService.encrypt_data(question_data['question_text'])
            
            # Update encrypted options if provided
            if 'options' in question_data:
                question.encrypted_options = EncryptionService.encrypt_data(json.dumps(question_data['options']))
            
            # Update correct answer if provided
            if 'correct_answer' in question_data:
                question.encrypted_correct_answer = EncryptionService.encrypt_data(question_data['correct_answer'])
            
            # Update explanation if provided
            if 'explanation' in question_data:
                explanation = question_data['explanation']
                question.encrypted_explanation = EncryptionService.encrypt_data(explanation) if explanation else None
            
            db.session.commit()
            
            # Log update
            AuditLog.log_action(
                action='update_question',
                details=f'Updated question {question_id}'
            )
            
            return question
            
        except ValidationError:
            raise
        except Exception as e:
            db.session.rollback()
            raise DatabaseError(f"Error updating question: {str(e)}")
    
    @staticmethod
    def delete_question(question_id):
        """
        Delete a question
        
        Args:
            question_id: ID of question to delete
            
        Raises:
            ValidationError: If question not found
            DatabaseError: If delete fails
        """
        try:
            question = Question.query.get(question_id)
            
            if not question:
                raise ValidationError("Question not found")
            
            test_id = question.test_id
            
            db.session.delete(question)
            db.session.commit()
            
            # Log deletion
            AuditLog.log_action(
                action='delete_question',
                details=f'Deleted question {question_id} from test {test_id}'
            )
            
        except ValidationError:
            raise
        except Exception as e:
            db.session.rollback()
            raise DatabaseError(f"Error deleting question: {str(e)}")
    
    @staticmethod
    def delete_all_questions_for_test(test_id):
        """
        Delete all questions for a test
        
        Args:
            test_id: ID of the test
            
        Returns:
            int: Number of deleted questions
        """
        try:
            count = Question.query.filter_by(test_id=test_id).delete()
            db.session.commit()
            
            # Log deletion
            AuditLog.log_action(
                action='delete_test_questions',
                details=f'Deleted {count} questions from test {test_id}'
            )
            
            return count
            
        except Exception as e:
            db.session.rollback()
            raise DatabaseError(f"Error deleting questions: {str(e)}")
    
    @staticmethod
    def get_question_count(test_id):
        """
        Get total number of questions for a test
        
        Args:
            test_id: ID of the test
            
        Returns:
            int: Question count
        """
        return Question.query.filter_by(test_id=test_id).count()
    
    @staticmethod
    def reorder_questions(test_id, question_order):
        """
        Reorder questions for a test
        
        Args:
            test_id: ID of the test
            question_order: List of question IDs in desired order
            
        Raises:
            DatabaseError: If reorder fails
        """
        try:
            for index, question_id in enumerate(question_order, start=1):
                question = Question.query.get(question_id)
                if question and question.test_id == test_id:
                    question.question_number = index
            
            db.session.commit()
            
        except Exception as e:
            db.session.rollback()
            raise DatabaseError(f"Error reordering questions: {str(e)}")
"""
Test Service
Handles test CRUD operations
"""
from app.models.test import Test
from app.models.audit_log import AuditLog
from app.services.question_service import QuestionService
from app.extensions.database import db
from app.utils.exceptions import ValidationError, DatabaseError
from datetime import datetime


class TestService:
    """Service for managing tests"""
    
    @staticmethod
    def create_test(name, subject, duration, teacher_id, **kwargs):
        """
        Create a new test
        
        Args:
            name: Test name
            subject: Subject name
            duration: Duration in minutes
            teacher_id: ID of teacher creating the test
            **kwargs: Additional fields
            
        Returns:
            Test object
            
        Raises:
            ValidationError: If validation fails
            DatabaseError: If database error occurs
        """
        try:
            # Validate inputs
            if not name or not name.strip():
                raise ValidationError("Test name is required")
            
            if not subject or not subject.strip():
                raise ValidationError("Subject is required")
            
            if not duration or duration <= 0:
                raise ValidationError("Duration must be greater than 0")
            
            # Create test
            test = Test(
                name=name.strip(),
                subject=subject.strip(),
                duration=duration,
                created_by=teacher_id,
                description=kwargs.get('description'),
                pass_percentage=kwargs.get('pass_percentage', 50.0),
                is_active=kwargs.get('is_active', True),
                is_published=kwargs.get('is_published', False)
            )
            
            db.session.add(test)
            db.session.commit()
            
            # Log creation
            AuditLog.log_action(
                action='create_test',
                details=f'Created test: {name}'
            )
            
            return test
            
        except ValidationError:
            raise
        except Exception as e:
            db.session.rollback()
            raise DatabaseError(f"Error creating test: {str(e)}")
    
    @staticmethod
    def get_tests_by_teacher(teacher_id, include_inactive=False):
        """
        Get all tests created by a teacher
        
        Args:
            teacher_id: ID of the teacher
            include_inactive: Whether to include inactive tests
            
        Returns:
            List of test objects with question counts
        """
        query = Test.query.filter_by(created_by=teacher_id)
        
        if not include_inactive:
            query = query.filter_by(is_active=True)
        
        tests = query.order_by(Test.created_at.desc()).all()
        
        # Add question count to each test
        test_list = []
        for test in tests:
            test_dict = test.to_dict()
            test_dict['question_count'] = QuestionService.get_question_count(test.id)
            test_list.append(test_dict)
        
        return test_list
    
    @staticmethod
    def get_all_tests(active_only=True):
        """
        Get all tests (for admin use)
        
        Args:
            active_only: Whether to return only active tests
            
        Returns:
            List of tests
        """
        query = Test.query
        
        if active_only:
            query = query.filter_by(is_active=True)
        
        tests = query.order_by(Test.created_at.desc()).all()
        
        # Add question count
        test_list = []
        for test in tests:
            test_dict = test.to_dict()
            test_dict['question_count'] = QuestionService.get_question_count(test.id)
            test_list.append(test_dict)
        
        return test_list
    
    @staticmethod
    def get_test_by_id(test_id, include_question_count=True):
        """
        Get a single test by ID
        
        Args:
            test_id: Test ID
            include_question_count: Whether to include question count
            
        Returns:
            Test object or dictionary with question count
        """
        test = Test.query.get(test_id)
        
        if not test:
            return None
        
        if include_question_count:
            test_dict = test.to_dict()
            test_dict['question_count'] = QuestionService.get_question_count(test.id)
            return test_dict
        
        return test
    
    @staticmethod
    def update_test(test_id, **kwargs):
        """
        Update test details
        
        Args:
            test_id: ID of test to update
            **kwargs: Fields to update
            
        Returns:
            Updated test object
            
        Raises:
            ValidationError: If test not found or validation fails
            DatabaseError: If update fails
        """
        try:
            test = Test.query.get(test_id)
            
            if not test:
                raise ValidationError("Test not found")
            
            # Update fields
            if 'name' in kwargs and kwargs['name']:
                test.name = kwargs['name'].strip()
            
            if 'subject' in kwargs and kwargs['subject']:
                test.subject = kwargs['subject'].strip()
            
            if 'duration' in kwargs:
                if kwargs['duration'] <= 0:
                    raise ValidationError("Duration must be greater than 0")
                test.duration = kwargs['duration']
            
            if 'description' in kwargs:
                test.description = kwargs['description']
            
            if 'pass_percentage' in kwargs:
                pass_pct = kwargs['pass_percentage']
                if pass_pct < 0 or pass_pct > 100:
                    raise ValidationError("Pass percentage must be between 0 and 100")
                test.pass_percentage = pass_pct
            
            if 'is_active' in kwargs:
                test.is_active = kwargs['is_active']
            
            if 'is_published' in kwargs:
                test.is_published = kwargs['is_published']
            
            test.updated_at = datetime.utcnow()
            
            db.session.commit()
            
            # Log update
            AuditLog.log_action(
                action='update_test',
                details=f'Updated test {test_id}: {test.name}'
            )
            
            return test
            
        except ValidationError:
            raise
        except Exception as e:
            db.session.rollback()
            raise DatabaseError(f"Error updating test: {str(e)}")
    
    @staticmethod
    def delete_test(test_id):
        """
        Delete a test and all its questions (cascade)
        
        Args:
            test_id: ID of test to delete
            
        Raises:
            ValidationError: If test not found
            DatabaseError: If delete fails
        """
        try:
            test = Test.query.get(test_id)
            
            if not test:
                raise ValidationError("Test not found")
            
            test_name = test.name
            
            # Delete all questions for this test
            QuestionService.delete_all_questions_for_test(test_id)
            
            # Delete test
            db.session.delete(test)
            db.session.commit()
            
            # Log deletion
            AuditLog.log_action(
                action='delete_test',
                details=f'Deleted test {test_id}: {test_name}'
            )
            
        except ValidationError:
            raise
        except Exception as e:
            db.session.rollback()
            raise DatabaseError(f"Error deleting test: {str(e)}")
    
    @staticmethod
    def publish_test(test_id):
        """
        Publish a test (make it available for students)
        
        Args:
            test_id: ID of test to publish
            
        Returns:
            Updated test object
            
        Raises:
            ValidationError: If test cannot be published
        """
        try:
            test = Test.query.get(test_id)
            
            if not test:
                raise ValidationError("Test not found")
            
            # Check if test has questions
            question_count = QuestionService.get_question_count(test_id)
            if question_count == 0:
                raise ValidationError("Cannot publish test without questions")
            
            test.is_published = True
            test.updated_at = datetime.utcnow()
            
            db.session.commit()
            
            # Log publication
            AuditLog.log_action(
                action='publish_test',
                details=f'Published test {test_id}: {test.name}'
            )
            
            return test
            
        except ValidationError:
            raise
        except Exception as e:
            db.session.rollback()
            raise DatabaseError(f"Error publishing test: {str(e)}")
    
    @staticmethod
    def unpublish_test(test_id):
        """
        Unpublish a test
        
        Args:
            test_id: ID of test to unpublish
            
        Returns:
            Updated test object
        """
        try:
            test = Test.query.get(test_id)
            
            if not test:
                raise ValidationError("Test not found")
            
            test.is_published = False
            test.updated_at = datetime.utcnow()
            
            db.session.commit()
            
            # Log action
            AuditLog.log_action(
                action='unpublish_test',
                details=f'Unpublished test {test_id}: {test.name}'
            )
            
            return test
            
        except ValidationError:
            raise
        except Exception as e:
            db.session.rollback()
            raise DatabaseError(f"Error unpublishing test: {str(e)}")
    
    @staticmethod
    def get_test_statistics(teacher_id=None):
        """
        Get test statistics
        
        Args:
            teacher_id: Optional teacher ID to filter by
            
        Returns:
            Dictionary with statistics
        """
        query = Test.query
        
        if teacher_id:
            query = query.filter_by(created_by=teacher_id)
        
        total_tests = query.count()
        active_tests = query.filter_by(is_active=True).count()
        published_tests = query.filter_by(is_published=True).count()
        
        return {
            'total_tests': total_tests,
            'active_tests': active_tests,
            'published_tests': published_tests,
            'draft_tests': total_tests - published_tests
        }

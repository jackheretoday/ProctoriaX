"""Test services"""
import pytest
from app.services.auth_service import AuthService
from app.services.test_service import TestService
from app.services.question_service import QuestionService
from app.utils.exceptions import ValidationError


class TestAuthService:
    """Test AuthService"""
    
    def test_create_user(self, db_session):
        """Test user creation"""
        user = AuthService.create_user(
            username='newuser',
            email='new@test.com',
            password='New@123',
            full_name='New User',
            role='student'
        )
        
        assert user is not None
        assert user.username == 'newuser'
        assert user.check_password('New@123')
    
    def test_authenticate(self, db_session, admin_user):
        """Test authentication"""
        user = AuthService.authenticate('admin', 'Admin@123')
        assert user is not None
        assert user.id == admin_user.id
        
        # Wrong password
        user = AuthService.authenticate('admin', 'wrong')
        assert user is None


class TestTestService:
    """Test TestService"""
    
    def test_create_test(self, db_session, teacher_user):
        """Test test creation"""
        test = TestService.create_test(
            name='New Test',
            subject='Science',
            duration=45,
            teacher_id=teacher_user.id
        )
        
        assert test is not None
        assert test.name == 'New Test'
        assert test.duration == 45
    
    def test_publish_test(self, db_session, sample_test, sample_questions):
        """Test publishing test"""
        TestService.publish_test(sample_test.id)
        test = TestService.get_test_by_id(sample_test.id)
        
        assert test['is_published'] is True


class TestQuestionService:
    """Test QuestionService"""
    
    def test_bulk_create(self, db_session, sample_test):
        """Test bulk question creation"""
        questions = [
            {
                'question_number': 1,
                'question_text': 'Q1',
                'options': {'A': '1', 'B': '2', 'C': '3', 'D': '4'},
                'correct_answer': 'A',
                'explanation': 'Exp1'
            }
        ]
        
        count = QuestionService.bulk_create_questions(sample_test.id, questions)
        assert count == 1
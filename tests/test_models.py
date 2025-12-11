"""Test database models"""
import pytest
from datetime import datetime
from app.models.user import User
from app.models.test import Test
from app.models.question import Question


class TestUserModel:
    """Test User model"""
    
    def test_create_user(self, db_session):
        """Test user creation"""
        user = User(
            username='testuser',
            email='test@example.com',
            role='student',
            full_name='Test User'
        )
        user.set_password('Test@123')
        db_session.add(user)
        db_session.commit()
        
        assert user.id is not None
        assert user.username == 'testuser'
        assert user.check_password('Test@123')
    
    def test_password_hashing(self, db_session, admin_user):
        """Test password is hashed"""
        assert admin_user.password_hash is not None
        assert admin_user.password_hash != 'Admin@123'
        assert admin_user.check_password('Admin@123')
        assert not admin_user.check_password('wrong')


class TestTestModel:
    """Test Test model"""
    
    def test_create_test(self, db_session, teacher_user):
        """Test test creation"""
        test = Test(
            name='Math Test',
            subject='Mathematics',
            duration=60,
            created_by=teacher_user.id
        )
        db_session.add(test)
        db_session.commit()
        
        assert test.id is not None
        assert test.name == 'Math Test'
        assert test.is_active is True
        assert test.is_published is False


class TestQuestionModel:
    """Test Question model"""
    
    def test_create_question(self, db_session, sample_test):
        """Test question creation"""
        question = Question(
            test_id=sample_test.id,
            question_number=1,
            encrypted_question='encrypted',
            encrypted_options='encrypted',
            encrypted_answer='encrypted'
        )
        db_session.add(question)
        db_session.commit()
        
        assert question.id is not None
        assert question.question_number == 1
"""Pytest configuration and fixtures for testing"""
import pytest
import os
import sys
from datetime import datetime, timedelta

# Add app to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.extensions.database import db
from app.models.user import User
from app.models.test import Test
from app.models.question import Question
from app.models.assignment import Assignment
from app.models.result import Result
from app.services.encryption_service import EncryptionService


@pytest.fixture(scope='session')
def app():
    """Create application for testing"""
    os.environ['TESTING'] = 'True'
    os.environ['SECRET_KEY'] = 'test-secret-key-12345'
    os.environ['ENCRYPTION_KEY'] = 'test-encryption-key-32-bytes-long!!!'
    
    app = create_app('testing')
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope='function')
def client(app):
    """Test client"""
    return app.test_client()


@pytest.fixture(scope='function')
def db_session(app):
    """Database session for testing"""
    with app.app_context():
        # Clear all tables
        db.session.remove()
        db.drop_all()
        db.create_all()
        yield db
        db.session.rollback()


@pytest.fixture
def admin_user(db_session):
    """Create admin user"""
    from app.services.auth_service import AuthService
    admin = AuthService.create_user(
        username='admin',
        email='admin@test.com',
        password='Admin@123',
        full_name='Test Admin',
        role='admin'
    )
    return admin


@pytest.fixture
def teacher_user(db_session):
    """Create teacher user"""
    from app.services.auth_service import AuthService
    teacher = AuthService.create_user(
        username='teacher',
        email='teacher@test.com',
        password='Teacher@123',
        full_name='Test Teacher',
        role='teacher'
    )
    return teacher


@pytest.fixture
def student_user(db_session):
    """Create student user"""
    from app.services.auth_service import AuthService
    student = AuthService.create_user(
        username='student',
        email='student@test.com',
        password='Student@123',
        full_name='Test Student',
        roll_number='STU001',
        role='student'
    )
    return student


@pytest.fixture
def sample_test(db_session, teacher_user):
    """Create sample test"""
    from app.services.test_service import TestService
    test = TestService.create_test(
        name='Sample Test',
        subject='Python',
        duration=60,
        teacher_id=teacher_user.id,
        description='Test Description'
    )
    return test


@pytest.fixture
def sample_questions(db_session, sample_test):
    """Create sample questions"""
    from app.services.question_service import QuestionService
    
    questions_data = [
        {
            'question_number': 1,
            'question_text': 'What is Python?',
            'options': {
                'A': 'A snake',
                'B': 'A programming language',
                'C': 'A game',
                'D': 'None'
            },
            'correct_answer': 'B',
            'explanation': 'Python is a programming language'
        },
        {
            'question_number': 2,
            'question_text': 'What is Flask?',
            'options': {
                'A': 'A bottle',
                'B': 'A web framework',
                'C': 'A database',
                'D': 'None'
            },
            'correct_answer': 'B',
            'explanation': 'Flask is a web framework'
        }
    ]
    
    count = QuestionService.bulk_create_questions(sample_test.id, questions_data)
    questions = QuestionService.get_questions_for_test(sample_test.id, decrypt=False)
    return questions


@pytest.fixture
def authenticated_admin(client, admin_user):
    """Authenticate as admin"""
    with client.session_transaction() as session:
        session['user_id'] = admin_user.id
        session['_fresh'] = True
    return client


@pytest.fixture
def authenticated_teacher(client, teacher_user):
    """Authenticate as teacher"""
    with client.session_transaction() as session:
        session['user_id'] = teacher_user.id
        session['_fresh'] = True
    return client


@pytest.fixture
def authenticated_student(client, student_user):
    """Authenticate as student"""
    with client.session_transaction() as session:
        session['user_id'] = student_user.id
        session['_fresh'] = True
    return client
#!/usr/bin/env python3
"""Seed database with realistic test data"""
import sys
import os
from datetime import datetime, timedelta

# Add app to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.extensions.database import db
from app.services.auth_service import AuthService
from app.services.test_service import TestService
from app.services.question_service import QuestionService
from app.services.terms_service import TermsService
from app.models.assignment import Assignment
from app.models.result import Result


def seed_users():
    """Create sample users"""
    print("Creating users...")
    
    # Admin
    admin = AuthService.create_user(
        username='admin',
        email='admin@example.com',
        password='Admin@123',
        full_name='System Administrator',
        role='admin'
    )
    print(f"  ✓ Admin created: {admin.username}")
    
    # Teachers
    teachers = []
    for i in range(1, 4):
        teacher = AuthService.create_user(
            username=f'teacher{i}',
            email=f'teacher{i}@example.com',
            password='Teacher@123',
            full_name=f'Teacher {i}',
            role='teacher'
        )
        teachers.append(teacher)
        print(f"  ✓ Teacher created: {teacher.username}")
    
    # Students
    students = []
    for i in range(1, 21):
        student = AuthService.create_user(
            username=f'student{i}',
            email=f'student{i}@example.com',
            password='Student@123',
            full_name=f'Student {i}',
            roll_number=f'STU{str(i).zfill(3)}',
            role='student'
        )
        students.append(student)
    print(f"  ✓ {len(students)} students created")
    
    return admin, teachers, students


def seed_tests(teachers):
    """Create sample tests"""
    print("\nCreating tests...")
    
    tests_data = [
        {
            'name': 'Python Basics',
            'subject': 'Computer Science',
            'duration': 60,
            'description': 'Introduction to Python programming'
        },
        {
            'name': 'Data Structures',
            'subject': 'Computer Science',
            'duration': 90,
            'description': 'Arrays, Lists, Trees, Graphs'
        },
        {
            'name': 'Web Development',
            'subject': 'Web Technologies',
            'duration': 45,
            'description': 'HTML, CSS, JavaScript basics'
        }
    ]
    
    tests = []
    for i, test_data in enumerate(tests_data):
        teacher = teachers[i % len(teachers)]
        test = TestService.create_test(
            name=test_data['name'],
            subject=test_data['subject'],
            duration=test_data['duration'],
            teacher_id=teacher.id,
            description=test_data['description']
        )
        tests.append(test)
        print(f"  ✓ Test created: {test.name}")
    
    return tests


def seed_questions(tests):
    """Create sample questions for tests"""
    print("\nCreating questions...")
    
    python_questions = [
        {
            'question_number': 1,
            'question_text': 'What is Python?',
            'options': {
                'A': 'A snake',
                'B': 'A programming language',
                'C': 'A database',
                'D': 'An operating system'
            },
            'correct_answer': 'B',
            'explanation': 'Python is a high-level programming language known for its simplicity and readability.'
        },
        {
            'question_number': 2,
            'question_text': 'What is the output of: print(type([]))?',
            'options': {
                'A': '<class "list">',
                'B': '<class "dict">',
                'C': '<class "tuple">',
                'D': '<class "set">'
            },
            'correct_answer': 'A',
            'explanation': '[] creates an empty list, so type([]) returns <class "list">.'
        },
        {
            'question_number': 3,
            'question_text': 'Which keyword is used to define a function in Python?',
            'options': {
                'A': 'function',
                'B': 'def',
                'C': 'func',
                'D': 'define'
            },
            'correct_answer': 'B',
            'explanation': 'The "def" keyword is used to define functions in Python.'
        }
    ]
    
    ds_questions = [
        {
            'question_number': 1,
            'question_text': 'What is the time complexity of searching in a balanced binary search tree?',
            'options': {
                'A': 'O(1)',
                'B': 'O(log n)',
                'C': 'O(n)',
                'D': 'O(n log n)'
            },
            'correct_answer': 'B',
            'explanation': 'In a balanced BST, search operation takes O(log n) time.'
        },
        {
            'question_number': 2,
            'question_text': 'Which data structure uses LIFO principle?',
            'options': {
                'A': 'Queue',
                'B': 'Stack',
                'C': 'Tree',
                'D': 'Graph'
            },
            'correct_answer': 'B',
            'explanation': 'Stack follows Last In First Out (LIFO) principle.'
        }
    ]
    
    web_questions = [
        {
            'question_number': 1,
            'question_text': 'What does HTML stand for?',
            'options': {
                'A': 'Hyper Text Markup Language',
                'B': 'High Tech Modern Language',
                'C': 'Home Tool Markup Language',
                'D': 'Hyperlinks and Text Markup Language'
            },
            'correct_answer': 'A',
            'explanation': 'HTML stands for Hyper Text Markup Language.'
        }
    ]
    
    all_questions = [python_questions, ds_questions, web_questions]
    
    for test, questions in zip(tests, all_questions):
        count = QuestionService.bulk_create_questions(test.id, questions)
        print(f"  ✓ {count} questions added to '{test.name}'")


def seed_terms(tests):
    """Create terms & conditions for tests"""
    print("\nCreating terms & conditions...")
    
    terms_list = [
        "You must complete the test in one sitting",
        "No external resources are allowed",
        "Timer starts when you begin the test",
        "You cannot go back to previous questions",
        "Each answer is final once submitted"
    ]
    
    for test in tests:
        TermsService.create_terms(test.id, terms_list)
        print(f"  ✓ Terms added to '{test.name}'")


def seed_assignments(tests, students):
    """Create test assignments"""
    print("\nCreating assignments...")
    
    count = 0
    for test in tests:
        # Assign to first 10 students
        for student in students[:10]:
            assignment = Assignment(
                test_id=test.id,
                student_id=student.id,
                assigned_date=datetime.now().date()
            )
            db.session.add(assignment)
            count += 1
    
    db.session.commit()
    print(f"  ✓ {count} assignments created")


def seed_results(tests, students):
    """Create sample results"""
    print("\nCreating sample results...")
    
    import random
    
    count = 0
    # Create results for first test, first 5 students
    test = tests[0]
    for student in students[:5]:
        total = 3
        correct = random.randint(1, 3)
        wrong = random.randint(0, total - correct)
        unattempted = total - correct - wrong
        percentage = round((correct / total) * 100, 2)
        
        result = Result(
            student_id=student.id,
            test_id=test.id,
            total_questions=total,
            correct_answers=correct,
            wrong_answers=wrong,
            unattempted=unattempted,
            score=correct,
            percentage=percentage,
            time_taken=random.randint(30, 60),
            status='completed',
            completed_at=datetime.now()
        )
        db.session.add(result)
        count += 1
    
    db.session.commit()
    print(f"  ✓ {count} results created")


def main():
    """Main seeding function"""
    print("="*50)
    print("Database Seeding Script")
    print("="*50)
    
    app = create_app()
    
    with app.app_context():
        # Clear existing data (optional)
        response = input("\nClear existing data? (y/N): ")
        if response.lower() == 'y':
            print("\nClearing database...")
            db.drop_all()
            db.create_all()
            print("  ✓ Database cleared")
        
        # Seed data
        admin, teachers, students = seed_users()
        tests = seed_tests(teachers)
        seed_questions(tests)
        seed_terms(tests)
        
        # Publish tests
        print("\nPublishing tests...")
        for test in tests:
            TestService.publish_test(test.id)
            print(f"  ✓ Published: {test.name}")
        
        seed_assignments(tests, students)
        seed_results(tests, students)
        
        print("\n" + "="*50)
        print("✓ Database seeding completed successfully!")
        print("="*50)
        print("\nLogin Credentials:")
        print("  Admin: admin / Admin@123")
        print("  Teacher: teacher1 / Teacher@123")
        print("  Student: student1 / Student@123")
        print("="*50)


if __name__ == '__main__':
    main()
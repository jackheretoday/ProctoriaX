"""Integration tests - end-to-end workflows"""
import pytest
from datetime import datetime, timedelta


class TestTeacherWorkflow:
    """Test teacher workflow from test creation to viewing results"""
    
    def test_complete_workflow(self, db_session, teacher_user, student_user):
        """Test complete teacher workflow"""
        from app.services.test_service import TestService
        from app.services.question_service import QuestionService
        from app.models.assignment import Assignment
        
        # 1. Create test
        test = TestService.create_test(
            name='Integration Test',
            subject='Python',
            duration=30,
            teacher_id=teacher_user.id
        )
        assert test is not None
        
        # 2. Add questions
        questions = [
            {
                'question_number': 1,
                'question_text': 'What is 2+2?',
                'options': {'A': '3', 'B': '4', 'C': '5', 'D': '6'},
                'correct_answer': 'B',
                'explanation': '2+2=4'
            }
        ]
        count = QuestionService.bulk_create_questions(test.id, questions)
        assert count == 1
        
        # 3. Publish test
        TestService.publish_test(test.id)
        updated_test = TestService.get_test_by_id(test.id)
        assert updated_test['is_published'] is True
        
        # 4. Assign to student
        assignment = Assignment(
            test_id=test.id,
            student_id=student_user.id,
            assigned_date=datetime.now().date()
        )
        db_session.add(assignment)
        db_session.commit()
        
        assert assignment.id is not None


class TestStudentWorkflow:
    """Test student taking test workflow"""
    
    def test_complete_workflow(self, db_session, sample_test, sample_questions, student_user):
        """Test complete student workflow"""
        from app.services.result_service import ResultService
        from app.models.result import Result
        from app.models.assignment import Assignment
        
        # 1. Assign test
        assignment = Assignment(
            test_id=sample_test.id,
            student_id=student_user.id,
            assigned_date=datetime.now().date()
        )
        db_session.add(assignment)
        db_session.commit()
        
        # 2. Submit result
        result = Result(
            student_id=student_user.id,
            test_id=sample_test.id,
            total_questions=2,
            correct_answers=1,
            wrong_answers=1,
            unattempted=0,
            score=1,
            percentage=50.0,
            time_taken=25,
            status='completed'
        )
        db_session.add(result)
        db_session.commit()
        
        assert result.id is not None
        assert result.percentage == 50.0
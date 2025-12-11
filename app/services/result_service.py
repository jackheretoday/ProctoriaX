"""
Result Service
Handles result retrieval and statistics
"""
from app.models.result import Result
from app.models.user import User
from app.models.test import Test
from app.extensions.database import db
from sqlalchemy import func


class ResultService:
    """Service for managing results"""
    
    @staticmethod
    def get_results_for_test(test_id):
        """
        Get all results for a specific test
        
        Args:
            test_id: ID of the test
            
        Returns:
            List of result dictionaries with student details
        """
        results = Result.query.filter_by(test_id=test_id).all()
        
        result_list = []
        for result in results:
            # Get student details
            student = User.query.get(result.student_id)
            
            # Handle legacy results that might not have incorrect_answers
            incorrect_answers = getattr(result, 'incorrect_answers', None)
            if incorrect_answers is None:
                # Calculate from total - correct - unanswered
                unanswered = getattr(result, 'unanswered', 0)
                incorrect_answers = result.total_questions - result.correct_answers - unanswered
            
            unanswered = getattr(result, 'unanswered', 0)
            
            result_dict = {
                'id': result.id,
                'student_id': student.id if student else None,
                'student_name': student.full_name if student else 'Unknown',
                'student_username': student.username if student else 'Unknown',
                'student_email': student.email if student else 'Unknown',
                'roll_number': student.student_id if student and student.student_id else 'N/A',
                'total_questions': result.total_questions,
                'correct_answers': result.correct_answers,
                'incorrect_answers': incorrect_answers,
                'unanswered': unanswered,
                'score': result.score,
                'percentage': result.percentage,
                'completed_at': result.completed_at.strftime('%Y-%m-%d %H:%M:%S') if result.completed_at else None,
                'time_taken': result.time_taken
            }
            
            result_list.append(result_dict)
        
        # Sort by percentage (highest first)
        result_list.sort(key=lambda x: x['percentage'], reverse=True)
        
        return result_list
    
    @staticmethod
    def get_result_by_id(result_id):
        """
        Get a single result by ID
        
        Args:
            result_id: Result ID
            
        Returns:
            Result dictionary with details
        """
        result = Result.query.get(result_id)
        
        if not result:
            return None
        
        student = User.query.get(result.student_id)
        test = Test.query.get(result.test_id)
        
        # Handle legacy results
        incorrect_answers = getattr(result, 'incorrect_answers', None)
        if incorrect_answers is None:
            unanswered = getattr(result, 'unanswered', 0)
            incorrect_answers = result.total_questions - result.correct_answers - unanswered
        
        unanswered = getattr(result, 'unanswered', 0)
        
        result_dict = {
            'id': result.id,
            'student_id': student.id if student else None,
            'student_name': student.full_name if student else 'Unknown',
            'student_username': student.username if student else 'Unknown',
            'student_email': student.email if student else 'Unknown',
            'roll_number': student.student_id if student and student.student_id else 'N/A',
            'test_id': test.id if test else None,
            'test_name': test.name if test else 'Unknown',
            'test_subject': test.subject if test else 'Unknown',
            'total_questions': result.total_questions,
            'correct_answers': result.correct_answers,
            'incorrect_answers': incorrect_answers,
            'unanswered': unanswered,
            'score': result.score,
            'percentage': result.percentage,
            'completed_at': result.completed_at.strftime('%Y-%m-%d %H:%M:%S') if result.completed_at else None,
            'time_taken': result.time_taken
        }
        
        return result_dict
    
    @staticmethod
    def get_result_statistics(test_id):
        """
        Get statistics for a test
        
        Args:
            test_id: ID of the test
            
        Returns:
            Dictionary with statistics
        """
        results = Result.query.filter_by(test_id=test_id).all()
        
        if not results:
            return {
                'total_attempts': 0,
                'average_score': 0,
                'average_percentage': 0,
                'highest_score': 0,
                'lowest_score': 0,
                'highest_percentage': 0,
                'lowest_percentage': 0,
                'pass_count': 0,
                'fail_count': 0,
                'pass_rate': 0
            }
        
        # Get test details for passing percentage
        test = Test.query.get(test_id)
        passing_percentage = 50.0  # Default 50%
        if test and hasattr(test, 'pass_percentage') and test.pass_percentage:
            passing_percentage = test.pass_percentage
        
        # Calculate statistics
        total_attempts = len(results)
        scores = [r.score for r in results]
        percentages = [r.percentage for r in results]
        
        average_score = sum(scores) / total_attempts
        average_percentage = sum(percentages) / total_attempts
        highest_score = max(scores)
        lowest_score = min(scores)
        highest_percentage = max(percentages)
        lowest_percentage = min(percentages)
        
        # Calculate pass/fail count
        pass_count = sum(1 for r in results if r.percentage >= passing_percentage)
        fail_count = total_attempts - pass_count
        pass_rate = (pass_count / total_attempts) * 100 if total_attempts > 0 else 0
        
        return {
            'total_attempts': total_attempts,
            'average_score': round(average_score, 2),
            'average_percentage': round(average_percentage, 2),
            'highest_score': highest_score,
            'lowest_score': lowest_score,
            'highest_percentage': round(highest_percentage, 2),
            'lowest_percentage': round(lowest_percentage, 2),
            'pass_count': pass_count,
            'fail_count': fail_count,
            'pass_rate': round(pass_rate, 2)
        }
    
    @staticmethod
    def get_results_by_student(student_id):
        """
        Get all results for a specific student
        
        Args:
            student_id: ID of the student
            
        Returns:
            List of result dictionaries with test details
        """
        results = Result.query.filter_by(student_id=student_id).all()
        
        result_list = []
        for result in results:
            test = Test.query.get(result.test_id)
            
            # Handle legacy results
            incorrect_answers = getattr(result, 'incorrect_answers', None)
            if incorrect_answers is None:
                unanswered = getattr(result, 'unanswered', 0)
                incorrect_answers = result.total_questions - result.correct_answers - unanswered
            
            unanswered = getattr(result, 'unanswered', 0)
            
            result_dict = {
                'id': result.id,
                'test_id': test.id if test else None,
                'test_name': test.name if test else 'Unknown',
                'test_subject': test.subject if test else 'Unknown',
                'total_questions': result.total_questions,
                'correct_answers': result.correct_answers,
                'incorrect_answers': incorrect_answers,
                'unanswered': unanswered,
                'score': result.score,
                'percentage': result.percentage,
                'completed_at': result.completed_at.strftime('%Y-%m-%d %H:%M:%S') if result.completed_at else None,
                'time_taken': result.time_taken
            }
            
            result_list.append(result_dict)
        
        # Sort by completion date (most recent first)
        result_list.sort(key=lambda x: x['completed_at'] if x['completed_at'] else '', reverse=True)
        
        return result_list
    
    @staticmethod
    def get_top_performers(test_id, limit=10):
        """
        Get top performers for a test
        
        Args:
            test_id: ID of the test
            limit: Number of top performers to return
            
        Returns:
            List of top result dictionaries
        """
        results = Result.query.filter_by(test_id=test_id)\
            .order_by(Result.percentage.desc())\
            .limit(limit)\
            .all()
        
        result_list = []
        for result in results:
            student = User.query.get(result.student_id)
            
            result_dict = {
                'student_name': student.full_name if student else 'Unknown',
                'student_username': student.username if student else 'Unknown',
                'roll_number': student.student_id if student and student.student_id else 'N/A',
                'score': result.score,
                'percentage': result.percentage,
                'completed_at': result.completed_at.strftime('%Y-%m-%d %H:%M:%S') if result.completed_at else None
            }
            
            result_list.append(result_dict)
        
        return result_list
    
    @staticmethod
    def get_teacher_results_summary(teacher_id):
        """
        Get results summary for all tests created by a teacher
        
        Args:
            teacher_id: ID of the teacher
            
        Returns:
            Dictionary with summary statistics
        """
        # Get all tests by teacher
        tests = Test.query.filter_by(created_by=teacher_id).all()
        test_ids = [t.id for t in tests]
        
        if not test_ids:
            return {
                'total_tests': 0,
                'total_attempts': 0,
                'total_students': 0,
                'average_score': 0
            }
        
        # Get all results for these tests
        results = Result.query.filter(Result.test_id.in_(test_ids)).all()
        
        # Get unique students
        unique_students = set(r.student_id for r in results)
        
        total_attempts = len(results)
        average_score = sum(r.percentage for r in results) / total_attempts if total_attempts > 0 else 0
        
        return {
            'total_tests': len(tests),
            'total_attempts': total_attempts,
            'total_students': len(unique_students),
            'average_score': round(average_score, 2)
        }

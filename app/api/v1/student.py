"""
Student API endpoints - FIXED VERSION
Handles all student module functionality including test taking, timer management, and results
"""
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, session
from flask_login import login_required, current_user
from app.utils.decorators import student_required
from app.services.test_service import TestService
from app.services.question_service import QuestionService
from app.services.terms_service import TermsService
from app.services.result_service import ResultService
from app.models.assignment import Assignment
from app.models.result import Result
from app.models.test import Test
from app.models.user import User
from app.models.question import Question
from app.services.encryption_service import EncryptionService
from app.utils.exceptions import ValidationError, DatabaseError
from app.extensions.limiter import limiter
from app.extensions.database import db
from datetime import datetime, timedelta
import json

# Create blueprint
student_bp = Blueprint('student', __name__, url_prefix='/student')


# ==================== HELPER FUNCTION ====================

def normalize_to_date(dt_obj):
    """Convert datetime to date object if needed"""
    if isinstance(dt_obj, datetime):
        return dt_obj.date()
    return dt_obj


# ==================== WEB ROUTES ====================

@student_bp.route('/dashboard')
@login_required
@student_required
def dashboard():
    """Student dashboard - shows today's assigned tests"""
    try:
        # Get today's date (date object only, no time)
        today = datetime.now().date()
        
        # Get all assignments for student
        assignments = Assignment.query.filter_by(student_id=current_user.id).all()
        
        # Categorize tests
        todays_tests = []
        upcoming_tests = []
        past_tests = []
        
        for assignment in assignments:
            try:
                # Get test details
                test = Test.query.get(assignment.test_id)
                if not test:
                    continue
                
                # Skip inactive or unpublished tests
                if hasattr(test, 'is_active') and not test.is_active:
                    continue
                if hasattr(test, 'is_published') and not test.is_published:
                    continue
                
                # Get result if exists
                result = Result.query.filter_by(
                    student_id=current_user.id,
                    test_id=assignment.test_id
                ).first()
                
                # CRITICAL FIX: Always convert to date for comparison
                if assignment.assigned_date is None:
                    continue  # Skip if no assigned date
                
                # Handle both datetime and date objects
                if hasattr(assignment.assigned_date, 'date'):
                    # It's a datetime object, extract date
                    assignment_date = assignment.assigned_date.date()
                else:
                    # It's already a date object
                    assignment_date = assignment.assigned_date
                
                test_data = {
                    'id': test.id,
                    'name': test.name,
                    'subject': test.subject,
                    'duration': test.duration,
                    'assigned_date': assignment_date,
                    'status': assignment.status,
                    'result': result  # Include result data
                }
                
                # Categorize by date and completion status
                if result:
                    # Test completed - add to past tests with result
                    past_tests.append(test_data)
                elif assignment_date == today:
                    todays_tests.append(test_data)
                elif assignment_date > today:
                    upcoming_tests.append(test_data)
                else:
                    # Past date but not completed
                    past_tests.append(test_data)
                    
            except Exception as inner_e:
                # Skip this assignment if there's an error
                print(f"Error processing assignment {assignment.id}: {str(inner_e)}")
                continue
        
        # Sort tests
        upcoming_tests.sort(key=lambda x: x['assigned_date'])
        past_tests.sort(key=lambda x: x['assigned_date'], reverse=True)
        
        return render_template(
            'student/dashboard.html',
            todays_tests=todays_tests,
            upcoming_tests=upcoming_tests,
            past_tests=past_tests,
            today=today
        )
        
    except Exception as e:
        import traceback
        print("=== DASHBOARD ERROR ===")
        traceback.print_exc()
        print("======================")
        flash(f'Error loading dashboard: {str(e)}', 'danger')
        return render_template(
            'student/dashboard.html', 
            todays_tests=[], 
            upcoming_tests=[], 
            past_tests=[], 
            today=datetime.now().date()
        )


@student_bp.route('/tests/<int:test_id>/instructions')
@login_required
@student_required
def test_instructions(test_id):
    """Show test instructions and terms & conditions"""
    try:
        # Verify student has access to this test
        assignment = Assignment.query.filter_by(
            student_id=current_user.id,
            test_id=test_id
        ).first()
        
        if not assignment:
            flash('Test not found or not assigned to you', 'danger')
            return redirect(url_for('student.dashboard'))
        
        # Check if test is available today
        today = datetime.now().date()
        assignment_date = normalize_to_date(assignment.assigned_date)
        
        if assignment_date > today:
            flash(f'This test is scheduled for {assignment_date.strftime("%B %d, %Y")}. Please come back on that date.', 'warning')
            return redirect(url_for('student.dashboard'))
        
        # Check if test already completed
        result = Result.query.filter_by(
            student_id=current_user.id,
            test_id=test_id
        ).first()
        
        if result:
            flash('You have already completed this test', 'info')
            return redirect(url_for('student.test_result', test_id=test_id))
        
        # Get test details
        test = Test.query.get(test_id)
        if not test:
            flash('Test not found', 'danger')
            return redirect(url_for('student.dashboard'))
        
        # Get question count
        question_count = QuestionService.get_question_count(test_id)
        
        # Get terms & conditions
        terms = TermsService.get_terms_for_test(test_id, decrypt=True)
        
        return render_template(
            'student/test_instructions.html',
            test=test,
            question_count=question_count,
            terms=terms or []
        )
        
    except Exception as e:
        flash(f'Error loading instructions: {str(e)}', 'danger')
        return redirect(url_for('student.dashboard'))


@student_bp.route('/tests/<int:test_id>/start', methods=['POST'])
@login_required
@student_required
def start_test(test_id):
    """Start test - create session and redirect to first question"""
    try:
        # Verify access
        assignment = Assignment.query.filter_by(
            student_id=current_user.id,
            test_id=test_id
        ).first()
        
        if not assignment:
            return jsonify({'success': False, 'error': 'Test not assigned'}), 403
        
        # Check if available today
        today = datetime.now().date()
        assignment_date = normalize_to_date(assignment.assigned_date)
        
        if assignment_date > today:
            return jsonify({'success': False, 'error': 'Test not available yet'}), 403
        
        # Check if already completed
        result = Result.query.filter_by(
            student_id=current_user.id,
            test_id=test_id
        ).first()
        
        if result:
            return jsonify({'success': False, 'error': 'Test already completed'}), 400
        
        # Get test details
        test = Test.query.get(test_id)
        if not test:
            return jsonify({'success': False, 'error': 'Test not found'}), 404
        
        # Validate test has questions
        question_count = QuestionService.get_question_count(test_id)
        if question_count == 0:
            return jsonify({
                'success': False, 
                'error': f'Test "{test.name}" has no questions. Please contact your teacher.'
            }), 400
        
        # Get all question IDs and randomize order for this student
        import random
        questions = QuestionService.get_questions_for_test(test_id, decrypt=False)
        question_ids = [q.id for q in questions]
        random.shuffle(question_ids)  # Randomize order
        
        # Create test session in Flask session
        start_time = datetime.now()
        end_time = start_time + timedelta(minutes=test.duration)
        
        session[f'test_{test_id}_start_time'] = start_time.isoformat()
        session[f'test_{test_id}_end_time'] = end_time.isoformat()
        session[f'test_{test_id}_answers'] = {}  # Store answers
        session[f'test_{test_id}_current_question'] = 1
        session[f'test_{test_id}_question_order'] = question_ids  # Store randomized order
        session[f'test_{test_id}_fullscreen_violations'] = 0  # Track fullscreen exits
        
        # Mark assignment as in progress
        assignment.status = 'in_progress'
        assignment.started_at = start_time
        db.session.commit()
        
        return jsonify({
            'success': True,
            'test_id': test_id,
            'start_time': start_time.isoformat(),
            'end_time': end_time.isoformat(),
            'duration': test.duration,
            'question_count': question_count,
            'redirect_url': url_for('student.take_test', test_id=test_id, question_number=1)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@student_bp.route('/tests/<int:test_id>/question/<int:question_number>')
@login_required
@student_required
def take_test(test_id, question_number):
    """Display test-taking interface with one question"""
    try:
        # Verify test session exists
        start_time_str = session.get(f'test_{test_id}_start_time')
        if not start_time_str:
            flash('Test session not found. Please start the test again.', 'warning')
            return redirect(url_for('student.test_instructions', test_id=test_id))
        
        # Calculate remaining time
        start_time = datetime.fromisoformat(start_time_str)
        end_time_str = session.get(f'test_{test_id}_end_time')
        end_time = datetime.fromisoformat(end_time_str)
        
        now = datetime.now()
        
        # Check if time expired
        if now >= end_time:
            flash('Time expired! Test auto-submitted.', 'warning')
            return redirect(url_for('student.submit_test', test_id=test_id))
        
        remaining_seconds = int((end_time - now).total_seconds())
        
        # Get test details
        test = Test.query.get(test_id)
        if not test:
            flash('Test not found', 'danger')
            return redirect(url_for('student.dashboard'))
        
        # Get randomized question order from session
        question_order = session.get(f'test_{test_id}_question_order', [])
        if not question_order:
            flash('Test session expired. Please start the test again.', 'warning')
            return redirect(url_for('student.test_instructions', test_id=test_id))
        
        total_questions = len(question_order)
        
        # Validate question number
        if question_number < 1 or question_number > total_questions:
            flash(f'Invalid question number {question_number}. Valid range: 1-{total_questions}', 'danger')
            return redirect(url_for('student.take_test', test_id=test_id, question_number=1))
        
        # Get the actual question ID from randomized order
        question_id = question_order[question_number - 1]
        
        # Get the specific question
        question_obj = Question.query.get(question_id)
        if not question_obj:
            flash('Question not found', 'danger')
            return redirect(url_for('student.dashboard'))
        
        # Decrypt question
        current_question = QuestionService.decrypt_question(question_obj)
        
        # Get fullscreen violation count
        fullscreen_violations = session.get(f'test_{test_id}_fullscreen_violations', 0)
        
        # Get previously saved answer if exists
        saved_answers = session.get(f'test_{test_id}_answers', {})
        saved_answer = saved_answers.get(str(current_question['id']))
        
        return render_template(
            'student/take_test.html',
            test=test,
            question=current_question,
            question_number=question_number,
            total_questions=total_questions,
            remaining_seconds=remaining_seconds,
            saved_answer=saved_answer,
            fullscreen_violations=fullscreen_violations
        )
        
    except Exception as e:
        import traceback
        print("=== TAKE TEST ERROR ===")
        traceback.print_exc()
        print("======================")
        flash(f'Error loading question: {str(e)}', 'danger')
        return redirect(url_for('student.dashboard'))


@student_bp.route('/tests/<int:test_id>/fullscreen-violation', methods=['POST'])
@login_required
@student_required
def track_fullscreen_violation(test_id):
    """Track fullscreen exit and other security violations"""
    try:
        # Get violation type from request
        data = request.get_json() if request.is_json else {}
        violation_type = data.get('violation_type', 'Fullscreen exit')
        
        violations_key = f'test_{test_id}_fullscreen_violations'
        violations = session.get(violations_key, 0)
        violations += 1
        session[violations_key] = violations
        session.modified = True
        
        # Log violation for audit
        try:
            from app.models.audit_log import AuditLog
            AuditLog.log_action(
                user_id=current_user.id,
                action=f'TEST_SECURITY_VIOLATION_{violations}',
                details=f'Test ID: {test_id}, Violation: {violation_type}',
                ip_address=request.remote_addr,
                status='warning'
            )
        except Exception as log_error:
            # Don't fail the request if logging fails
            print(f"Failed to log violation: {log_error}")
        
        if violations >= 2:
            # Auto-submit test on second violation
            return jsonify({
                'success': True,
                'violations': violations,
                'auto_submit': True,
                'message': f'Test auto-submitted due to security violations: {violation_type}'
            }), 200
        else:
            # First violation - warning
            return jsonify({
                'success': True,
                'violations': violations,
                'auto_submit': False,
                'message': f'Warning: {violation_type}. Doing this again will auto-submit your test!'
            }), 200
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@student_bp.route('/tests/<int:test_id>/submit-answer', methods=['POST'])
@login_required
@student_required
@limiter.limit("100 per hour")
def submit_answer(test_id):
    """Submit answer for current question and move to next"""
    try:
        data = request.get_json() if request.is_json else request.form
        
        question_id = data.get('question_id')
        selected_answer = data.get('selected_answer')
        question_number = int(data.get('question_number', 0))
        
        if not question_id or not selected_answer:
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
        
        # Store answer in session
        answers_key = f'test_{test_id}_answers'
        answers = session.get(answers_key, {})
        answers[str(question_id)] = selected_answer
        session[answers_key] = answers
        session.modified = True  # Ensure session is saved
        
        # Update current question
        session[f'test_{test_id}_current_question'] = question_number + 1
        
        # Get total questions
        total_questions = QuestionService.get_question_count(test_id)
        
        # Check if this was the last question
        if question_number >= total_questions:
            return jsonify({
                'success': True,
                'last_question': True,
                'message': 'Last question answered',
                'redirect_url': url_for('student.submit_test_page', test_id=test_id)
            }), 200
        
        # Redirect to next question
        return jsonify({
            'success': True,
            'last_question': False,
            'next_question': question_number + 1,
            'redirect_url': url_for('student.take_test', test_id=test_id, question_number=question_number + 1)
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@student_bp.route('/tests/<int:test_id>/previous-question/<int:question_number>')
@login_required
@student_required
def go_to_previous_question(test_id, question_number):
    """Navigate to a previous question"""
    try:
        # Verify test session exists
        start_time_str = session.get(f'test_{test_id}_start_time')
        if not start_time_str:
            flash('Test session not found. Please start the test again.', 'warning')
            return redirect(url_for('student.test_instructions', test_id=test_id))
        
        # Validate question number (must be >= 1)
        if question_number < 1:
            return redirect(url_for('student.take_test', test_id=test_id, question_number=1))
        
        # Get test details
        test = Test.query.get(test_id)
        if not test:
            flash('Test not found', 'danger')
            return redirect(url_for('student.dashboard'))
        
        # Calculate remaining time
        start_time = datetime.fromisoformat(start_time_str)
        end_time_str = session.get(f'test_{test_id}_end_time')
        end_time = datetime.fromisoformat(end_time_str)
        
        now = datetime.now()
        
        # Check if time expired
        if now >= end_time:
            flash('Time expired! Test auto-submitted.', 'warning')
            return redirect(url_for('student.submit_test', test_id=test_id))
        
        remaining_seconds = int((end_time - now).total_seconds())
        
        # Get randomized question order from session
        question_order = session.get(f'test_{test_id}_question_order', [])
        if not question_order:
            flash('Test session expired. Please start the test again.', 'warning')
            return redirect(url_for('student.test_instructions', test_id=test_id))
        
        total_questions = len(question_order)
        
        # Validate question number
        if question_number > total_questions:
            return redirect(url_for('student.take_test', test_id=test_id, question_number=total_questions))
        
        # Update current question in session
        session[f'test_{test_id}_current_question'] = question_number
        session.modified = True
        
        # Redirect to the requested question
        return redirect(url_for('student.take_test', test_id=test_id, question_number=question_number))
        
    except Exception as e:
        flash(f'Error navigating to question: {str(e)}', 'danger')
        return redirect(url_for('student.dashboard'))


@student_bp.route('/tests/<int:test_id>/submit-page')
@login_required
@student_required
def submit_test_page(test_id):
    """Show final submit page"""
    try:
        test = Test.query.get(test_id)
        total_questions = QuestionService.get_question_count(test_id)
        answered_count = len(session.get(f'test_{test_id}_answers', {}))
        
        return render_template(
            'student/submit_test_page.html',
            test=test,
            total_questions=total_questions,
            answered_count=answered_count
        )
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        return redirect(url_for('student.dashboard'))


@student_bp.route('/tests/<int:test_id>/submit', methods=['POST', 'GET'])
@login_required
@student_required
def submit_test(test_id):
    """Submit entire test and calculate results"""
    try:
        # Get submitted answers from session (can be empty if auto-submitted)
        answers = session.get(f'test_{test_id}_answers', {})
        
        # Check if already submitted
        existing_result = Result.query.filter_by(
            student_id=current_user.id,
            test_id=test_id
        ).first()
        
        if existing_result:
            flash('Test already submitted', 'info')
            return redirect(url_for('student.test_result', test_id=test_id))
        
        # Get all questions with correct answers for grading
        questions = QuestionService.get_questions_for_test(test_id, decrypt=True, include_answers=True)
        
        # Calculate score
        total_questions = len(questions)
        correct_answers = 0
        incorrect_answers = 0
        unattempted = 0
        
        for question in questions:
            question_id_str = str(question['id'])
            submitted_answer = answers.get(question_id_str)
            
            if not submitted_answer:
                unattempted += 1
            elif submitted_answer == question['correct_answer']:
                correct_answers += 1
            else:
                incorrect_answers += 1
        
        # Calculate percentage
        percentage = (correct_answers / total_questions * 100) if total_questions > 0 else 0
        score = correct_answers  # Or calculate based on marks per question
        
        # Get test details
        test = Test.query.get(test_id)
        
        # Determine pass/fail
        pass_percentage = getattr(test, 'pass_percentage', 50.0)
        passed = percentage >= pass_percentage
        
        # Get time taken
        start_time_str = session.get(f'test_{test_id}_start_time')
        if start_time_str:
            start_time = datetime.fromisoformat(start_time_str)
            time_taken = int((datetime.now() - start_time).total_seconds())  # in seconds
        else:
            time_taken = test.duration * 60  # convert minutes to seconds
        
        # Create result record
        result = Result(
            student_id=current_user.id,
            test_id=test_id,
            total_questions=total_questions,
            correct_answers=correct_answers,
            unanswered=unattempted,
            pass_percentage=pass_percentage,
            time_taken=time_taken,
            completed_at=datetime.now()
        )
        
        db.session.add(result)
        
        # Update assignment status
        assignment = Assignment.query.filter_by(
            student_id=current_user.id,
            test_id=test_id
        ).first()
        
        if assignment:
            assignment.status = 'completed'
            assignment.completed_at = datetime.now()
            if assignment.started_at:
                assignment.time_spent = int((datetime.now() - assignment.started_at).total_seconds())
        
        db.session.commit()
        
        # Store result ID and answers in session for review
        session[f'test_{test_id}_result_id'] = result.id
        session[f'test_{test_id}_final_answers'] = answers
        
        # Clear test session data (but keep result and answers for review)
        session.pop(f'test_{test_id}_start_time', None)
        session.pop(f'test_{test_id}_end_time', None)
        session.pop(f'test_{test_id}_current_question', None)
        
        # Redirect to results page
        flash('Test submitted successfully!', 'success')
        return redirect(url_for('student.test_result', test_id=test_id))
        
    except Exception as e:
        db.session.rollback()
        import traceback
        traceback.print_exc()
        flash(f'Error submitting test: {str(e)}', 'danger')
        return redirect(url_for('student.dashboard'))


@student_bp.route('/tests/<int:test_id>/result')
@login_required
@student_required
def test_result(test_id):
    """Display immediate test results"""
    try:
        # Get result
        result = Result.query.filter_by(
            student_id=current_user.id,
            test_id=test_id
        ).first()
        
        if not result:
            flash('Result not found. Please complete the test first.', 'danger')
            return redirect(url_for('student.dashboard'))
        
        # Get test details
        test = Test.query.get(test_id)
        
        return render_template(
            'student/test_result.html',
            test=test,
            result=result
        )
        
    except Exception as e:
        flash(f'Error loading results: {str(e)}', 'danger')
        return redirect(url_for('student.dashboard'))


@student_bp.route('/tests/<int:test_id>/review')
@login_required
@student_required
def review_answers(test_id):
    """Review answers with correct answers and explanations"""
    try:
        # Get result
        result = Result.query.filter_by(
            student_id=current_user.id,
            test_id=test_id
        ).first()
        
        if not result:
            flash('Please complete the test first', 'warning')
            return redirect(url_for('student.dashboard'))
        
        # Get submitted answers
        submitted_answers = session.get(f'test_{test_id}_final_answers', {})
        if not submitted_answers:
            # Try to get from database if session expired
            submitted_answers = session.get(f'test_{test_id}_answers', {})
        
        # Get all questions with answers for review
        questions = QuestionService.get_questions_for_test(test_id, decrypt=True, include_answers=True)
        
        # Prepare review data
        review_data = []
        for idx, question in enumerate(questions, start=1):
            question_id_str = str(question['id'])
            submitted_answer = submitted_answers.get(question_id_str, 'Not answered')
            correct_answer = question.get('correct_answer', 'N/A')
            is_correct = submitted_answer == correct_answer
            
            review_data.append({
                'question_number': idx,
                'question_text': question['question_text'],
                'options': question['options'],
                'your_answer': submitted_answer,
                'correct_answer': correct_answer,
                'is_correct': is_correct,
                'explanation': question.get('explanation', 'No explanation provided')
            })
        
        # Get test details
        test = Test.query.get(test_id)
        
        return render_template(
            'student/review_answers.html',
            test=test,
            result=result,
            review_data=review_data
        )
        
    except Exception as e:
        flash(f'Error loading review: {str(e)}', 'danger')
        return redirect(url_for('student.dashboard'))


# ==================== API ENDPOINTS ====================

@student_bp.route('/api/dashboard')
@login_required
@student_required
def api_dashboard():
    """API endpoint for dashboard data"""
    try:
        today = datetime.now().date()
        
        # Get assignments
        assignments = Assignment.query.filter_by(student_id=current_user.id).all()
        
        todays_tests = []
        upcoming_tests = []
        past_tests = []
        
        for assignment in assignments:
            test = Test.query.get(assignment.test_id)
            if not test:
                continue
            
            # Skip inactive tests
            if hasattr(test, 'is_active') and not test.is_active:
                continue
            if hasattr(test, 'is_published') and not test.is_published:
                continue
            
            result = Result.query.filter_by(
                student_id=current_user.id,
                test_id=assignment.test_id
            ).first()
            
            assignment_date = normalize_to_date(assignment.assigned_date)
            
            test_data = {
                'id': test.id,
                'name': test.name,
                'subject': test.subject,
                'duration': test.duration,
                'assigned_date': assignment_date.isoformat(),
                'status': 'completed' if result else 'pending'
            }
            
            if assignment_date == today:
                todays_tests.append(test_data)
            elif assignment_date > today:
                upcoming_tests.append(test_data)
            else:
                past_tests.append(test_data)
        
        return jsonify({
            'success': True,
            'todays_tests': todays_tests,
            'upcoming_tests': upcoming_tests,
            'past_tests': past_tests
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@student_bp.route('/api/tests/<int:test_id>/time-remaining')
@login_required
@student_required
def api_time_remaining(test_id):
    """Get remaining time for test (server-side validation)"""
    try:
        end_time_str = session.get(f'test_{test_id}_end_time')
        if not end_time_str:
            return jsonify({'success': False, 'error': 'No active test session'}), 404
        
        end_time = datetime.fromisoformat(end_time_str)
        now = datetime.now()
        
        if now >= end_time:
            return jsonify({
                'success': True,
                'expired': True,
                'remaining_seconds': 0
            }), 200
        
        remaining_seconds = int((end_time - now).total_seconds())
        
        return jsonify({
            'success': True,
            'expired': False,
            'remaining_seconds': remaining_seconds
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
# """
# Teacher API endpoints
# Handles all teacher module functionality
# """
# from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, send_file
# from flask_login import login_required, current_user
# from werkzeug.utils import secure_filename
# from app.utils.decorators import teacher_required
# from app.services.test_service import TestService
# from app.services.question_service import QuestionService
# from app.services.file_parser_service import FileParserService
# from app.services.terms_service import TermsService
# from app.services.result_service import ResultService
# from app.services.excel_service import ExcelService
# from app.utils.exceptions import ValidationError, DatabaseError
# from app.extensions.limiter import limiter
# import os
# import tempfile

# # Create blueprint
# teacher_bp = Blueprint('teacher', __name__, url_prefix='/teacher')

# # Allowed file extensions
# ALLOWED_EXTENSIONS = {'docx', 'pptx'}
# MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


# def allowed_file(filename):
#     """Check if file extension is allowed"""
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# # ==================== WEB ROUTES ====================

# @teacher_bp.route('/dashboard')
# @login_required
# @teacher_required
# def dashboard():
#     """Teacher dashboard"""
#     try:
#         # Get teacher statistics
#         test_stats = TestService.get_test_statistics(current_user.id)
#         results_summary = ResultService.get_teacher_results_summary(current_user.id)
        
#         # Get recent tests
#         recent_tests = TestService.get_tests_by_teacher(current_user.id)[:5]
        
#         return render_template(
#             'teacher/dashboard.html',
#             test_stats=test_stats,
#             results_summary=results_summary,
#             recent_tests=recent_tests
#         )
#     except Exception as e:
#         flash(f'Error loading dashboard: {str(e)}', 'danger')
#         return render_template('teacher/dashboard.html', test_stats={}, results_summary={}, recent_tests=[])


# @teacher_bp.route('/tests')
# @login_required
# @teacher_required
# def manage_tests():
#     """Manage tests page"""
#     try:
#         tests = TestService.get_tests_by_teacher(current_user.id, include_inactive=True)
#         return render_template('teacher/manage_tests.html', tests=tests)
#     except Exception as e:
#         flash(f'Error loading tests: {str(e)}', 'danger')
#         return render_template('teacher/manage_tests.html', tests=[])


# @teacher_bp.route('/tests/create', methods=['GET', 'POST'])
# @login_required
# @teacher_required
# def create_test():
#     """Create new test"""
#     if request.method == 'POST':
#         try:
#             name = request.form.get('name')
#             subject = request.form.get('subject')
#             duration = request.form.get('duration', type=int)
#             description = request.form.get('description')
            
#             test = TestService.create_test(
#                 name=name,
#                 subject=subject,
#                 duration=duration,
#                 teacher_id=current_user.id,
#                 description=description
#             )
            
#             flash(f'Test "{name}" created successfully!', 'success')
#             return redirect(url_for('teacher.manage_tests'))
            
#         except (ValidationError, DatabaseError) as e:
#             flash(str(e), 'danger')
    
#     return render_template('teacher/manage_tests.html')


# @teacher_bp.route('/upload-questions', methods=['GET', 'POST'])
# @login_required
# @teacher_required
# def upload_questions():
#     """Upload questions page"""
#     if request.method == 'POST':
#         try:
#             test_id = request.form.get('test_id', type=int)
#             file_type = request.form.get('file_type')  # 'word' or 'powerpoint'
            
#             if 'file' not in request.files:
#                 flash('No file uploaded', 'danger')
#                 return redirect(request.url)
            
#             file = request.files['file']
            
#             if file.filename == '':
#                 flash('No file selected', 'danger')
#                 return redirect(request.url)
            
#             if not allowed_file(file.filename):
#                 flash('Invalid file type. Only .docx and .pptx files are allowed', 'danger')
#                 return redirect(request.url)
            
#             # Save file temporarily
#             filename = secure_filename(file.filename)
#             temp_dir = tempfile.mkdtemp()
#             temp_path = os.path.join(temp_dir, filename)
#             file.save(temp_path)
            
#             # Parse file
#             if file_type == 'word' or filename.endswith('.docx'):
#                 questions = FileParserService.parse_word_document(temp_path)
#             elif file_type == 'powerpoint' or filename.endswith('.pptx'):
#                 questions = FileParserService.parse_powerpoint(temp_path)
#             else:
#                 flash('Invalid file type', 'danger')
#                 os.remove(temp_path)
#                 os.rmdir(temp_dir)
#                 return redirect(request.url)
            
#             # Create questions in database
#             count = QuestionService.bulk_create_questions(test_id, questions)
            
#             # Clean up
#             os.remove(temp_path)
#             os.rmdir(temp_dir)
            
#             flash(f'{count} questions uploaded successfully!', 'success')
#             return redirect(url_for('teacher.manage_tests'))
            
#         except (ValidationError, DatabaseError) as e:
#             flash(str(e), 'danger')
#         except Exception as e:
#             flash(f'Error uploading questions: {str(e)}', 'danger')
    
#     # GET request - show form
#     tests = TestService.get_tests_by_teacher(current_user.id)
#     return render_template('teacher/upload_questions.html', tests=tests)


# @teacher_bp.route('/upload-terms', methods=['GET', 'POST'])
# @login_required
# @teacher_required
# def upload_terms():
#     """Upload terms & conditions"""
#     if request.method == 'POST':
#         try:
#             test_id = request.form.get('test_id', type=int)
#             file_type = request.form.get('file_type')
            
#             if 'file' not in request.files:
#                 flash('No file uploaded', 'danger')
#                 return redirect(request.url)
            
#             file = request.files['file']
            
#             if file.filename == '':
#                 flash('No file selected', 'danger')
#                 return redirect(request.url)
            
#             if not allowed_file(file.filename):
#                 flash('Invalid file type. Only .docx and .pptx files are allowed', 'danger')
#                 return redirect(request.url)
            
#             # Save file temporarily
#             filename = secure_filename(file.filename)
#             temp_dir = tempfile.mkdtemp()
#             temp_path = os.path.join(temp_dir, filename)
#             file.save(temp_path)
            
#             # Parse terms
#             terms = FileParserService.parse_terms_conditions(temp_path, file_type)
            
#             # Create or update terms
#             TermsService.create_or_update_terms(test_id, terms)
            
#             # Clean up
#             os.remove(temp_path)
#             os.rmdir(temp_dir)
            
#             flash(f'Terms & Conditions uploaded successfully! ({len(terms)} terms)', 'success')
#             return redirect(url_for('teacher.manage_tests'))
            
#         except (ValidationError, DatabaseError) as e:
#             flash(str(e), 'danger')
#         except Exception as e:
#             flash(f'Error uploading terms: {str(e)}', 'danger')
    
#     # GET request
#     tests = TestService.get_tests_by_teacher(current_user.id)
#     return render_template('teacher/upload_terms.html', tests=tests)


# @teacher_bp.route('/results')
# @login_required
# @teacher_required
# def view_results():
#     """View test results"""
#     test_id = request.args.get('test_id', type=int)
    
#     if not test_id:
#         tests = TestService.get_tests_by_teacher(current_user.id)
#         return render_template('teacher/view_results.html', tests=tests, results=None, statistics=None)
    
#     try:
#         # Verify test belongs to teacher
#         test = TestService.get_test_by_id(test_id, include_question_count=False)
#         if not test or test.created_by != current_user.id:
#             flash('Test not found or access denied', 'danger')
#             return redirect(url_for('teacher.view_results'))
        
#         # Get results and statistics
#         results = ResultService.get_results_for_test(test_id)
#         statistics = ResultService.get_result_statistics(test_id)
        
#         tests = TestService.get_tests_by_teacher(current_user.id)
        
#         return render_template(
#             'teacher/view_results.html',
#             tests=tests,
#             selected_test=test,
#             results=results,
#             statistics=statistics
#         )
        
#     except Exception as e:
#         flash(f'Error loading results: {str(e)}', 'danger')
#         tests = TestService.get_tests_by_teacher(current_user.id)
#         return render_template('teacher/view_results.html', tests=tests, results=None, statistics=None)


# @teacher_bp.route('/export-results')
# @login_required
# @teacher_required
# def export_results():
#     """Export results page"""
#     tests = TestService.get_tests_by_teacher(current_user.id)
#     return render_template('teacher/export_results.html', tests=tests)


# @teacher_bp.route('/tests/<int:test_id>/delete', methods=['POST'])
# @login_required
# @teacher_required
# def delete_test(test_id):
#     """Delete a test"""
#     try:
#         # Verify ownership
#         test = TestService.get_test_by_id(test_id, include_question_count=False)
#         if not test or test.created_by != current_user.id:
#             flash('Test not found or access denied', 'danger')
#             return redirect(url_for('teacher.manage_tests'))
        
#         TestService.delete_test(test_id)
#         flash('Test deleted successfully!', 'success')
        
#     except (ValidationError, DatabaseError) as e:
#         flash(str(e), 'danger')
    
#     return redirect(url_for('teacher.manage_tests'))


# # ==================== API ENDPOINTS ====================

# @teacher_bp.route('/api/dashboard')
# @login_required
# @teacher_required
# def api_dashboard():
#     """API endpoint for dashboard statistics"""
#     try:
#         test_stats = TestService.get_test_statistics(current_user.id)
#         results_summary = ResultService.get_teacher_results_summary(current_user.id)
        
#         return jsonify({
#             'success': True,
#             'statistics': {
#                 'tests': test_stats,
#                 'results': results_summary
#             }
#         }), 200
        
#     except Exception as e:
#         return jsonify({
#             'success': False,
#             'error': str(e)
#         }), 500


# @teacher_bp.route('/api/tests', methods=['GET', 'POST'])
# @login_required
# @teacher_required
# def api_tests():
#     """List or create tests"""
#     if request.method == 'GET':
#         try:
#             tests = TestService.get_tests_by_teacher(current_user.id)
#             return jsonify({
#                 'success': True,
#                 'tests': tests
#             }), 200
            
#         except Exception as e:
#             return jsonify({
#                 'success': False,
#                 'error': str(e)
#             }), 500
    
#     elif request.method == 'POST':
#         try:
#             data = request.get_json()
            
#             test = TestService.create_test(
#                 name=data.get('name'),
#                 subject=data.get('subject'),
#                 duration=data.get('duration'),
#                 teacher_id=current_user.id,
#                 description=data.get('description')
#             )
            
#             return jsonify({
#                 'success': True,
#                 'message': 'Test created successfully',
#                 'test': test.to_dict()
#             }), 201
            
#         except (ValidationError, DatabaseError) as e:
#             return jsonify({
#                 'success': False,
#                 'error': str(e)
#             }), 400


# @teacher_bp.route('/api/tests/<int:test_id>', methods=['GET', 'PUT', 'DELETE'])
# @login_required
# @teacher_required
# def api_test_detail(test_id):
#     """Get, update, or delete a test"""
#     # Verify ownership
#     test = TestService.get_test_by_id(test_id, include_question_count=False)
#     if not test or test.created_by != current_user.id:
#         return jsonify({
#             'success': False,
#             'error': 'Test not found or access denied'
#         }), 404
    
#     if request.method == 'GET':
#         try:
#             test_data = TestService.get_test_by_id(test_id, include_question_count=True)
#             return jsonify({
#                 'success': True,
#                 'test': test_data
#             }), 200
            
#         except Exception as e:
#             return jsonify({
#                 'success': False,
#                 'error': str(e)
#             }), 500
    
#     elif request.method == 'PUT':
#         try:
#             data = request.get_json()
#             updated_test = TestService.update_test(test_id, **data)
            
#             return jsonify({
#                 'success': True,
#                 'message': 'Test updated successfully',
#                 'test': updated_test.to_dict()
#             }), 200
            
#         except (ValidationError, DatabaseError) as e:
#             return jsonify({
#                 'success': False,
#                 'error': str(e)
#             }), 400
    
#     elif request.method == 'DELETE':
#         try:
#             TestService.delete_test(test_id)
            
#             return jsonify({
#                 'success': True,
#                 'message': 'Test deleted successfully'
#             }), 200
            
#         except (ValidationError, DatabaseError) as e:
#             return jsonify({
#                 'success': False,
#                 'error': str(e)
#             }), 400


# @teacher_bp.route('/api/tests/<int:test_id>/questions/upload', methods=['POST'])
# @login_required
# @teacher_required
# @limiter.limit("10 per hour")
# def api_upload_questions(test_id):
#     """Upload questions via API"""
#     try:
#         # Verify ownership
#         test = TestService.get_test_by_id(test_id, include_question_count=False)
#         if not test or test.created_by != current_user.id:
#             return jsonify({
#                 'success': False,
#                 'error': 'Test not found or access denied'
#             }), 404
        
#         if 'file' not in request.files:
#             return jsonify({
#                 'success': False,
#                 'error': 'No file uploaded'
#             }), 400
        
#         file = request.files['file']
        
#         if file.filename == '' or not allowed_file(file.filename):
#             return jsonify({
#                 'success': False,
#                 'error': 'Invalid file'
#             }), 400
        
#         # Save temporarily
#         filename = secure_filename(file.filename)
#         temp_dir = tempfile.mkdtemp()
#         temp_path = os.path.join(temp_dir, filename)
#         file.save(temp_path)
        
#         # Parse
#         if filename.endswith('.docx'):
#             questions = FileParserService.parse_word_document(temp_path)
#         else:
#             questions = FileParserService.parse_powerpoint(temp_path)
        
#         # Create questions
#         count = QuestionService.bulk_create_questions(test_id, questions)
        
#         # Clean up
#         os.remove(temp_path)
#         os.rmdir(temp_dir)
        
#         return jsonify({
#             'success': True,
#             'message': f'{count} questions uploaded successfully',
#             'questions_count': count
#         }), 201
        
#     except (ValidationError, DatabaseError) as e:
#         return jsonify({
#             'success': False,
#             'error': str(e)
#         }), 400
#     except Exception as e:
#         return jsonify({
#             'success': False,
#             'error': f'Upload failed: {str(e)}'
#         }), 500


# @teacher_bp.route('/api/tests/<int:test_id>/questions')
# @login_required
# @teacher_required
# def api_get_questions(test_id):
#     """Get questions for a test"""
#     try:
#         # Verify ownership
#         test = TestService.get_test_by_id(test_id, include_question_count=False)
#         if not test or test.created_by != current_user.id:
#             return jsonify({
#                 'success': False,
#                 'error': 'Test not found or access denied'
#             }), 404
        
#         decrypt = request.args.get('decrypt', 'false').lower() == 'true'
#         questions = QuestionService.get_questions_for_test(test_id, decrypt=decrypt)
        
#         return jsonify({
#             'success': True,
#             'questions': questions if decrypt else [q.to_dict() for q in questions]
#         }), 200
        
#     except Exception as e:
#         return jsonify({
#             'success': False,
#             'error': str(e)
#         }), 500


# @teacher_bp.route('/api/tests/<int:test_id>/terms', methods=['GET', 'POST'])
# @login_required
# @teacher_required
# def api_terms(test_id):
#     """Get or create terms & conditions"""
#     # Verify ownership
#     test = TestService.get_test_by_id(test_id, include_question_count=False)
#     if not test or test.created_by != current_user.id:
#         return jsonify({
#             'success': False,
#             'error': 'Test not found or access denied'
#         }), 404
    
#     if request.method == 'GET':
#         try:
#             terms = TermsService.get_terms_for_test(test_id, decrypt=True)
            
#             return jsonify({
#                 'success': True,
#                 'terms': terms if terms else []
#             }), 200
            
#         except Exception as e:
#             return jsonify({
#                 'success': False,
#                 'error': str(e)
#             }), 500
    
#     elif request.method == 'POST':
#         try:
#             data = request.get_json()
#             terms_list = data.get('terms', [])
            
#             TermsService.create_or_update_terms(test_id, terms_list)
            
#             return jsonify({
#                 'success': True,
#                 'message': 'Terms & Conditions saved successfully'
#             }), 201
            
#         except (ValidationError, DatabaseError) as e:
#             return jsonify({
#                 'success': False,
#                 'error': str(e)
#             }), 400


# @teacher_bp.route('/api/tests/<int:test_id>/results')
# @login_required
# @teacher_required
# def api_get_results(test_id):
#     """Get results for a test"""
#     try:
#         # Verify ownership
#         test = TestService.get_test_by_id(test_id, include_question_count=False)
#         if not test or test.created_by != current_user.id:
#             return jsonify({
#                 'success': False,
#                 'error': 'Test not found or access denied'
#             }), 404
        
#         results = ResultService.get_results_for_test(test_id)
#         statistics = ResultService.get_result_statistics(test_id)
        
#         return jsonify({
#             'success': True,
#             'results': results,
#             'statistics': statistics
#         }), 200
        
#     except Exception as e:
#         return jsonify({
#             'success': False,
#             'error': str(e)
#         }), 500


# @teacher_bp.route('/api/tests/<int:test_id>/results/export')
# @login_required
# @teacher_required
# @limiter.limit("5 per hour")
# def api_export_results(test_id):
#     """Export results to encrypted Excel"""
#     try:
#         # Verify ownership
#         test = TestService.get_test_by_id(test_id, include_question_count=False)
#         if not test or test.created_by != current_user.id:
#             return jsonify({
#                 'success': False,
#                 'error': 'Test not found or access denied'
#             }), 404
        
#         # Get results
#         results = ResultService.get_results_for_test(test_id)
        
#         if not results:
#             return jsonify({
#                 'success': False,
#                 'error': 'No results to export'
#             }), 400
        
#         # Generate encrypted Excel
#         encrypted_path = ExcelService.generate_results_excel(test_id, test.name, results)
        
#         # Decrypt for download
#         decrypted_path = ExcelService.decrypt_and_prepare_download(encrypted_path)
        
#         # Send file
#         response = send_file(
#             decrypted_path,
#             as_attachment=True,
#             download_name=f'results_test_{test_id}.xlsx',
#             mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
#         )
        
#         # Schedule cleanup (file will be deleted after send)
#         @response.call_on_close
#         def cleanup():
#             ExcelService.cleanup_temp_file(decrypted_path)
        
#         return response
        
#     except (ValidationError, DatabaseError) as e:
#         return jsonify({
#             'success': False,
#             'error': str(e)
#         }), 400
#     except Exception as e:
#         return jsonify({
#             'success': False,
#             'error': f'Export failed: {str(e)}'
#         }), 500


# @teacher_bp.route('/api/tests/<int:test_id>/publish', methods=['POST'])
# @login_required
# @teacher_required
# def api_publish_test(test_id):
#     """Publish a test"""
#     try:
#         # Verify ownership
#         test = TestService.get_test_by_id(test_id, include_question_count=False)
#         if not test or test.created_by != current_user.id:
#             return jsonify({
#                 'success': False,
#                 'error': 'Test not found or access denied'
#             }), 404
        
#         TestService.publish_test(test_id)
        
#         return jsonify({
#             'success': True,
#             'message': 'Test published successfully'
#         }), 200
        
#     except (ValidationError, DatabaseError) as e:
#         return jsonify({
#             'success': False,
#             'error': str(e)
#         }), 400

"""
Teacher API endpoints
Handles all teacher module functionality
"""
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, send_file
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app.utils.decorators import teacher_required
from app.services.test_service import TestService
from app.services.question_service import QuestionService
from app.services.file_parser_service import FileParserService
from app.services.terms_service import TermsService
from app.services.result_service import ResultService
from app.services.excel_service import ExcelService
from app.utils.exceptions import ValidationError, DatabaseError
from app.extensions.limiter import limiter
import os
import tempfile

# Create blueprint
teacher_bp = Blueprint('teacher', __name__, url_prefix='/teacher')

# Allowed file extensions
ALLOWED_EXTENSIONS = {'docx', 'pptx'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ==================== WEB ROUTES ====================

@teacher_bp.route('/dashboard')
@login_required
@teacher_required
def dashboard():
    """Teacher dashboard"""
    try:
        # Get teacher statistics
        test_stats = TestService.get_test_statistics(current_user.id)
        results_summary = ResultService.get_teacher_results_summary(current_user.id)
        
        # Get recent tests
        recent_tests = TestService.get_tests_by_teacher(current_user.id)[:5]
        
        return render_template(
            'teacher/dashboard.html',
            test_stats=test_stats,
            results_summary=results_summary,
            recent_tests=recent_tests
        )
    except Exception as e:
        flash(f'Error loading dashboard: {str(e)}', 'danger')
        return render_template('teacher/dashboard.html', test_stats={}, results_summary={}, recent_tests=[])


@teacher_bp.route('/tests')
@login_required
@teacher_required
def manage_tests():
    """Manage tests page"""
    try:
        tests = TestService.get_tests_by_teacher(current_user.id, include_inactive=True)
        return render_template('teacher/manage_tests.html', tests=tests)
    except Exception as e:
        flash(f'Error loading tests: {str(e)}', 'danger')
        return render_template('teacher/manage_tests.html', tests=[])


@teacher_bp.route('/tests/create', methods=['GET', 'POST'])
@login_required
@teacher_required
def create_test():
    """Create new test"""
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            subject = request.form.get('subject')
            duration = request.form.get('duration', type=int)
            description = request.form.get('description')
            
            test = TestService.create_test(
                name=name,
                subject=subject,
                duration=duration,
                teacher_id=current_user.id,
                description=description
            )
            
            flash(f'Test "{name}" created successfully!', 'success')
            return redirect(url_for('teacher.manage_tests'))
            
        except (ValidationError, DatabaseError) as e:
            flash(str(e), 'danger')
    
    return render_template('teacher/manage_tests.html')


@teacher_bp.route('/upload-questions', methods=['GET', 'POST'])
@login_required
@teacher_required
def upload_questions():
    """Upload questions page"""
    if request.method == 'POST':
        try:
            # Get form data
            test_id = request.form.get('test_id', type=int)
            file_type = request.form.get('file_type')  # 'word' or 'powerpoint'
            
            # Validate test_id
            if not test_id:
                flash('Please select a test', 'danger')
                return redirect(request.url)
            
            # Verify test exists and belongs to current teacher
            test = TestService.get_test_by_id(test_id, include_question_count=False)
            if not test:
                flash('Invalid test selected', 'danger')
                return redirect(request.url)
            
            if test.created_by != current_user.id:
                flash('You do not have permission to add questions to this test', 'danger')
                return redirect(request.url)
            
            # Check if file was uploaded
            if 'file' not in request.files:
                flash('No file uploaded', 'danger')
                return redirect(request.url)
            
            file = request.files['file']
            
            if file.filename == '':
                flash('No file selected', 'danger')
                return redirect(request.url)
            
            if not allowed_file(file.filename):
                flash('Invalid file type. Only .docx and .pptx files are allowed', 'danger')
                return redirect(request.url)
            
            # Check file size
            file.seek(0, os.SEEK_END)
            file_size = file.tell()
            file.seek(0)
            
            if file_size > MAX_FILE_SIZE:
                flash('File size exceeds 10 MB limit', 'danger')
                return redirect(request.url)
            
            if file_size == 0:
                flash('Uploaded file is empty', 'danger')
                return redirect(request.url)
            
            # Save file temporarily
            filename = secure_filename(file.filename)
            temp_dir = tempfile.mkdtemp()
            temp_path = os.path.join(temp_dir, filename)
            
            try:
                file.save(temp_path)
                
                # Parse file based on type
                questions = []
                
                if file_type == 'word' or filename.endswith('.docx'):
                    questions = FileParserService.parse_word_document(temp_path)
                elif file_type == 'powerpoint' or filename.endswith('.pptx'):
                    questions = FileParserService.parse_powerpoint(temp_path)
                else:
                    flash('Invalid file type selected', 'danger')
                    raise ValueError('Invalid file type')
                
                # Check if questions were parsed
                if not questions:
                    flash('No valid questions found in the file. Please check the file format.', 'warning')
                    return redirect(request.url)
                
                # Get current question count before upload
                from app.services.question_service import QuestionService
                existing_count = QuestionService.get_question_count(test_id)
                
                # Bulk create questions in database
                count = QuestionService.bulk_create_questions(test_id, questions)
                
                if count > 0:
                    new_total = existing_count + count
                    if existing_count > 0:
                        flash(f'✅ Successfully added {count} new questions to test "{test.name}"! Total questions: {new_total}', 'success')
                    else:
                        flash(f'✅ Successfully uploaded {count} questions to test "{test.name}"!', 'success')
                    return redirect(url_for('teacher.manage_tests'))
                else:
                    flash('⚠️ No questions were added. Please check the file format.', 'warning')
                    return redirect(request.url)
                
            except ValidationError as ve:
                flash(f'Validation error: {str(ve)}', 'danger')
                return redirect(request.url)
                
            except DatabaseError as de:
                flash(f'Database error: {str(de)}', 'danger')
                return redirect(request.url)
                
            except Exception as e:
                flash(f'Error processing file: {str(e)}', 'danger')
                return redirect(request.url)
                
            finally:
                # Clean up temporary files
                try:
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
                    if os.path.exists(temp_dir):
                        os.rmdir(temp_dir)
                except Exception as cleanup_error:
                    print(f"Cleanup error: {cleanup_error}")
            
        except Exception as e:
            flash(f'Error uploading questions: {str(e)}', 'danger')
            return redirect(request.url)
    
    # GET request - show form
    try:
        tests = TestService.get_tests_by_teacher(current_user.id)
        return render_template('teacher/upload_questions.html', tests=tests)
    except Exception as e:
        flash(f'Error loading page: {str(e)}', 'danger')
        return render_template('teacher/upload_questions.html', tests=[])


@teacher_bp.route('/upload-terms', methods=['GET', 'POST'])
@login_required
@teacher_required
def upload_terms():
    """Upload terms & conditions"""
    if request.method == 'POST':
        try:
            test_id = request.form.get('test_id', type=int)
            file_type = request.form.get('file_type')
            
            if not test_id:
                flash('Please select a test', 'danger')
                return redirect(request.url)
            
            # Verify test ownership
            test = TestService.get_test_by_id(test_id, include_question_count=False)
            if not test or test.created_by != current_user.id:
                flash('Test not found or access denied', 'danger')
                return redirect(request.url)
            
            if 'file' not in request.files:
                flash('No file uploaded', 'danger')
                return redirect(request.url)
            
            file = request.files['file']
            
            if file.filename == '':
                flash('No file selected', 'danger')
                return redirect(request.url)
            
            if not allowed_file(file.filename):
                flash('Invalid file type. Only .docx and .pptx files are allowed', 'danger')
                return redirect(request.url)
            
            # Save file temporarily
            filename = secure_filename(file.filename)
            temp_dir = tempfile.mkdtemp()
            temp_path = os.path.join(temp_dir, filename)
            
            try:
                file.save(temp_path)
                
                # Parse terms
                terms = FileParserService.parse_terms_conditions(temp_path, file_type)
                
                if not terms:
                    flash('No terms found in the file', 'warning')
                    return redirect(request.url)
                
                # Create or update terms
                TermsService.create_or_update_terms(test_id, terms)
                
                flash(f'Terms & Conditions uploaded successfully! ({len(terms)} terms)', 'success')
                return redirect(url_for('teacher.manage_tests'))
                
            finally:
                # Clean up
                try:
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
                    if os.path.exists(temp_dir):
                        os.rmdir(temp_dir)
                except Exception as cleanup_error:
                    print(f"Cleanup error: {cleanup_error}")
            
        except (ValidationError, DatabaseError) as e:
            flash(str(e), 'danger')
        except Exception as e:
            flash(f'Error uploading terms: {str(e)}', 'danger')
    
    # GET request
    tests = TestService.get_tests_by_teacher(current_user.id)
    return render_template('teacher/upload_terms.html', tests=tests)


@teacher_bp.route('/results')
@login_required
@teacher_required
def view_results():
    """View test results"""
    test_id = request.args.get('test_id', type=int)
    
    # Get all tests for dropdown
    tests = TestService.get_tests_by_teacher(current_user.id)
    
    if not test_id:
        return render_template('teacher/view_results.html', 
                             tests=tests, 
                             selected_test=None,
                             results=None, 
                             statistics=None)
    
    try:
        # Verify test belongs to teacher
        test = TestService.get_test_by_id(test_id, include_question_count=False)
        if not test or test.created_by != current_user.id:
            flash('Test not found or access denied', 'danger')
            return redirect(url_for('teacher.view_results'))
        
        # Get results and statistics (even if empty)
        results = ResultService.get_results_for_test(test_id)
        statistics = ResultService.get_result_statistics(test_id)
        
        # Always pass selected_test so template knows a test was selected
        return render_template(
            'teacher/view_results.html',
            tests=tests,
            selected_test=test,
            results=results if results else [],  # Pass empty list instead of None
            statistics=statistics if statistics else None
        )
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        flash(f'Error loading results: {str(e)}', 'danger')
        return render_template('teacher/view_results.html', 
                             tests=tests, 
                             selected_test=None,
                             results=None, 
                             statistics=None)


@teacher_bp.route('/export-results')
@login_required
@teacher_required
def export_results():
    """Export results page"""
    tests = TestService.get_tests_by_teacher(current_user.id)
    return render_template('teacher/export_results.html', tests=tests)


@teacher_bp.route('/tests/<int:test_id>/delete', methods=['POST'])
@login_required
@teacher_required
def delete_test(test_id):
    """Delete a test"""
    try:
        # Verify ownership
        test = TestService.get_test_by_id(test_id, include_question_count=False)
        if not test or test.created_by != current_user.id:
            flash('Test not found or access denied', 'danger')
            return redirect(url_for('teacher.manage_tests'))
        
        TestService.delete_test(test_id)
        flash('Test deleted successfully!', 'success')
        
    except (ValidationError, DatabaseError) as e:
        flash(str(e), 'danger')
    
    return redirect(url_for('teacher.manage_tests'))


# ==================== API ENDPOINTS ====================

@teacher_bp.route('/api/dashboard')
@login_required
@teacher_required
def api_dashboard():
    """API endpoint for dashboard statistics"""
    try:
        test_stats = TestService.get_test_statistics(current_user.id)
        results_summary = ResultService.get_teacher_results_summary(current_user.id)
        
        return jsonify({
            'success': True,
            'statistics': {
                'tests': test_stats,
                'results': results_summary
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@teacher_bp.route('/api/tests', methods=['GET', 'POST'])
@login_required
@teacher_required
def api_tests():
    """List or create tests"""
    if request.method == 'GET':
        try:
            tests = TestService.get_tests_by_teacher(current_user.id)
            return jsonify({
                'success': True,
                'tests': tests
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            
            test = TestService.create_test(
                name=data.get('name'),
                subject=data.get('subject'),
                duration=data.get('duration'),
                teacher_id=current_user.id,
                description=data.get('description')
            )
            
            return jsonify({
                'success': True,
                'message': 'Test created successfully',
                'test': test.to_dict()
            }), 201
            
        except (ValidationError, DatabaseError) as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 400


@teacher_bp.route('/api/tests/<int:test_id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
@teacher_required
def api_test_detail(test_id):
    """Get, update, or delete a test"""
    # Verify ownership
    test = TestService.get_test_by_id(test_id, include_question_count=False)
    if not test or test.created_by != current_user.id:
        return jsonify({
            'success': False,
            'error': 'Test not found or access denied'
        }), 404
    
    if request.method == 'GET':
        try:
            test_data = TestService.get_test_by_id(test_id, include_question_count=True)
            return jsonify({
                'success': True,
                'test': test_data
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    elif request.method == 'PUT':
        try:
            data = request.get_json()
            updated_test = TestService.update_test(test_id, **data)
            
            return jsonify({
                'success': True,
                'message': 'Test updated successfully',
                'test': updated_test.to_dict()
            }), 200
            
        except (ValidationError, DatabaseError) as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 400
    
    elif request.method == 'DELETE':
        try:
            TestService.delete_test(test_id)
            
            return jsonify({
                'success': True,
                'message': 'Test deleted successfully'
            }), 200
            
        except (ValidationError, DatabaseError) as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 400


@teacher_bp.route('/api/tests/<int:test_id>/questions/upload', methods=['POST'])
@login_required
@teacher_required
@limiter.limit("10 per hour")
def api_upload_questions(test_id):
    """Upload questions via API"""
    try:
        # Verify ownership
        test = TestService.get_test_by_id(test_id, include_question_count=False)
        if not test or test.created_by != current_user.id:
            return jsonify({
                'success': False,
                'error': 'Test not found or access denied'
            }), 404
        
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file uploaded'
            }), 400
        
        file = request.files['file']
        
        if file.filename == '' or not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': 'Invalid file'
            }), 400
        
        # Save temporarily
        filename = secure_filename(file.filename)
        temp_dir = tempfile.mkdtemp()
        temp_path = os.path.join(temp_dir, filename)
        
        try:
            file.save(temp_path)
            
            # Parse
            if filename.endswith('.docx'):
                questions = FileParserService.parse_word_document(temp_path)
            else:
                questions = FileParserService.parse_powerpoint(temp_path)
            
            # Create questions
            count = QuestionService.bulk_create_questions(test_id, questions)
            
            return jsonify({
                'success': True,
                'message': f'{count} questions uploaded successfully',
                'questions_count': count
            }), 201
            
        finally:
            # Clean up
            try:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                if os.path.exists(temp_dir):
                    os.rmdir(temp_dir)
            except Exception as cleanup_error:
                print(f"Cleanup error: {cleanup_error}")
        
    except (ValidationError, DatabaseError) as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Upload failed: {str(e)}'
        }), 500


@teacher_bp.route('/api/tests/<int:test_id>/questions')
@login_required
@teacher_required
def api_get_questions(test_id):
    """Get questions for a test"""
    try:
        # Verify ownership
        test = TestService.get_test_by_id(test_id, include_question_count=False)
        if not test or test.created_by != current_user.id:
            return jsonify({
                'success': False,
                'error': 'Test not found or access denied'
            }), 404
        
        decrypt = request.args.get('decrypt', 'false').lower() == 'true'
        questions = QuestionService.get_questions_for_test(test_id, decrypt=decrypt)
        
        return jsonify({
            'success': True,
            'questions': questions if decrypt else [q.to_dict() for q in questions]
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@teacher_bp.route('/api/tests/<int:test_id>/terms', methods=['GET', 'POST'])
@login_required
@teacher_required
def api_terms(test_id):
    """Get or create terms & conditions"""
    # Verify ownership
    test = TestService.get_test_by_id(test_id, include_question_count=False)
    if not test or test.created_by != current_user.id:
        return jsonify({
            'success': False,
            'error': 'Test not found or access denied'
        }), 404
    
    if request.method == 'GET':
        try:
            terms = TermsService.get_terms_for_test(test_id, decrypt=True)
            
            return jsonify({
                'success': True,
                'terms': terms if terms else []
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            terms_list = data.get('terms', [])
            
            TermsService.create_or_update_terms(test_id, terms_list)
            
            return jsonify({
                'success': True,
                'message': 'Terms & Conditions saved successfully'
            }), 201
            
        except (ValidationError, DatabaseError) as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 400


@teacher_bp.route('/api/tests/<int:test_id>/results')
@login_required
@teacher_required
def api_get_results(test_id):
    """Get results for a test"""
    try:
        # Verify ownership
        test = TestService.get_test_by_id(test_id, include_question_count=False)
        if not test or test.created_by != current_user.id:
            return jsonify({
                'success': False,
                'error': 'Test not found or access denied'
            }), 404
        
        results = ResultService.get_results_for_test(test_id)
        statistics = ResultService.get_result_statistics(test_id)
        
        return jsonify({
            'success': True,
            'results': results,
            'statistics': statistics
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@teacher_bp.route('/api/tests/<int:test_id>/results/export')
@login_required
@teacher_required
def api_export_results(test_id):
    """Export results to encrypted Excel"""
    try:
        # Verify ownership
        test = TestService.get_test_by_id(test_id, include_question_count=False)
        if not test or test.created_by != current_user.id:
            return jsonify({
                'success': False,
                'error': 'Test not found or access denied'
            }), 404
        
        # Get results
        results = ResultService.get_results_for_test(test_id)
        
        if not results:
            return jsonify({
                'success': False,
                'error': 'No results to export'
            }), 400
        
        # Generate Excel
        excel_path = ExcelService.generate_results_excel(test_id, test.name, results)
        
        # Send file directly (no decryption needed)
        response = send_file(
            excel_path,
            as_attachment=True,
            download_name=f'results_test_{test_id}.xlsx',
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        
        # Schedule cleanup (file will be deleted after send)
        @response.call_on_close
        def cleanup():
            ExcelService.cleanup_temp_file(excel_path)
        
        return response
        
    except (ValidationError, DatabaseError) as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Export failed: {str(e)}'
        }), 500


@teacher_bp.route('/api/tests/<int:test_id>/publish', methods=['POST'])
@login_required
@teacher_required
def api_publish_test(test_id):
    """Publish a test"""
    try:
        # Verify ownership
        test = TestService.get_test_by_id(test_id, include_question_count=False)
        if not test or test.created_by != current_user.id:
            return jsonify({
                'success': False,
                'error': 'Test not found or access denied'
            }), 404
        
        TestService.publish_test(test_id)
        
        return jsonify({
            'success': True,
            'message': 'Test published successfully'
        }), 200
        
    except (ValidationError, DatabaseError) as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

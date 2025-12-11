# """
# Admin API endpoints
# Handles all administrative functions
# """
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.utils.decorators import admin_required
from app.services.user_service import UserService
from app.models.user import User
from app.models.test import Test
from app.models.assignment import Assignment
from app.models.result import Result
from app.models.audit_log import AuditLog
from app.extensions.database import db
from app.utils.exceptions import ValidationError, DatabaseError
from datetime import datetime, timedelta

# # Create blueprint
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


# # ==================== WEB ROUTES ====================

# @admin_bp.route('/dashboard')
# @login_required
# @admin_required
# def dashboard():
#     """Admin dashboard"""
#     # Get statistics
#     user_stats = UserService.get_user_statistics()
    
#     # Get test count
#     total_tests = Test.query.count()
    
#     # Get assignment count
#     active_assignments = Assignment.query.filter_by(status='pending').count()
    
#     # Get recent activity (last 10 audit logs)
#     recent_activity = AuditLog.query.order_by(
#         AuditLog.timestamp.desc()
#     ).limit(10).all()
    
#     return render_template(
#         'admin/dashboard.html',
#         user_stats=user_stats,
#         total_tests=total_tests,
#         active_assignments=active_assignments,
#         recent_activity=recent_activity
#     )


@admin_bp.route('/users')
@login_required
@admin_required
def manage_users():
     """User management page"""
     page = request.args.get('page', 1, type=int)
     role = request.args.get('role')
     search = request.args.get('search')
    
     if search:
         users, total = UserService.search_users(search, role=role, page=page)
     else:
         users, total = UserService.get_all_users(role=role, page=page)
    
     # Calculate pagination
     pages = (total + 19) // 20  # Ceiling division
    
     return render_template(
         'admin/manage_users.html',
         users=users,
         total=total,
         page=page,
         pages=pages,
         current_role=role,
         search_query=search
     )


@admin_bp.route('/users/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_user():
     """Create user page"""
     if request.method == 'POST':
         username = request.form.get('username')
         email = request.form.get('email')
         password = request.form.get('password')
         role = request.form.get('role')
         full_name = request.form.get('full_name')
         student_id = request.form.get('student_id')
        
         try:
             user = UserService.create_user(
                 username=username,
                 email=email,
                 password=password,
                 role=role,
                 full_name=full_name,
                 student_id=student_id if role == 'student' else None
             )
            
             flash(f'User {username} created successfully!', 'success')
             return redirect(url_for('admin.manage_users'))
            
         except (ValidationError, DatabaseError) as e:
             flash(str(e), 'danger')
    
     return render_template('admin/create_user.html')


# @admin_bp.route('/users/<int:user_id>/delete', methods=['POST'])
# @login_required
# @admin_required
# def delete_user(user_id):
#     """Delete user"""
#     try:
#         UserService.delete_user(user_id, current_user.id)
#         flash('User deleted successfully!', 'success')
#     except (ValidationError, DatabaseError) as e:
#         flash(str(e), 'danger')
    
#     return redirect(url_for('admin.manage_users'))


# @admin_bp.route('/users/<int:user_id>/reset-password', methods=['POST'])
# @login_required
# @admin_required
# def reset_user_password(user_id):
#     """Reset user password"""
#     try:
#         new_password = UserService.reset_user_password(user_id)
#         flash(f'Password reset successfully! New password: {new_password}', 'success')
#     except DatabaseError as e:
#         flash(str(e), 'danger')
    
#     return redirect(url_for('admin.manage_users'))


# @admin_bp.route('/assign-tests', methods=['GET', 'POST'])
# @login_required
# @admin_required
# def assign_tests():
#     """Assign tests to students"""
#     if request.method == 'POST':
#         test_id = request.form.get('test_id', type=int)
#         student_ids = request.form.getlist('student_ids', type=int)
#         assigned_date = request.form.get('assigned_date')
        
#         try:
#             # Parse date
#             assign_date = datetime.strptime(assigned_date, '%Y-%m-%d')
            
#             # Validate date is not in the past
#             if assign_date.date() < datetime.utcnow().date():
#                 flash('Cannot assign test with past date!', 'danger')
#                 return redirect(url_for('admin.assign_tests'))
            
#             # Create assignments
#             created_count = 0
#             for student_id in student_ids:
#                 # Check if assignment already exists
#                 existing = Assignment.query.filter_by(
#                     student_id=student_id,
#                     test_id=test_id
#                 ).first()
                
#                 if not existing:
#                     assignment = Assignment(
#                         student_id=student_id,
#                         test_id=test_id,
#                         assigned_date=assign_date,
#                         assigned_by=current_user.id
#                     )
#                     db.session.add(assignment)
#                     created_count += 1
            
#             db.session.commit()
#             flash(f'Test assigned to {created_count} student(s) successfully!', 'success')
#             return redirect(url_for('admin.manage_test_dates'))
            
#         except Exception as e:
#             db.session.rollback()
#             flash(f'Error assigning test: {str(e)}', 'danger')
    
#     # GET request - show form
#     tests = Test.query.filter_by(is_active=True, is_published=True).all()
#     students = User.query.filter_by(role='student', is_active=True, is_deleted=False).all()
    
#     return render_template('admin/assign_tests.html', tests=tests, students=students)


# @admin_bp.route('/test-dates')
# @login_required
# @admin_required
# def manage_test_dates():
#     """Manage test assignment dates"""
#     page = request.args.get('page', 1, type=int)
#     test_id = request.args.get('test_id', type=int)
#     student_id = request.args.get('student_id', type=int)
    
#     query = Assignment.query
    
#     if test_id:
#         query = query.filter_by(test_id=test_id)
#     if student_id:
#         query = query.filter_by(student_id=student_id)
    
#     assignments = query.order_by(Assignment.assigned_date.desc()).paginate(
#         page=page, per_page=20, error_out=False
#     )
    
#     tests = Test.query.all()
#     students = User.query.filter_by(role='student').all()
    
#     return render_template(
#         'admin/manage_test_dates.html',
#         assignments=assignments.items,
#         page=page,
#         pages=assignments.pages,
#         tests=tests,
#         students=students
#     )


# @admin_bp.route('/assignments/<int:assignment_id>/update', methods=['POST'])
# @login_required
# @admin_required
# def update_assignment(assignment_id):
#     """Update assignment date"""
#     new_date = request.form.get('assigned_date')
    
#     try:
#         assignment = Assignment.query.get_or_404(assignment_id)
#         assignment.assigned_date = datetime.strptime(new_date, '%Y-%m-%d')
#         db.session.commit()
#         flash('Assignment date updated successfully!', 'success')
#     except Exception as e:
#         db.session.rollback()
#         flash(f'Error updating assignment: {str(e)}', 'danger')
    
#     return redirect(url_for('admin.manage_test_dates'))


# @admin_bp.route('/assignments/<int:assignment_id>/delete', methods=['POST'])
# @login_required
# @admin_required
# def delete_assignment(assignment_id):
#     """Delete assignment"""
#     try:
#         assignment = Assignment.query.get_or_404(assignment_id)
#         db.session.delete(assignment)
#         db.session.commit()
#         flash('Assignment removed successfully!', 'success')
#     except Exception as e:
#         db.session.rollback()
#         flash(f'Error removing assignment: {str(e)}', 'danger')
    
#     return redirect(url_for('admin.manage_test_dates'))


@admin_bp.route('/logs')
@login_required
@admin_required
def system_logs():
     """View system audit logs"""
     page = request.args.get('page', 1, type=int)
     user_id = request.args.get('user_id', type=int)
     action = request.args.get('action')
     date_from = request.args.get('date_from')
     date_to = request.args.get('date_to')
    
     query = AuditLog.query
    
     # Filters
     if user_id:
         query = query.filter_by(user_id=user_id)
     if action:
         query = query.filter_by(action=action)
     if date_from:
         date_from_dt = datetime.strptime(date_from, '%Y-%m-%d')
         query = query.filter(AuditLog.timestamp >= date_from_dt)
     if date_to:
         date_to_dt = datetime.strptime(date_to, '%Y-%m-%d') + timedelta(days=1)
         query = query.filter(AuditLog.timestamp < date_to_dt)
    
     logs = query.order_by(AuditLog.timestamp.desc()).paginate(
         page=page, per_page=50, error_out=False
     )
    
     # Get unique users and actions for filters
     users = User.query.all()
     actions = db.session.query(AuditLog.action).distinct().all()
     actions = [a[0] for a in actions]
    
     return render_template(
         'admin/system_logs.html',
         logs=logs.items,
         page=page,
         pages=logs.pages,
         users=users,
         actions=actions
     )


# # ==================== API ENDPOINTS ====================

# @admin_bp.route('/api/dashboard')
# @login_required
# @admin_required
# def api_dashboard():
#     """API endpoint for dashboard statistics"""
#     user_stats = UserService.get_user_statistics()
    
#     return jsonify({
#         'success': True,
#         'statistics': {
#             'users': user_stats,
#             'total_tests': Test.query.count(),
#             'active_assignments': Assignment.query.filter_by(status='pending').count(),
#             'completed_tests': Result.query.count()
#         }
#     }), 200


# @admin_bp.route('/api/users')
# @login_required
# @admin_required
# def api_get_users():
#     """API endpoint to list all users"""
#     role = request.args.get('role')
#     page = request.args.get('page', 1, type=int)
#     per_page = request.args.get('per_page', 20, type=int)
#     search = request.args.get('search')
    
#     if search:
#         users, total = UserService.search_users(search, role=role, page=page, per_page=per_page)
#     else:
#         users, total = UserService.get_all_users(role=role, page=page, per_page=per_page)
    
#     return jsonify({
#         'success': True,
#         'users': [u.to_dict() for u in users],
#         'total': total,
#         'page': page,
#         'per_page': per_page
#     }), 200


# @admin_bp.route('/api/users', methods=['POST'])
# @login_required
# @admin_required
# def api_create_user():
#     """API endpoint to create user"""
#     data = request.get_json()
    
#     try:
#         user = UserService.create_user(
#             username=data.get('username'),
#             email=data.get('email'),
#             password=data.get('password'),
#             role=data.get('role'),
#             full_name=data.get('full_name'),
#             student_id=data.get('student_id')
#         )
        
#         return jsonify({
#             'success': True,
#             'message': 'User created successfully',
#             'user': user.to_dict()
#         }), 201
        
#     except (ValidationError, DatabaseError) as e:
#         return jsonify({
#             'success': False,
#             'error': str(e)
#         }), 400


# @admin_bp.route('/api/users/<int:user_id>')
# @login_required
# @admin_required
# def api_get_user(user_id):
#     """API endpoint to get single user"""
#     user = UserService.get_user_by_id(user_id)
    
#     if not user:
#         return jsonify({
#             'success': False,
#             'error': 'User not found'
#         }), 404
    
#     return jsonify({
#         'success': True,
#         'user': user.to_dict(include_sensitive=True)
#     }), 200


# @admin_bp.route('/api/users/<int:user_id>', methods=['PUT'])
# @login_required
# @admin_required
# def api_update_user(user_id):
#     """API endpoint to update user"""
#     data = request.get_json()
    
#     try:
#         user = UserService.update_user(user_id, **data)
        
#         return jsonify({
#             'success': True,
#             'message': 'User updated successfully',
#             'user': user.to_dict()
#         }), 200
        
#     except (ValidationError, DatabaseError) as e:
#         return jsonify({
#             'success': False,
#             'error': str(e)
#         }), 400


# @admin_bp.route('/api/users/<int:user_id>', methods=['DELETE'])
# @login_required
# @admin_required
# def api_delete_user(user_id):
#     """API endpoint to delete user"""
#     try:
#         UserService.delete_user(user_id, current_user.id)
        
#         return jsonify({
#             'success': True,
#             'message': 'User deleted successfully'
#         }), 200
        
#     except (ValidationError, DatabaseError) as e:
#         return jsonify({
#             'success': False,
#             'error': str(e)
#         }), 400


# @admin_bp.route('/api/users/<int:user_id>/reset-password', methods=['POST'])
# @login_required
# @admin_required
# def api_reset_password(user_id):
#     """API endpoint to reset user password"""
#     try:
#         new_password = UserService.reset_user_password(user_id)
        
#         return jsonify({
#             'success': True,
#             'message': 'Password reset successfully',
#             'new_password': new_password
#         }), 200
        
#     except DatabaseError as e:
#         return jsonify({
#             'success': False,
#             'error': str(e)
#         }), 400


# @admin_bp.route('/api/tests')
# @login_required
# @admin_required
# def api_get_tests():
#     """API endpoint to list all tests"""
#     tests = Test.query.all()
    
#     return jsonify({
#         'success': True,
#         'tests': [t.to_dict() for t in tests]
#     }), 200


# @admin_bp.route('/api/assignments', methods=['POST'])
# @login_required
# @admin_required
# def api_create_assignment():
#     """API endpoint to create assignment"""
#     data = request.get_json()
    
#     try:
#         test_id = data.get('test_id')
#         student_ids = data.get('student_ids', [])
#         assigned_date = datetime.strptime(data.get('assigned_date'), '%Y-%m-%d')
        
#         assignments = []
#         for student_id in student_ids:
#             assignment = Assignment(
#                 student_id=student_id,
#                 test_id=test_id,
#                 assigned_date=assigned_date,
#                 assigned_by=current_user.id
#             )
#             db.session.add(assignment)
#             assignments.append(assignment)
        
#         db.session.commit()
        
#         return jsonify({
#             'success': True,
#             'message': f'{len(assignments)} assignment(s) created',
#             'assignments': [a.to_dict() for a in assignments]
#         }), 201
        
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({
#             'success': False,
#             'error': str(e)
#         }), 400


# @admin_bp.route('/api/assignments')
# @login_required
# @admin_required
# def api_get_assignments():
#     """API endpoint to list assignments"""
#     test_id = request.args.get('test_id', type=int)
#     student_id = request.args.get('student_id', type=int)
    
#     query = Assignment.query
    
#     if test_id:
#         query = query.filter_by(test_id=test_id)
#     if student_id:
#         query = query.filter_by(student_id=student_id)
    
#     assignments = query.all()
    
#     return jsonify({
#         'success': True,
#         'assignments': [a.to_dict() for a in assignments]
#     }), 200


# @admin_bp.route('/api/assignments/<int:assignment_id>', methods=['PUT'])
# @login_required
# @admin_required
# def api_update_assignment(assignment_id):
#     """API endpoint to update assignment"""
#     data = request.get_json()
    
#     try:
#         assignment = Assignment.query.get_or_404(assignment_id)
        
#         if 'assigned_date' in data:
#             assignment.assigned_date = datetime.strptime(data['assigned_date'], '%Y-%m-%d')
        
#         db.session.commit()
        
#         return jsonify({
#             'success': True,
#             'message': 'Assignment updated successfully',
#             'assignment': assignment.to_dict()
#         }), 200
        
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({
#             'success': False,
#             'error': str(e)
#         }), 400


# @admin_bp.route('/api/audit-logs')
# @login_required
# @admin_required
# def api_get_audit_logs():
#     """API endpoint to get audit logs"""
#     page = request.args.get('page', 1, type=int)
#     per_page = request.args.get('per_page', 50, type=int)
#     user_id = request.args.get('user_id', type=int)
#     action = request.args.get('action')
    
#     query = AuditLog.query
    
#     if user_id:
#         query = query.filter_by(user_id=user_id)
#     if action:
#         query = query.filter_by(action=action)
    
#     logs = query.order_by(AuditLog.timestamp.desc()).paginate(
#         page=page, per_page=per_page, error_out=False
#     )
    
#     return jsonify({
#         'success': True,
#         'logs': [log.to_dict() for log in logs.items],
#         'total': logs.total,
#         'page': page,
#         'per_page': per_page
#     }), 200


# # ==================== DASHBOARD CHART DATA ====================

# @admin_bp.route('/api/daily-users')
# @login_required
# @admin_required
# def api_daily_users():
#     """Return last 14 days data for active users, tests, and assignments."""
#     try:
#         days = 14
#         today = datetime.utcnow().date()
#         labels = []
#         users_arr, tests_arr, assigns_arr = [], [], []

#         for i in range(days - 1, -1, -1):
#             day = today - timedelta(days=i)
#             next_day = day + timedelta(days=1)
#             labels.append(f"{day.month}/{day.day}")

#             # active users: distinct user_id appearing in audit logs on that day
#             users_count = (db.session.query(AuditLog.user_id)
#                            .filter(AuditLog.timestamp >= datetime.combine(day, datetime.min.time()))
#                            .filter(AuditLog.timestamp < datetime.combine(next_day, datetime.min.time()))
#                            .distinct()
#                            .count())

#             # tests taken (results completed that day)
#             tests_count = (db.session.query(Result.id)
#                            .filter(Result.completed_at >= datetime.combine(day, datetime.min.time()))
#                            .filter(Result.completed_at < datetime.combine(next_day, datetime.min.time()))
#                            .count())

#             # assignments created that day
#             assigns_count = (db.session.query(Assignment.id)
#                              .filter(Assignment.assigned_date >= datetime.combine(day, datetime.min.time()))
#                              .filter(Assignment.assigned_date < datetime.combine(next_day, datetime.min.time()))
#                              .count())

#             users_arr.append(users_count)
#             tests_arr.append(tests_count)
#             assigns_arr.append(assigns_count)

#         return jsonify({
#             'labels': labels,
#             'users': users_arr,
#             'tests': tests_arr,
#             'assignments': assigns_arr
#         }), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500


# @admin_bp.route('/api/user-type-distribution')
# @login_required
# @admin_required
# def api_user_type_distribution():
#     """Return counts for Students/Teachers/Admins."""
#     try:
#         students = User.query.filter_by(role='student', is_deleted=False).count()
#         teachers = User.query.filter_by(role='teacher', is_deleted=False).count()
#         admins = User.query.filter_by(role='admin', is_deleted=False).count()
#         return jsonify({
#             'labels': ['Students', 'Teachers', 'Admins'],
#             'values': [students, teachers, admins]
#         }), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500


# @admin_bp.route('/api/test-results')
# @login_required
# @admin_required
# def api_test_results():
#     """Return overview of test results status."""
#     try:
#         passed = Result.query.filter_by(passed=True).count()
#         failed = Result.query.filter_by(passed=False).count()

#         # Pending: assignments that do not yet have a result
#         total_assignments = Assignment.query.count()
#         total_results = Result.query.count()
#         pending = max(total_assignments - total_results, 0)

#         in_progress = 0  # No explicit field; keep zero unless tracked elsewhere

#         return jsonify({
#             'labels': ['Passed', 'Failed', 'Pending', 'In Progress'],
#             'values': [passed, failed, pending, in_progress]
#         }), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500


# @admin_bp.route('/api/assignment-traffic')
# @login_required
# @admin_required
# def api_assignment_traffic():
#     """Return assignment traffic sources. Lacking explicit source tracking, map all to Dashboard."""
#     try:
#         total = Assignment.query.count()
#         direct = 0
#         email = 0
#         dashboard = total
#         mobile = 0
#         other = 0

#         return jsonify({
#             'labels': ['Direct Link', 'Email', 'Dashboard', 'Mobile App', 'Other'],
#             'values': [direct, email, dashboard, mobile, other]
#         }), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

"""
Admin API endpoints - FIXED VERSION
Handles all administrative functions with teacher access for test assignments
"""
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.utils.decorators import admin_required
from app.services.user_service import UserService
from app.models.user import User
from app.models.test import Test
from app.models.assignment import Assignment
from app.models.result import Result
from app.models.audit_log import AuditLog
from app.extensions.database import db
from app.utils.exceptions import ValidationError, DatabaseError
from datetime import datetime, timedelta
from sqlalchemy import func
from functools import wraps

# Create blueprint
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


# ==================== CUSTOM DECORATORS ====================

def teacher_or_admin_required(f):
    """Decorator to require teacher or admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        
        if current_user.role not in ['teacher', 'admin']:
            flash('Access denied. Teacher or Admin privileges required.', 'danger')
            return redirect(url_for('main.index'))
        
        return f(*args, **kwargs)
    return decorated_function


# ==================== WEB ROUTES ====================

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """Admin dashboard with real-time traffic monitoring"""
    try:
        # Get traffic data with error handling
        try:
            traffic_data = TrafficService.get_dashboard_data()
        except Exception as e:
            print(f"Error getting traffic data: {e}")
            # Fallback data if traffic monitoring fails
            from datetime import datetime
            traffic_data = {
                'real_time': {
                    'active_users': 0,
                    'total_requests': 0,
                    'requests_per_minute': [(datetime.utcnow().isoformat(), 0)],
                    'avg_response_time': 0,
                    'status_distribution': [],
                    'user_activity': [],
                    'top_endpoints': []
                },
                'hourly_traffic': [],
                'system_metrics': {
                    'cpu_percent': 0,
                    'memory_percent': 0,
                    'disk_percent': 0,
                    'active_connections': 0
                },
                'endpoint_performance': [],
                'error_stats': {
                    'total_errors': 0,
                    'error_rate': 0,
                    'top_errors': []
                }
            }
        
        # Get user statistics
        total_users = User.query.filter_by(is_deleted=False).count()
        total_admins = User.query.filter_by(role='admin', is_deleted=False).count()
        total_teachers = User.query.filter_by(role='teacher', is_deleted=False).count()
        total_students = User.query.filter_by(role='student', is_deleted=False).count()
        active_users = User.query.filter_by(is_active=True, is_deleted=False).count()
        
        # Get test statistics
        total_tests = Test.query.count()
        pending_assignments = Assignment.query.filter_by(status='pending').count()
        
        # Get recent activity
        recent_logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).limit(10).all()
        
        return render_template('admin/dashboard.html',
                             traffic_data=traffic_data,
                             total_users=total_users,
                             total_admins=total_admins,
                             total_teachers=total_teachers,
                             total_students=total_students,
                             active_users=active_users,
                             total_tests=total_tests,
                             pending_assignments=pending_assignments,
                             recent_logs=recent_logs
        )
        
    except Exception as e:
        print(f"Dashboard error: {e}")
        # Return a basic dashboard without traffic data
        total_users = User.query.filter_by(is_deleted=False).count()
        total_admins = User.query.filter_by(role='admin', is_deleted=False).count()
        total_teachers = User.query.filter_by(role='teacher', is_deleted=False).count()
        total_students = User.query.filter_by(role='student', is_deleted=False).count()
        active_users = User.query.filter_by(is_active=True, is_deleted=False).count()
        total_tests = Test.query.count()
        pending_assignments = Assignment.query.filter_by(status='pending').count()
        
        # Empty traffic data
        from datetime import datetime
        traffic_data = {
            'real_time': {
                'active_users': 0,
                'total_requests': 0,
                'requests_per_minute': [(datetime.utcnow().isoformat(), 0)],
                'avg_response_time': 0,
                'status_distribution': [],
                'user_activity': [],
                'top_endpoints': []
            },
            'hourly_traffic': [],
            'system_metrics': {
                'cpu_percent': 0,
                'memory_percent': 0,
                'disk_percent': 0,
                'active_connections': 0
            },
            'endpoint_performance': [],
            'error_stats': {
                'total_errors': 0,
                'error_rate': 0,
                'top_errors': []
            }
        }
        
        return render_template('admin/dashboard.html',
                             traffic_data=traffic_data,
                             total_users=total_users,
                             total_admins=total_admins,
                             total_teachers=total_teachers,
                             total_students=total_students,
                             active_users=active_users,
                             total_tests=total_tests,
                             pending_assignments=pending_assignments,
                             recent_logs=[]
        )


@admin_bp.route('/manage-users')
@login_required
@admin_required
def manage_users():
    """User management page"""
    page = request.args.get('page', 1, type=int)
    role = request.args.get('role')
    search = request.args.get('search')
    
    if search:
        users, total = UserService.search_users(search, role=role, page=page)
    else:
        users, total = UserService.get_all_users(role=role, page=page)
    
    # Calculate pagination
    pages = (total + 19) // 20  # Ceiling division
    
    return render_template(
        'admin/manage_users.html',
        users=users,
        total=total,
        page=page,
        pages=pages,
        current_role=role,
        search_query=search
    )


@admin_bp.route('/create-user', methods=['GET', 'POST'])
@login_required
@admin_required
def create_user():
    """Create user page"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        full_name = request.form.get('full_name')
        student_id = request.form.get('student_id')
        
        try:
            user = UserService.create_user(
                username=username,
                email=email,
                password=password,
                role=role,
                full_name=full_name,
                student_id=student_id if role == 'student' else None
            )
            
            flash(f'User {username} created successfully!', 'success')
            return redirect(url_for('admin.manage_users'))
            
        except (ValidationError, DatabaseError) as e:
            flash(str(e), 'danger')
    
    return render_template('admin/create_user.html')


@admin_bp.route('/users/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    """Delete user"""
    try:
        UserService.delete_user(user_id, current_user.id)
        flash('User deleted successfully!', 'success')
    except (ValidationError, DatabaseError) as e:
        flash(str(e), 'danger')
    
    return redirect(url_for('admin.manage_users'))


@admin_bp.route('/users/<int:user_id>/reset-password', methods=['POST'])
@login_required
@admin_required
def reset_user_password(user_id):
    """Reset user password"""
    try:
        new_password = UserService.reset_user_password(user_id)
        flash(f'Password reset successfully! New password: {new_password}', 'success')
    except DatabaseError as e:
        flash(str(e), 'danger')
    
    return redirect(url_for('admin.manage_users'))

@admin_bp.route('/assign-tests', methods=['GET', 'POST'])
@login_required
@teacher_or_admin_required
def assign_tests():
    """Assign tests to students - accessible by teachers and admins"""
    
    if request.method == 'POST':
        test_id = request.form.get('test_id', type=int)
        student_ids = request.form.getlist('student_ids')
        assigned_date_str = request.form.get('assigned_date')
        
        # Validation
        if not test_id:
            flash('Please select a test!', 'danger')
            return redirect(url_for('admin.assign_tests'))
        
        if not student_ids:
            flash('Please select at least one student!', 'danger')
            return redirect(url_for('admin.assign_tests'))
        
        if not assigned_date_str:
            flash('Please select an assignment date!', 'danger')
            return redirect(url_for('admin.assign_tests'))
        
        try:
            # Convert student_ids to integers
            student_ids = [int(sid) for sid in student_ids]
            
            # Parse date as a date object to avoid datetime vs date mismatches
            assign_date = datetime.strptime(assigned_date_str, '%Y-%m-%d').date()
            
            # Validate date is not in the past
            today = datetime.utcnow().date()
            if assign_date < today:
                flash('Cannot assign test with a past date! Please select today or a future date.', 'danger')
                return redirect(url_for('admin.assign_tests'))
            
            # Verify test exists
            test = Test.query.get(test_id)
            if not test:
                flash('Selected test not found!', 'danger')
                return redirect(url_for('admin.assign_tests'))
            
            # Check test status
            if hasattr(test, 'is_published') and not test.is_published:
                flash('Cannot assign unpublished test!', 'danger')
                return redirect(url_for('admin.assign_tests'))
            
            if hasattr(test, 'is_active') and not test.is_active:
                flash('Cannot assign inactive test!', 'danger')
                return redirect(url_for('admin.assign_tests'))
            
            # For teachers, verify ownership
            if current_user.role == 'teacher':
                if hasattr(test, 'created_by') and test.created_by != current_user.id:
                    flash('You can only assign tests you created!', 'danger')
                    return redirect(url_for('admin.assign_tests'))
            
            # Process assignments
            created_count = 0
            skipped_count = 0
            error_messages = []
            
            for student_id in student_ids:
                try:
                    # Verify student exists
                    student = User.query.get(student_id)
                    if not student:
                        error_messages.append(f'Student ID {student_id} not found')
                        skipped_count += 1
                        continue
                    
                    # Verify is a student
                    if student.role != 'student':
                        error_messages.append(f'{student.username} is not a student')
                        skipped_count += 1
                        continue
                    
                    # Check if active
                    if student.is_deleted or not student.is_active:
                        error_messages.append(f'Student {student.username} is inactive')
                        skipped_count += 1
                        continue
                    
                    # Check for existing assignment
                    existing = Assignment.query.filter_by(
                        student_id=student_id,
                        test_id=test_id
                    ).first()
                    
                    if existing:
                        error_messages.append(f'{student.username} already assigned this test')
                        skipped_count += 1
                        continue
                    
                    # Create new assignment
                    assignment = Assignment(
                        student_id=student_id,
                        test_id=test_id,
                        assigned_date=assign_date,
                        assigned_by=current_user.id,
                        status='pending'
                    )
                    db.session.add(assignment)
                    created_count += 1
                    
                except Exception as e:
                    error_messages.append(f'Error with student ID {student_id}: {str(e)}')
                    skipped_count += 1
            
            # Commit successful assignments
            if created_count > 0:
                db.session.commit()
                flash(f'✓ Test assigned to {created_count} student(s) successfully!', 'success')
            
            if skipped_count > 0:
                flash(f'⚠ {skipped_count} assignment(s) skipped.', 'warning')
                for msg in error_messages[:5]:
                    flash(f'  • {msg}', 'info')
            
            if created_count == 0:
                flash('No new assignments created.', 'warning')
            
            return redirect(url_for('admin.manage_test_dates'))
            
        except ValueError as e:
            flash(f'Invalid input: {str(e)}', 'danger')
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
    
    # ========== GET REQUEST - LOAD DATA FROM DATABASE ==========
    try:
        # Load tests based on role
        if current_user.role == 'admin':
            tests_query = Test.query
            if hasattr(Test, 'is_active'):
                tests_query = tests_query.filter_by(is_active=True)
            if hasattr(Test, 'is_published'):
                tests_query = tests_query.filter_by(is_published=True)
            tests = tests_query.order_by(Test.created_at.desc()).all()
        else:
            tests_query = Test.query.filter_by(created_by=current_user.id)
            if hasattr(Test, 'is_active'):
                tests_query = tests_query.filter_by(is_active=True)
            if hasattr(Test, 'is_published'):
                tests_query = tests_query.filter_by(is_published=True)
            tests = tests_query.order_by(Test.created_at.desc()).all()
        
        # ===== CRITICAL: LOAD ALL ACTIVE STUDENTS FROM DATABASE =====
        students_query = User.query.filter_by(role='student')
        
        # Apply filters to get only active students
        students_query = students_query.filter_by(is_deleted=False)
        students_query = students_query.filter_by(is_active=True)
        
        # Order by name for better UX
        if hasattr(User, 'full_name'):
            students = students_query.order_by(User.full_name.asc()).all()
        else:
            students = students_query.order_by(User.username.asc()).all()
        
        # Debug logging (remove in production)
        print(f"DEBUG: Found {len(students)} students in database")
        print(f"DEBUG: Found {len(tests)} tests in database")
        
        # Get today's date
        today = datetime.utcnow().date().isoformat()
        
        # Provide user feedback
        if not tests:
            if current_user.role == 'teacher':
                flash('No published tests available. Please create and publish a test first.', 'info')
            else:
                flash('No published tests available for assignment.', 'info')
        
        if not students:
            flash('No active students found in the database. Please add students first.', 'warning')
        else:
            flash(f'Loaded {len(students)} active student(s) from database.', 'info')
        
        # Render template with data
        return render_template(
            'admin/assign_tests.html',
            tests=tests,
            students=students,
            today=today
        )
        
    except Exception as e:
        # Handle any errors in loading data
        flash(f'Error loading page: {str(e)}', 'danger')
        print(f"ERROR in assign_tests: {str(e)}")
        import traceback
        traceback.print_exc()
        
        return render_template(
            'admin/assign_tests.html',
            tests=[],
            students=[],
            today=datetime.utcnow().date().isoformat()
        )


@admin_bp.route('/manage-test-dates')
@login_required
@teacher_or_admin_required  # FIXED: Allow teachers access
def manage_test_dates():
    """Manage test assignment dates - accessible by teachers and admins"""
    try:
        # Clear any stale session data
        db.session.expire_all()
        
        page = request.args.get('page', 1, type=int)
        test_id = request.args.get('test_id', type=int)
        student_id = request.args.get('student_id', type=int)
        
        # Use raw SQL to avoid any relationship issues
        base_query = db.select(Assignment)
        
        # FIXED: Teachers only see assignments for their tests
        if current_user.role == 'teacher':
            # Get test IDs created by current teacher
            teacher_test_ids = [t.id for t in db.session.execute(
                db.select(Test.id).where(Test.created_by == current_user.id)
            ).scalars().all()]
            
            if teacher_test_ids:
                base_query = base_query.where(Assignment.test_id.in_(teacher_test_ids))
            else:
                # Teacher has no tests, return empty result
                return render_template(
                    'admin/manage_test_dates.html',
                    assignments=[],
                    page=page,
                    pages=1,
                    tests=[],
                    students=[]
                )
        
        if test_id:
            base_query = base_query.where(Assignment.test_id == test_id)
        if student_id:
            base_query = base_query.where(Assignment.student_id == student_id)
        
        # Get total count for pagination
        count_query = db.select(func.count(Assignment.id)).select_from(base_query)
        total_count = db.session.execute(count_query).scalar()
        
        # Calculate pagination
        per_page = 20
        total_pages = (total_count + per_page - 1) // per_page
        offset = (page - 1) * per_page
        
        # Get assignments with pagination
        assignments_query = base_query.order_by(Assignment.assigned_date.desc()).offset(offset).limit(per_page)
        assignments = db.session.execute(assignments_query).scalars().all()
        
        # FIXED: Filter tests based on role
        if current_user.role == 'admin':
            tests = db.session.execute(db.select(Test).order_by(Test.name)).scalars().all()
        else:
            tests = db.session.execute(
                db.select(Test).where(Test.created_by == current_user.id).order_by(Test.name)
            ).scalars().all()
        
        students = db.session.execute(
            db.select(User).where(User.role == 'student').order_by(User.full_name)
        ).scalars().all()
        
        return render_template(
            'admin/manage_test_dates.html',
            assignments=assignments,
            page=page,
            pages=total_pages,
            tests=tests,
            students=students
        )
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        flash(f'Error loading test dates: {str(e)}', 'danger')
        return redirect(url_for('admin.dashboard'))


@admin_bp.route('/assignments/<int:assignment_id>/update', methods=['POST'])
@login_required
@teacher_or_admin_required  # FIXED: Allow teachers access
def update_assignment(assignment_id):
    """Update assignment date"""
    new_date_str = request.form.get('assigned_date')
    
    if not new_date_str:
        flash('Please provide a new date!', 'danger')
        return redirect(url_for('admin.manage_test_dates'))
    
    try:
        assignment = Assignment.query.get_or_404(assignment_id)
        
        # FIXED: Teachers can only update their own test assignments
        if current_user.role == 'teacher':
            test = Test.query.get(assignment.test_id)
            if not test or test.created_by != current_user.id:
                flash('You can only update assignments for your own tests!', 'danger')
                return redirect(url_for('admin.manage_test_dates'))
        
        new_date = datetime.strptime(new_date_str, '%Y-%m-%d').date()
        
        # FIXED: Validate new date is not in the past
        if new_date < datetime.utcnow().date():
            flash('Cannot set assignment date to the past!', 'danger')
            return redirect(url_for('admin.manage_test_dates'))
        
        assignment.assigned_date = new_date
        db.session.commit()
        flash('Assignment date updated successfully!', 'success')
        
    except ValueError:
        flash('Invalid date format!', 'danger')
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating assignment: {str(e)}', 'danger')
    
    return redirect(url_for('admin.manage_test_dates'))


@admin_bp.route('/assignments/<int:assignment_id>/delete', methods=['POST'])
@login_required
@teacher_or_admin_required  # FIXED: Allow teachers access
def delete_assignment(assignment_id):
    """Delete assignment"""
    try:
        print(f"DEBUG: Attempting to delete assignment {assignment_id}")
        
        # Use a simple query without any relationships first
        assignment = db.session.execute(
            db.select(Assignment).where(Assignment.id == assignment_id)
        ).scalar_one_or_none()
        
        if not assignment:
            flash('Assignment not found!', 'danger')
            return redirect(url_for('admin.manage_test_dates'))
            
        print(f"DEBUG: Found assignment: {assignment}")
        
        # FIXED: Teachers can only delete their own test assignments
        if current_user.role == 'teacher':
            test = db.session.execute(
                db.select(Test).where(Test.id == assignment.test_id)
            ).scalar_one_or_none()
            if not test or test.created_by != current_user.id:
                flash('You can only delete assignments for your own tests!', 'danger')
                return redirect(url_for('admin.manage_test_dates'))
        
        # FIXED: Prevent deletion if test already completed
        # Check if result exists for this student and test combination
        print(f"DEBUG: Checking for result with student_id={assignment.student_id}, test_id={assignment.test_id}")
        
        # Use raw SQL to avoid any relationship issues
        result_exists = db.session.execute(
            db.select(Result).where(
                Result.student_id == assignment.student_id,
                Result.test_id == assignment.test_id
            )
        ).scalar_one_or_none()
        
        print(f"DEBUG: Found result: {result_exists}")
        
        if result_exists:
            # Get student and test names safely
            student = db.session.execute(
                db.select(User).where(User.id == assignment.student_id)
            ).scalar_one_or_none()
            test = db.session.execute(
                db.select(Test).where(Test.id == assignment.test_id)
            ).scalar_one_or_none()
            
            student_name = student.username if student else 'Unknown Student'
            test_name = test.name if test else 'Unknown Test'
            flash(f'Cannot delete assignment - {student_name} has already completed {test_name}!', 'danger')
            return redirect(url_for('admin.manage_test_dates'))
        
        # FIXED: Prevent deletion if test is currently in progress
        if assignment.status == 'in_progress':
            student = db.session.execute(
                db.select(User).where(User.id == assignment.student_id)
            ).scalar_one_or_none()
            test = db.session.execute(
                db.select(Test).where(Test.id == assignment.test_id)
            ).scalar_one_or_none()
            
            student_name = student.username if student else 'Unknown Student'
            test_name = test.name if test else 'Unknown Test'
            flash(f'Cannot delete assignment - {student_name} is currently taking {test_name}!', 'danger')
            return redirect(url_for('admin.manage_test_dates'))
        
        # Store assignment info for success message
        student = db.session.execute(
            db.select(User).where(User.id == assignment.student_id)
        ).scalar_one_or_none()
        test = db.session.execute(
            db.select(Test).where(Test.id == assignment.test_id)
        ).scalar_one_or_none()
        
        student_name = student.username if student else 'Unknown Student'
        test_name = test.name if test else 'Unknown Test'
        
        print(f"DEBUG: Deleting assignment {assignment_id}")
        
        # Delete the assignment using raw SQL to avoid relationship issues
        db.session.execute(
            db.delete(Assignment).where(Assignment.id == assignment_id)
        )
        db.session.commit()
        flash(f'Assignment for {student_name} - {test_name} removed successfully!', 'success')
        
    except Exception as e:
        db.session.rollback()
        import traceback
        print("DEBUG: Exception occurred:")
        traceback.print_exc()
        flash(f'Error removing assignment: {str(e)}', 'danger')
    
    return redirect(url_for('admin.manage_test_dates'))


@admin_bp.route('/system-logs')
@login_required
@admin_required
def system_logs():
    """View system audit logs"""
    page = request.args.get('page', 1, type=int)
    user_id = request.args.get('user_id', type=int)
    action = request.args.get('action')
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    
    query = AuditLog.query
    
    # Filters
    if user_id:
        query = query.filter_by(user_id=user_id)
    if action:
        query = query.filter_by(action=action)
    if date_from:
        date_from_dt = datetime.strptime(date_from, '%Y-%m-%d')
        query = query.filter(AuditLog.timestamp >= date_from_dt)
    if date_to:
        date_to_dt = datetime.strptime(date_to, '%Y-%m-%d') + timedelta(days=1)
        query = query.filter(AuditLog.timestamp < date_to_dt)
    
    logs = query.order_by(AuditLog.timestamp.desc()).paginate(
        page=page, per_page=50, error_out=False
    )
    
    # Get unique users and actions for filters
    users = User.query.all()
    actions = db.session.query(AuditLog.action).distinct().all()
    actions = [a[0] for a in actions]
    
    return render_template(
        'admin/system_logs.html',
        logs=logs.items,
        page=page,
        pages=logs.pages,
        users=users,
        actions=actions
    )


# ==================== API ENDPOINTS ====================

@admin_bp.route('/api/traffic/debug')
@login_required
@admin_required
def api_traffic_debug():
    """Debug endpoint to check traffic logging"""
    try:
        from app.models.traffic import TrafficLog
        from datetime import datetime, timedelta
        from flask import request
        
        # Check recent logs
        since = datetime.utcnow() - timedelta(minutes=5)
        recent_logs = TrafficLog.query.filter(TrafficLog.timestamp >= since).all()
        
        # Check current request info
        from flask_login import current_user
        current_info = {
            'is_authenticated': current_user.is_authenticated if current_user else False,
            'user_id': current_user.id if current_user and current_user.is_authenticated else None,
            'role': current_user.role if current_user and current_user.is_authenticated else None,
            'request_endpoint': request.endpoint,
            'request_method': request.method,
            'remote_addr': request.remote_addr
        }
        
        # Get database stats
        total_logs = TrafficLog.query.count()
        logs_with_users = TrafficLog.query.filter(TrafficLog.user_id.isnot(None)).count()
        
        debug_info = {
            'current_request': current_info,
            'database_stats': {
                'total_logs': total_logs,
                'logs_with_users': logs_with_users,
                'recent_logs_5min': len(recent_logs)
            },
            'recent_logs': [
                {
                    'id': log.id,
                    'timestamp': log.timestamp.isoformat(),
                    'endpoint': log.endpoint,
                    'method': log.method,
                    'user_id': log.user_id,
                    'user_role': log.user_role,
                    'status_code': log.status_code,
                    'ip_address': log.ip_address
                }
                for log in recent_logs[-10:]  # Last 10 logs
            ],
            'real_time_stats': TrafficLog.get_real_time_stats(minutes=1)
        }
        
        return jsonify({
            'success': True,
            'debug_info': debug_info
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'error_type': str(type(e).__name__)
        }), 500

@admin_bp.route('/api/traffic/test-log')
@login_required
@admin_required
def api_test_traffic_log():
    """Test endpoint to create a traffic log entry"""
    try:
        from app.models.traffic import TrafficLog
        from flask_login import current_user
        
        # Create a test log entry
        test_log = TrafficLog.log_request(
            endpoint='admin.test_traffic_log',
            method='GET',
            status_code=200,
            ip_address='127.0.0.1',
            user_agent='Test Browser',
            user_id=current_user.id if current_user.is_authenticated else None,
            user_role=current_user.role if current_user.is_authenticated else None,
            response_time=50.0
        )
        
        return jsonify({
            'success': True,
            'test_log_id': test_log.id if test_log else None,
            'message': 'Test log entry created'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@admin_bp.route('/api/traffic/live')
@login_required
@admin_required
def api_traffic_live():
    """Get truly real-time traffic data based on actual user sessions"""
    try:
        from datetime import datetime
        from app.services.traffic_service import TrafficService
        
        # Get live statistics based on actual sessions
        live_stats = TrafficService.get_real_time_stats()
        
        # Get current activity
        current_activity = TrafficService.get_live_activity(limit=20)
        
        return jsonify({
            'success': True,
            'live_stats': live_stats,
            'current_activity': current_activity,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@admin_bp.route('/api/traffic/current')
@login_required
@admin_required
def api_traffic_current():
    """Get current real-time metrics based on actual user sessions"""
    try:
        from app.services.traffic_service import TrafficService
        
        # Get real-time stats based on actual login sessions
        stats = TrafficService.get_current_stats()
        
        return jsonify({
            'success': True,
            'data': stats,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@admin_bp.route('/api/traffic/realtime')
@login_required
@admin_required
def api_traffic_realtime():
    """Get real-time traffic data"""
    from app.services.traffic_service import TrafficService
    data = TrafficService.get_real_time_stats(minutes=1)  # Changed to 1 minute for more real-time
    return jsonify(data)

@admin_bp.route('/api/traffic/hourly')
@login_required
@admin_required
def api_traffic_hourly():
    """Get hourly traffic data"""
    hours = request.args.get('hours', 24, type=int)
    from app.services.traffic_service import TrafficService
    data = TrafficService.get_hourly_traffic(hours)
    return jsonify(data)

@admin_bp.route('/api/traffic/system-metrics')
@login_required
@admin_required
def api_system_metrics():
    """Get system metrics"""
    from app.services.traffic_service import TrafficService
    data = TrafficService.get_system_metrics()
    return jsonify(data)

@admin_bp.route('/api/traffic/performance')
@login_required
@admin_required
def api_endpoint_performance():
    """Get endpoint performance metrics"""
    from app.services.traffic_service import TrafficService
    data = TrafficService.get_endpoint_performance()
    return jsonify(data)

@admin_bp.route('/api/traffic/errors')
@login_required
@admin_required
def api_error_analysis():
    """Get error analysis"""
    from app.services.traffic_service import TrafficService
    data = TrafficService.get_error_analysis()
    return jsonify(data)

@admin_bp.route('/api/dashboard')
@login_required
@admin_required
def api_dashboard():
    """API endpoint for dashboard statistics"""
    user_stats = UserService.get_user_statistics()
    
    return jsonify({
        'success': True,
        'statistics': {
            'users': user_stats,
            'total_tests': Test.query.count(),
            'active_assignments': Assignment.query.filter_by(status='pending').count(),
            'completed_tests': Result.query.count()
        }
    }), 200


@admin_bp.route('/api/users')
@login_required
@admin_required
def api_get_users():
    """API endpoint to list all users"""
    role = request.args.get('role')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search')
    
    if search:
        users, total = UserService.search_users(search, role=role, page=page, per_page=per_page)
    else:
        users, total = UserService.get_all_users(role=role, page=page, per_page=per_page)
    
    return jsonify({
        'success': True,
        'users': [u.to_dict() for u in users],
        'total': total,
        'page': page,
        'per_page': per_page
    }), 200


@admin_bp.route('/api/users', methods=['POST'])
@login_required
@admin_required
def api_create_user():
    """API endpoint to create user"""
    data = request.get_json()
    
    try:
        user = UserService.create_user(
            username=data.get('username'),
            email=data.get('email'),
            password=data.get('password'),
            role=data.get('role'),
            full_name=data.get('full_name'),
            student_id=data.get('student_id')
        )
        
        return jsonify({
            'success': True,
            'message': 'User created successfully',
            'user': user.to_dict()
        }), 201
        
    except (ValidationError, DatabaseError) as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@admin_bp.route('/api/users/<int:user_id>')
@login_required
@admin_required
def api_get_user(user_id):
    """API endpoint to get single user"""
    user = UserService.get_user_by_id(user_id)
    
    if not user:
        return jsonify({
            'success': False,
            'error': 'User not found'
        }), 404
    
    return jsonify({
        'success': True,
        'user': user.to_dict(include_sensitive=True)
    }), 200


@admin_bp.route('/api/users/<int:user_id>', methods=['PUT'])
@login_required
@admin_required
def api_update_user(user_id):
    """API endpoint to update user"""
    data = request.get_json()
    
    try:
        user = UserService.update_user(user_id, **data)
        
        return jsonify({
            'success': True,
            'message': 'User updated successfully',
            'user': user.to_dict()
        }), 200
        
    except (ValidationError, DatabaseError) as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@admin_bp.route('/api/users/<int:user_id>', methods=['DELETE'])
@login_required
@admin_required
def api_delete_user(user_id):
    """API endpoint to delete user"""
    try:
        UserService.delete_user(user_id, current_user.id)
        
        return jsonify({
            'success': True,
            'message': 'User deleted successfully'
        }), 200
        
    except (ValidationError, DatabaseError) as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@admin_bp.route('/api/users/<int:user_id>/reset-password', methods=['POST'])
@login_required
@admin_required
def api_reset_password(user_id):
    """API endpoint to reset user password"""
    try:
        new_password = UserService.reset_user_password(user_id)
        
        return jsonify({
            'success': True,
            'message': 'Password reset successfully',
            'new_password': new_password
        }), 200
        
    except DatabaseError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@admin_bp.route('/api/tests')
@login_required
@teacher_or_admin_required  # FIXED: Allow teachers access
def api_get_tests():
    """API endpoint to list tests based on user role"""
    # FIXED: Filter based on role
    if current_user.role == 'admin':
        tests = Test.query.all()
    else:
        tests = Test.query.filter_by(created_by=current_user.id).all()
    
    return jsonify({
        'success': True,
        'tests': [t.to_dict() for t in tests]
    }), 200


@admin_bp.route('/api/assignments', methods=['POST'])
@login_required
@teacher_or_admin_required  # FIXED: Allow teachers access
def api_create_assignment():
    """API endpoint to create assignment"""
    data = request.get_json()
    
    try:
        test_id = data.get('test_id')
        student_ids = data.get('student_ids', [])
        assigned_date_str = data.get('assigned_date')
        
        if not test_id or not student_ids or not assigned_date_str:
            return jsonify({
                'success': False,
                'error': 'Missing required fields: test_id, student_ids, assigned_date'
            }), 400
        
        # FIXED: Verify test exists and permissions
        test = Test.query.get(test_id)
        if not test:
            return jsonify({
                'success': False,
                'error': 'Test not found'
            }), 404
        
        if current_user.role == 'teacher' and test.created_by != current_user.id:
            return jsonify({
                'success': False,
                'error': 'You can only assign tests you created'
            }), 403
        
        if not test.is_published or not test.is_active:
            return jsonify({
                'success': False,
                'error': 'Test must be published and active'
            }), 400
        
        assigned_date = datetime.strptime(assigned_date_str, '%Y-%m-%d').date()
        
        # FIXED: Validate date
        if assigned_date < datetime.utcnow().date():
            return jsonify({
                'success': False,
                'error': 'Assignment date cannot be in the past'
            }), 400
        
        assignments = []
        skipped = 0
        
        for student_id in student_ids:
            # Check for existing assignment
            existing = Assignment.query.filter_by(
                student_id=student_id,
                test_id=test_id
            ).first()
            
            if existing:
                skipped += 1
                continue
            
            assignment = Assignment(
                student_id=student_id,
                test_id=test_id,
                assigned_date=assigned_date,
                assigned_by=current_user.id,
                status='pending'
            )
            db.session.add(assignment)
            assignments.append(assignment)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'{len(assignments)} assignment(s) created, {skipped} skipped',
            'assignments': [a.to_dict() for a in assignments],
            'skipped': skipped
        }), 201
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': f'Invalid date format: {str(e)}'
        }), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@admin_bp.route('/api/assignments')
@login_required
@teacher_or_admin_required  # FIXED: Allow teachers access
def api_get_assignments():
    """API endpoint to list assignments"""
    test_id = request.args.get('test_id', type=int)
    student_id = request.args.get('student_id', type=int)
    
    query = Assignment.query
    
    # FIXED: Teachers only see their test assignments
    if current_user.role == 'teacher':
        teacher_test_ids = [t.id for t in Test.query.filter_by(created_by=current_user.id).all()]
        query = query.filter(Assignment.test_id.in_(teacher_test_ids))
    
    if test_id:
        query = query.filter_by(test_id=test_id)
    if student_id:
        query = query.filter_by(student_id=student_id)
    
    assignments = query.all()
    
    return jsonify({
        'success': True,
        'assignments': [a.to_dict() for a in assignments]
    }), 200


@admin_bp.route('/api/assignments/<int:assignment_id>', methods=['PUT'])
@login_required
@teacher_or_admin_required  # FIXED: Allow teachers access
def api_update_assignment(assignment_id):
    """API endpoint to update assignment"""
    data = request.get_json()
    
    try:
        assignment = Assignment.query.get_or_404(assignment_id)
        
        # FIXED: Teachers can only update their own test assignments
        if current_user.role == 'teacher':
            test = Test.query.get(assignment.test_id)
            if not test or test.created_by != current_user.id:
                return jsonify({
                    'success': False,
                    'error': 'You can only update assignments for your own tests'
                }), 403
        
        if 'assigned_date' in data:
            new_date = datetime.strptime(data['assigned_date'], '%Y-%m-%d')
            
            # FIXED: Validate date
            if new_date.date() < datetime.utcnow().date():
                return jsonify({
                    'success': False,
                    'error': 'Assignment date cannot be in the past'
                }), 400
            
            assignment.assigned_date = new_date
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Assignment updated successfully',
            'assignment': assignment.to_dict()
        }), 200
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': f'Invalid date format: {str(e)}'
        }), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@admin_bp.route('/api/audit-logs')
@login_required
@admin_required
def api_get_audit_logs():
    """API endpoint to get audit logs"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    user_id = request.args.get('user_id', type=int)
    action = request.args.get('action')
    
    query = AuditLog.query
    
    if user_id:
        query = query.filter_by(user_id=user_id)
    if action:
        query = query.filter_by(action=action)
    
    logs = query.order_by(AuditLog.timestamp.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'success': True,
        'logs': [log.to_dict() for log in logs.items],
        'total': logs.total,
        'page': page,
        'per_page': per_page
    }), 200


# ==================== DASHBOARD CHART DATA ====================

@admin_bp.route('/api/daily-users')
@login_required
@admin_required
def api_daily_users():
    """Return last 14 days data for active users, tests, and assignments."""
    try:
        days = 14
        today = datetime.utcnow().date()
        labels = []
        users_arr, tests_arr, assigns_arr = [], [], []

        for i in range(days - 1, -1, -1):
            day = today - timedelta(days=i)
            next_day = day + timedelta(days=1)
            labels.append(f"{day.month}/{day.day}")

            # active users: distinct user_id appearing in audit logs on that day
            users_count = (db.session.query(AuditLog.user_id)
                           .filter(AuditLog.timestamp >= datetime.combine(day, datetime.min.time()))
                           .filter(AuditLog.timestamp < datetime.combine(next_day, datetime.min.time()))
                           .distinct()
                           .count())

            # tests taken (results completed that day)
            tests_count = (db.session.query(Result.id)
                           .filter(Result.completed_at >= datetime.combine(day, datetime.min.time()))
                           .filter(Result.completed_at < datetime.combine(next_day, datetime.min.time()))
                           .count())

            # assignments created that day
            assigns_count = (db.session.query(Assignment.id)
                             .filter(Assignment.assigned_date >= datetime.combine(day, datetime.min.time()))
                             .filter(Assignment.assigned_date < datetime.combine(next_day, datetime.min.time()))
                             .count())

            users_arr.append(users_count)
            tests_arr.append(tests_count)
            assigns_arr.append(assigns_count)

        return jsonify({
            'labels': labels,
            'users': users_arr,
            'tests': tests_arr,
            'assignments': assigns_arr
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/api/user-type-distribution')
@login_required
@admin_required
def api_user_type_distribution():
    """Return counts for Students/Teachers/Admins."""
    try:
        students = User.query.filter_by(role='student', is_deleted=False).count()
        teachers = User.query.filter_by(role='teacher', is_deleted=False).count()
        admins = User.query.filter_by(role='admin', is_deleted=False).count()
        return jsonify({
            'labels': ['Students', 'Teachers', 'Admins'],
            'values': [students, teachers, admins]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/api/test-results')
@login_required
@admin_required
def api_test_results():
    """Return overview of test results status."""
    try:
        passed = Result.query.filter_by(passed=True).count()
        failed = Result.query.filter_by(passed=False).count()

        # Pending: assignments that do not yet have a result
        total_assignments = Assignment.query.count()
        total_results = Result.query.count()
        pending = max(total_assignments - total_results, 0)

        in_progress = 0  # No explicit field; keep zero unless tracked elsewhere

        return jsonify({
            'labels': ['Passed', 'Failed', 'Pending', 'In Progress'],
            'values': [passed, failed, pending, in_progress]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/api/assignment-traffic')
@login_required
@admin_required
def api_assignment_traffic():
    """Return assignment traffic sources. Lacking explicit source tracking, map all to Dashboard."""
    try:
        total = Assignment.query.count()
        direct = 0
        email = 0
        dashboard = total
        mobile = 0
        other = 0

        return jsonify({
            'labels': ['Direct Link', 'Email', 'Dashboard', 'Mobile App', 'Other'],
            'values': [direct, email, dashboard, mobile, other]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
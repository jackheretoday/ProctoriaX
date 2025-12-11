"""
Authentication API endpoints
"""
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from app.services.auth_service import AuthService
from app.services.session_service import SessionService
from app.models.audit_log import AuditLog
from app.utils.helpers import get_client_ip
from app.utils.exceptions import AuthenticationError

# Create blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login page and handler"""
    # Redirect if already logged in
    if current_user.is_authenticated:
        if current_user.is_admin():
            return redirect(url_for('admin.dashboard'))
        elif current_user.is_teacher():
            return redirect(url_for('teacher.dashboard'))
        elif current_user.is_student():
            return redirect(url_for('student.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember', False)
        
        if not username or not password:
            flash('Please enter username and password.', 'danger')
            return render_template('auth/login.html')
        
        try:
            # Authenticate user
            user = AuthService.authenticate_user(
                username=username,
                password=password,
                ip_address=get_client_ip()
            )
            
            # Log in user
            login_user(user, remember=remember)
            
            # Create session
            SessionService.create_session(user)
            
            # Create user session for monitoring (with error handling)
            try:
                from app.models.user_session import UserSession
                import uuid
                session_id = str(uuid.uuid4())
                UserSession.create_session(
                    user=user,
                    session_id=session_id,
                    ip_address=request.remote_addr,
                    user_agent=request.headers.get('User-Agent')
                )
                
                # Store session ID in Flask session for tracking
                session['session_id'] = session_id
            except Exception as session_error:
                print(f"Session creation failed: {session_error}")
                # Continue with login even if session tracking fails
                pass
            
            flash(f'Welcome, {user.username}!', 'success')
            
            # Redirect based on role
            if user.is_admin():
                return redirect(url_for('admin.dashboard'))
            elif user.is_teacher():
                return redirect(url_for('teacher.dashboard'))
            elif user.is_student():
                return redirect(url_for('student.dashboard'))
            else:
                return redirect(url_for('index'))
            
        except AuthenticationError as e:
            flash(str(e), 'danger')
            return render_template('auth/login.html')
    
    return render_template('auth/login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Registration page and handler"""
    # Redirect if already logged in
    if current_user.is_authenticated:
        if current_user.is_admin():
            return redirect(url_for('admin.dashboard'))
        elif current_user.is_teacher():
            return redirect(url_for('teacher.dashboard'))
        elif current_user.is_student():
            return redirect(url_for('student.dashboard'))
    
    if request.method == 'POST':
        # Get form data
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        full_name = request.form.get('full_name', '').strip()
        student_id = request.form.get('student_id', '').strip()
        role = request.form.get('role', 'student')
        
        # Validate input
        if not all([username, email, password, confirm_password, full_name]):
            flash('Please fill in all required fields.', 'danger')
            return render_template('auth/register.html')
        
        # Check password match
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('auth/register.html')
        
        # Validate password strength
        if len(password) < 8:
            flash('Password must be at least 8 characters long.', 'danger')
            return render_template('auth/register.html')
        
        # Check if username exists
        from app.models.user import User
        from app.extensions.database import db
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists. Please choose another.', 'danger')
            return render_template('auth/register.html')
        
        # Check if email exists
        if User.query.filter_by(email=email).first():
            flash('Email already registered. Please use another email.', 'danger')
            return render_template('auth/register.html')
        
        try:
            # Create new user
            password_hash = AuthService.hash_password(password)
            
            new_user = User(
                username=username,
                email=email,
                password_hash=password_hash,
                role=role,
                full_name=full_name,
                student_id=student_id if student_id else None,
                is_active=True,  # Users are active by default when registering
                is_verified=True  # Email is considered verified for direct registration
            )
            
            db.session.add(new_user)
            db.session.commit()
            
            # Log registration
            AuditLog.log_action(
                action='user_registered',
                username=username,
                ip_address=get_client_ip(),
                details=f'New {role} registered successfully'
            )
            
            flash('Registration successful! You can now log in with your credentials.', 'success')
            return redirect(url_for('auth.login'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Registration failed: {str(e)}', 'danger')
            return render_template('auth/register.html')
    
    return render_template('auth/register.html')


@auth_bp.route('/logout')
@login_required
def logout():
    """Logout handler"""
    # Log logout
    AuditLog.log_logout(user=current_user, ip_address=get_client_ip())
    
    # End user session for monitoring (with error handling)
    try:
        from app.models.user_session import UserSession
        session_id = session.get('session_id')
        if session_id:
            UserSession.end_session(user_id=current_user.id, session_id=session_id)
    except Exception as session_error:
        print(f"Session end failed: {session_error}")
        # Continue with logout even if session tracking fails
        pass
    
    # Destroy session
    SessionService.destroy_session()
    
    # Logout user
    logout_user()
    
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Change password page and handler"""
    if request.method == 'POST':
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        if not old_password or not new_password or not confirm_password:
            flash('Please fill in all fields.', 'danger')
            return render_template('auth/change_password.html')
        
        if new_password != confirm_password:
            flash('New passwords do not match.', 'danger')
            return render_template('auth/change_password.html')
        
        try:
            # Change password
            AuthService.change_password(
                user=current_user,
                old_password=old_password,
                new_password=new_password
            )
            
            flash('Password changed successfully.', 'success')
            return redirect(url_for('index'))
            
        except AuthenticationError as e:
            flash(str(e), 'danger')
            return render_template('auth/change_password.html')
    
    return render_template('auth/change_password.html')


# API endpoints for AJAX requests
@auth_bp.route('/api/login', methods=['POST'])
def api_login():
    """API endpoint for login"""
    data = request.get_json()
    
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({
            'success': False,
            'message': 'Username and password required'
        }), 400
    
    try:
        user = AuthService.authenticate_user(
            username=username,
            password=password,
            ip_address=get_client_ip()
        )
        
        login_user(user)
        SessionService.create_session(user)
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'user': user.to_dict()
        }), 200
        
    except AuthenticationError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 401


@auth_bp.route('/api/logout', methods=['POST'])
@login_required
def api_logout():
    """API endpoint for logout"""
    AuditLog.log_logout(user=current_user, ip_address=get_client_ip())
    SessionService.destroy_session()
    logout_user()
    
    return jsonify({
        'success': True,
        'message': 'Logout successful'
    }), 200


@auth_bp.route('/api/current-user', methods=['GET'])
@login_required
def api_current_user():
    """Get current user info"""
    return jsonify({
        'success': True,
        'user': current_user.to_dict()
    }), 200

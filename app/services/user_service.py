"""
User Service
Handles user CRUD operations for admin module
"""
from app.models.user import User
from app.models.audit_log import AuditLog
from app.services.auth_service import AuthService
from app.extensions.database import db
from app.utils.validators import validate_email, validate_username, validate_role
from app.utils.helpers import generate_random_string
from app.utils.exceptions import ValidationError, DatabaseError
from sqlalchemy.exc import IntegrityError


class UserService:
    """Service for managing users"""
    
    @staticmethod
    def create_user(username, email, password, role, **kwargs):
        """
        Create a new user
        
        Args:
            username: Username (unique)
            email: Email address
            password: Plain text password
            role: User role (admin, teacher, student)
            **kwargs: Additional fields (full_name, student_id)
            
        Returns:
            User object
            
        Raises:
            ValidationError: If validation fails
            DatabaseError: If database error occurs
        """
        # Validate username
        is_valid, error = validate_username(username)
        if not is_valid:
            raise ValidationError(error)
        
        # Validate email
        if not validate_email(email):
            raise ValidationError("Invalid email format")
        
        # Validate role
        if not validate_role(role):
            raise ValidationError(f"Invalid role. Must be admin, teacher, or student")
        
        # Check if username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            raise ValidationError(f"Username '{username}' already exists")
        
        # Check if email already exists
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            raise ValidationError(f"Email '{email}' already exists")
        
        # Hash password
        password_hash = AuthService.hash_password(password)
        
        # Create user
        try:
            user = User(
                username=username,
                email=email,
                password_hash=password_hash,
                role=role,
                full_name=kwargs.get('full_name'),
                student_id=kwargs.get('student_id'),
                is_active=kwargs.get('is_active', True),
                is_verified=kwargs.get('is_verified', True)
            )
            
            db.session.add(user)
            db.session.commit()
            
            # Log user creation
            AuditLog.log_action(
                action='create_user',
                user=None,  # Admin user will be logged by middleware
                resource_type='user',
                resource_id=user.id,
                details=f"Created user: {username} with role: {role}"
            )
            
            return user
            
        except IntegrityError as e:
            db.session.rollback()
            raise DatabaseError(f"Database error: {str(e)}")
        except Exception as e:
            db.session.rollback()
            raise DatabaseError(f"Error creating user: {str(e)}")
    
    @staticmethod
    def get_all_users(role=None, active_only=False, page=1, per_page=20):
        """
        Get all users with optional filtering
        
        Args:
            role: Filter by role (optional)
            active_only: Only return active users
            page: Page number for pagination
            per_page: Items per page
            
        Returns:
            Tuple of (users list, total count)
        """
        query = User.query.filter_by(is_deleted=False)
        
        # Filter by role
        if role:
            query = query.filter_by(role=role)
        
        # Filter active only
        if active_only:
            query = query.filter_by(is_active=True)
        
        # Get total count
        total = query.count()
        
        # Paginate
        users = query.order_by(User.created_at.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return users.items, total
    
    @staticmethod
    def get_user_by_id(user_id):
        """
        Get user by ID
        
        Args:
            user_id: User ID
            
        Returns:
            User object or None
        """
        return User.query.filter_by(id=user_id, is_deleted=False).first()
    
    @staticmethod
    def get_user_by_username(username):
        """
        Get user by username
        
        Args:
            username: Username
            
        Returns:
            User object or None
        """
        return User.query.filter_by(username=username, is_deleted=False).first()
    
    @staticmethod
    def update_user(user_id, **kwargs):
        """
        Update user details
        
        Args:
            user_id: User ID
            **kwargs: Fields to update (email, role, is_active, full_name)
            
        Returns:
            Updated user object
            
        Raises:
            ValidationError: If validation fails
            DatabaseError: If user not found or database error
        """
        user = UserService.get_user_by_id(user_id)
        if not user:
            raise DatabaseError("User not found")
        
        # Update allowed fields
        if 'email' in kwargs:
            email = kwargs['email']
            if not validate_email(email):
                raise ValidationError("Invalid email format")
            
            # Check if email already taken by another user
            existing = User.query.filter_by(email=email).first()
            if existing and existing.id != user_id:
                raise ValidationError(f"Email '{email}' already in use")
            
            user.email = email
        
        if 'role' in kwargs:
            role = kwargs['role']
            if not validate_role(role):
                raise ValidationError("Invalid role")
            user.role = role
        
        if 'is_active' in kwargs:
            user.is_active = kwargs['is_active']
        
        if 'full_name' in kwargs:
            user.full_name = kwargs['full_name']
        
        if 'student_id' in kwargs:
            user.student_id = kwargs['student_id']
        
        try:
            db.session.commit()
            
            # Log update
            AuditLog.log_action(
                action='update_user',
                resource_type='user',
                resource_id=user.id,
                details=f"Updated user: {user.username}"
            )
            
            return user
            
        except Exception as e:
            db.session.rollback()
            raise DatabaseError(f"Error updating user: {str(e)}")
    
    @staticmethod
    def delete_user(user_id, current_user_id=None):
        """
        Delete user (soft delete)
        
        Args:
            user_id: User ID to delete
            current_user_id: ID of user performing deletion (cannot delete self)
            
        Returns:
            True if deleted
            
        Raises:
            ValidationError: If trying to delete self
            DatabaseError: If user not found
        """
        # Prevent deleting yourself
        if current_user_id and user_id == current_user_id:
            raise ValidationError("Cannot delete your own account")
        
        user = UserService.get_user_by_id(user_id)
        if not user:
            raise DatabaseError("User not found")
        
        try:
            # Soft delete
            user.soft_delete()
            db.session.commit()
            
            # Log deletion
            AuditLog.log_action(
                action='delete_user',
                resource_type='user',
                resource_id=user.id,
                details=f"Deleted user: {user.username}"
            )
            
            return True
            
        except Exception as e:
            db.session.rollback()
            raise DatabaseError(f"Error deleting user: {str(e)}")
    
    @staticmethod
    def reset_user_password(user_id):
        """
        Reset user password to a random one
        
        Args:
            user_id: User ID
            
        Returns:
            New plain text password (show to admin once)
            
        Raises:
            DatabaseError: If user not found
        """
        user = UserService.get_user_by_id(user_id)
        if not user:
            raise DatabaseError("User not found")
        
        # Generate random password
        new_password = generate_random_string(12)
        
        try:
            # Reset password
            AuthService.reset_password(user, new_password)
            
            # Log password reset
            AuditLog.log_action(
                action='reset_password',
                resource_type='user',
                resource_id=user.id,
                details=f"Reset password for user: {user.username}"
            )
            
            return new_password
            
        except Exception as e:
            raise DatabaseError(f"Error resetting password: {str(e)}")
    
    @staticmethod
    def get_user_statistics():
        """
        Get user statistics
        
        Returns:
            Dict with user counts by role
        """
        total_users = User.query.filter_by(is_deleted=False).count()
        total_admins = User.query.filter_by(role='admin', is_deleted=False).count()
        total_teachers = User.query.filter_by(role='teacher', is_deleted=False).count()
        total_students = User.query.filter_by(role='student', is_deleted=False).count()
        active_users = User.query.filter_by(is_active=True, is_deleted=False).count()
        
        return {
            'total_users': total_users,
            'total_admins': total_admins,
            'total_teachers': total_teachers,
            'total_students': total_students,
            'active_users': active_users,
            'inactive_users': total_users - active_users
        }
    
    @staticmethod
    def search_users(query, role=None, page=1, per_page=20):
        """
        Search users by username or email
        
        Args:
            query: Search query
            role: Filter by role (optional)
            page: Page number
            per_page: Items per page
            
        Returns:
            Tuple of (users list, total count)
        """
        search = f"%{query}%"
        user_query = User.query.filter(
            db.or_(
                User.username.ilike(search),
                User.email.ilike(search)
            ),
            User.is_deleted == False
        )
        
        if role:
            user_query = user_query.filter_by(role=role)
        
        total = user_query.count()
        
        users = user_query.order_by(User.created_at.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return users.items, total

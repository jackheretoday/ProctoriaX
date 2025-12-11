"""
Authentication Service
Handles password hashing, verification, and user authentication
"""
import bcrypt
from app.models.user import User
from app.models.audit_log import AuditLog
from app.extensions.database import db
from app.utils.exceptions import AuthenticationError


class AuthService:
    """Authentication service for user login and password management"""
    
    @staticmethod
    def hash_password(password):
        """
        Hash password using bcrypt
        
        Args:
            password: Plain text password
            
        Returns:
            Hashed password string
        """
        if not password:
            raise ValueError("Password cannot be empty")
        
        # Generate salt and hash password
        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        
        return hashed.decode('utf-8')
    
    @staticmethod
    def verify_password(password, password_hash):
        """
        Verify password against hash
        
        Args:
            password: Plain text password
            password_hash: Hashed password (string or bytes)
            
        Returns:
            True if password matches, False otherwise
        """
        if not password or not password_hash:
            return False
        
        try:
            # Convert password to bytes if it's a string
            if isinstance(password, str):
                password = password.encode('utf-8')
            
            # Convert hash to bytes if it's a string
            if isinstance(password_hash, str):
                password_hash = password_hash.encode('utf-8')
            
            return bcrypt.checkpw(password, password_hash)
        except Exception as e:
            print(f"Password verification error: {str(e)}")
            return False
    
    @staticmethod
    def authenticate_user(username, password, ip_address=None):
        """
        Authenticate user with username and password
        
        Args:
            username: Username
            password: Password
            ip_address: IP address of request
            
        Returns:
            User object if authentication successful
            
        Raises:
            AuthenticationError: If authentication fails
        """
        # Find user by username
        user = User.query.filter_by(username=username).first()
        
        if not user:
            # Log failed login attempt
            if ip_address:
                AuditLog.log_failed_login(
                    username=username,
                    ip_address=ip_address,
                    error_message="User not found"
                )
            raise AuthenticationError("Invalid username or password")
        
        # Check if account is locked
        if user.is_locked():
            if ip_address:
                AuditLog.log_failed_login(
                    username=username,
                    ip_address=ip_address,
                    error_message="Account locked"
                )
            raise AuthenticationError("Account is locked. Please try again later.")
        
        # Check if account is active
        if not user.is_active:
            if ip_address:
                AuditLog.log_failed_login(
                    username=username,
                    ip_address=ip_address,
                    error_message="Account inactive"
                )
            raise AuthenticationError("Account is inactive")
        
        # Verify password
        if not AuthService.verify_password(password, user.password_hash):
            # Increment failed login attempts
            user.increment_failed_login()
            
            # Lock account if too many failed attempts
            if user.failed_login_attempts >= 5:
                user.lock_account(minutes=15)
            
            if ip_address:
                AuditLog.log_failed_login(
                    username=username,
                    ip_address=ip_address,
                    error_message="Invalid password"
                )
            
            raise AuthenticationError("Invalid username or password")
        
        # Authentication successful
        user.update_last_login()
        
        if ip_address:
            AuditLog.log_login(user=user, ip_address=ip_address)
        
        return user
    
    @staticmethod
    def change_password(user, old_password, new_password):
        """
        Change user password
        
        Args:
            user: User object
            old_password: Current password
            new_password: New password
            
        Returns:
            True if password changed successfully
            
        Raises:
            AuthenticationError: If old password is incorrect
        """
        # Verify old password
        if not AuthService.verify_password(old_password, user.password_hash):
            raise AuthenticationError("Current password is incorrect")
        
        # Validate new password
        from app.utils.validators import validate_password_strength
        is_valid, error_message = validate_password_strength(new_password)
        if not is_valid:
            raise AuthenticationError(error_message)
        
        # Hash and update password
        user.password_hash = AuthService.hash_password(new_password)
        db.session.commit()
        
        # Log password change
        AuditLog.log_action(
            action='change_password',
            user=user,
            details='Password changed successfully'
        )
        
        return True
    
    @staticmethod
    def reset_password(user, new_password):
        """
        Reset user password (admin function)
        
        Args:
            user: User object
            new_password: New password
            
        Returns:
            True if password reset successfully
        """
        # Validate new password
        from app.utils.validators import validate_password_strength
        is_valid, error_message = validate_password_strength(new_password)
        if not is_valid:
            raise AuthenticationError(error_message)
        
        # Hash and update password
        user.password_hash = AuthService.hash_password(new_password)
        db.session.commit()
        
        # Log password reset
        AuditLog.log_action(
            action='reset_password',
            user=user,
            details='Password reset by admin'
        )
        
        return True

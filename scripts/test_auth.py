"""
Test authentication system
"""
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.extensions.database import db
from app.models.user import User
from app.services.auth_service import AuthService
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def test_auth():
    """Test authentication system"""
    print("Testing authentication system...\n")
    
    # Create app
    app = create_app(os.getenv('FLASK_ENV', 'development'))
    
    with app.app_context():
        # Check if admin exists
        admin = User.query.filter_by(username='admin').first()
        
        if not admin:
            print("❌ Admin user not found!")
            return
        
        print(f"✅ Admin user found: {admin.username}")
        print(f"   Email: {admin.email}")
        print(f"   Role: {admin.role}")
        print(f"   Active: {admin.is_active}")
        print(f"   Verified: {admin.is_verified}")
        print()
        
        # Test password verification
        print("Testing password verification...")
        test_password = "Admin@123"
        is_valid = AuthService.verify_password(test_password, admin.password_hash)
        
        if is_valid:
            print(f"✅ Password verification successful")
        else:
            print(f"❌ Password verification failed")
        print()
        
        # Test authentication
        print("Testing full authentication...")
        try:
            authenticated_user = AuthService.authenticate_user(
                username='admin',
                password=test_password,
                ip_address='127.0.0.1'
            )
            print(f"✅ Authentication successful: {authenticated_user.username}")
        except Exception as e:
            print(f"❌ Authentication failed: {str(e)}")
        print()
        
        # Check relationships
        print("Checking relationships...")
        try:
            print(f"   Created tests: {admin.created_tests.count()}")
            print(f"   Assignments: {admin.assignments.count()}")
            print(f"   Results: {admin.results.count()}")
            print(f"   Audit logs: {admin.audit_logs.count()}")
            print("✅ All relationships working")
        except Exception as e:
            print(f"❌ Relationship error: {str(e)}")


if __name__ == '__main__':
    test_auth()

"""
Create admin user
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


def create_admin_user():
    """Create default admin user"""
    print("Creating admin user...")
    
    # Create app
    app = create_app(os.getenv('FLASK_ENV', 'development'))
    
    with app.app_context():
        # Check if admin already exists
        existing_admin = User.query.filter_by(username='admin').first()
        
        if existing_admin:
            print("⚠️  Admin user already exists!")
            print(f"Username: {existing_admin.username}")
            print(f"Email: {existing_admin.email}")
            
            response = input("\nDo you want to reset the password? (yes/no): ")
            if response.lower() in ['yes', 'y']:
                new_password = input("Enter new password: ")
                AuthService.reset_password(existing_admin, new_password)
                print("✅ Admin password reset successfully!")
            return
        
        # Get admin details
        print("\n--- Admin User Creation ---")
        username = input("Enter admin username (default: admin): ") or "admin"
        email = input("Enter admin email (default: admin@testplatform.com): ") or "admin@testplatform.com"
        full_name = input("Enter admin full name (default: Administrator): ") or "Administrator"
        password = input("Enter admin password (default: Admin@123): ") or "Admin@123"
        
        # Hash password
        password_hash = AuthService.hash_password(password)
        
        # Create admin user
        admin = User(
            username=username,
            email=email,
            password_hash=password_hash,
            role='admin',
            full_name=full_name,
            is_active=True,
            is_verified=True
        )
        
        db.session.add(admin)
        db.session.commit()
        
        print("\n✅ Admin user created successfully!")
        print(f"\nUsername: {username}")
        print(f"Email: {email}")
        print(f"Password: {password}")
        print(f"\n⚠️  Please change the password after first login!")


if __name__ == '__main__':
    create_admin_user()

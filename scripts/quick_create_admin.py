"""
Quick create admin user without prompts
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


def quick_create_admin():
    """Create default admin user without prompts"""
    print("Creating admin user...")
    
    # Create app
    app = create_app(os.getenv('FLASK_ENV', 'development'))
    
    with app.app_context():
        # Check if admin already exists
        existing_admin = User.query.filter_by(username='admin').first()
        
        if existing_admin:
            print("✅ Admin user already exists!")
            print(f"Username: admin")
            print(f"Password: Admin@123")
            return
        
        # Hash password
        password_hash = AuthService.hash_password('Admin@123')
        
        # Create admin user
        admin = User(
            username='admin',
            email='admin@testplatform.com',
            password_hash=password_hash,
            role='admin',
            full_name='Administrator',
            is_active=True,
            is_verified=True
        )
        
        db.session.add(admin)
        db.session.commit()
        
        print("\n✅ Admin user created successfully!")
        print(f"Username: admin")
        print(f"Password: Admin@123")
        print(f"\n⚠️  Please change the password after first login!")


if __name__ == '__main__':
    quick_create_admin()

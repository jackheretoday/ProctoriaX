"""
Fix admin user to set is_verified = True
"""
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.extensions.database import db
from app.models.user import User
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def fix_admin():
    """Fix admin user"""
    print("Fixing admin user...")
    
    # Create app
    app = create_app(os.getenv('FLASK_ENV', 'development'))
    
    with app.app_context():
        admin = User.query.filter_by(username='admin').first()
        
        if admin:
            admin.is_verified = True
            db.session.commit()
            print("✅ Admin user updated: is_verified = True")
        else:
            print("❌ Admin user not found")


if __name__ == '__main__':
    fix_admin()

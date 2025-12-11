"""
Initialize database
Creates all tables
"""
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.extensions.database import db
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def init_database():
    """Initialize database and create all tables"""
    print("Initializing database...")
    
    # Create app
    app = create_app(os.getenv('FLASK_ENV', 'development'))
    
    with app.app_context():
        # Drop all tables (caution!)
        print("Dropping existing tables...")
        db.drop_all()
        
        # Create all tables
        print("Creating tables...")
        db.create_all()
        
        print("✅ Database initialized successfully!")
        print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
        
        # Print table names
        print("\nCreated tables:")
        for table in db.metadata.tables:
            print(f"  - {table}")


if __name__ == '__main__':
    init_database()

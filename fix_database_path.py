"""
Fix Flask Database Path Issue
Ensures Flask app uses correct database path
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def fix_database_path():
    """Fix Flask database path issue"""
    try:
        print("Checking Flask database configuration...")
        
        from app import create_app
        from app.config import config_by_name
        
        # Check different environment configs
        for env_name in ['development', 'default']:
            config = config_by_name.get(env_name)
            if config:
                db_uri = config.SQLALCHEMY_DATABASE_URI
                print(f"{env_name} config DB URI: {db_uri}")
                
                # Check if the database file exists at that path
                if 'sqlite:///' in db_uri:
                    db_path = db_uri.replace('sqlite:///', '')
                    abs_path = os.path.abspath(db_path)
                    print(f"  Database path: {abs_path}")
                    print(f"  File exists: {os.path.exists(abs_path)}")
        
        # Create app and check actual database
        app = create_app()
        with app.app_context():
            print(f"\nApp database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
            
            # Try to access the database
            from app.extensions.database import db
            try:
                # Test connection
                db.engine.execute("SELECT 1")
                print("OK Database connection works")
                
                # Test TrafficLog model
                from app.models.traffic import TrafficLog
                count = TrafficLog.query.count()
                print(f"OK TrafficLog model works - {count} records")
                
                return True
                
            except Exception as e:
                print(f"X Database connection failed: {e}")
                
                # Try to fix the path
                current_uri = app.config['SQLALCHEMY_DATABASE_URI']
                if 'sqlite:///' in current_uri:
                    # Make the path absolute
                    db_path = current_uri.replace('sqlite:///', '')
                    if not os.path.isabs(db_path):
                        # Convert to absolute path
                        abs_path = os.path.abspath(db_path)
                        new_uri = f'sqlite:///{abs_path}'
                        print(f"Changing database URI to: {new_uri}")
                        app.config['SQLALCHEMY_DATABASE_URI'] = new_uri
                        
                        # Test again
                        try:
                            db.engine.execute("SELECT 1")
                            print("OK Database connection fixed!")
                            return True
                        except Exception as e2:
                            print(f"X Still failed: {e2}")
                
                return False
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    success = fix_database_path()
    if success:
        print("\nDatabase path issue resolved!")
    else:
        print("\nDatabase path issue persists")

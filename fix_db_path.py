"""
Fix Database Path Issue
This script fixes the database path problem
"""

def fix_database_path():
    """Fix the database path to use absolute path"""
    import os
    from os.path import join, dirname, abspath
    
    # Get the absolute path to the correct database
    base_dir = dirname(__file__)
    db_path = abspath(join(base_dir, 'instance', 'testing_platform.db'))
    
    print(f"Base directory: {base_dir}")
    print(f"Database path: {db_path}")
    print(f"Database exists: {os.path.exists(db_path)}")
    
    if os.path.exists(db_path):
        # Create a new database URI with absolute path
        db_uri = f"sqlite:///{db_path}"
        print(f"New database URI: {db_uri}")
        
        # Update the environment variable
        os.environ['DATABASE_URI'] = db_uri
        print("Set DATABASE_URI environment variable")
        
        return db_uri
    else:
        print("Database file not found!")
        return None

if __name__ == "__main__":
    fix_database_path()

"""
Check All Database Files
This script checks all database files to find the correct one
"""

def check_all_databases():
    """Check all database files to find the correct one"""
    import sqlite3
    from os.path import join, dirname
    
    db_files = [
        'instance/app.db',
        'instance/testing_platform.db', 
        'tests.db'
    ]
    
    base_path = dirname(__file__)
    
    for db_file in db_files:
        full_path = join(base_path, db_file)
        print(f"\n=== Checking {db_file} ===")
        
        try:
            conn = sqlite3.connect(full_path)
            cursor = conn.cursor()
            
            # Get all tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            
            print(f"Tables: {[t[0] for t in tables]}")
            
            # Check if users table exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
            users_exists = cursor.fetchone()
            
            if users_exists:
                cursor.execute("SELECT COUNT(*) FROM users")
                user_count = cursor.fetchone()[0]
                print(f"Users: {user_count}")
                
                cursor.execute("SELECT id, username, role FROM users WHERE role = 'admin' LIMIT 1")
                admin_user = cursor.fetchone()
                if admin_user:
                    print(f"Admin: {admin_user}")
            
            # Check if user_sessions table exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user_sessions'")
            sessions_exists = cursor.fetchone()
            
            if sessions_exists:
                cursor.execute("SELECT COUNT(*) FROM user_sessions")
                session_count = cursor.fetchone()[0]
                print(f"Sessions: {session_count}")
            
            conn.close()
            
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    check_all_databases()

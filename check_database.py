"""
Check Database Tables
This script shows what tables exist in the database
"""

def check_database_tables():
    """Check what tables exist in the database"""
    try:
        import sqlite3
        from os.path import join, dirname
        
        # Find the database file
        db_path = join(dirname(__file__), 'instance', 'app.db')
        
        print(f"Checking tables in: {db_path}")
        
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print("Available tables:")
        for table in tables:
            print(f"  - {table[0]}")
        
        # Check if users table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        users_exists = cursor.fetchone()
        
        if users_exists:
            print("\nUsers table exists!")
            # Get user count
            cursor.execute("SELECT COUNT(*) FROM users")
            user_count = cursor.fetchone()[0]
            print(f"Total users: {user_count}")
            
            # Get admin users
            cursor.execute("SELECT id, username, role FROM users WHERE role = 'admin'")
            admin_users = cursor.fetchall()
            print(f"Admin users: {admin_users}")
        else:
            print("\nUsers table does not exist!")
        
        # Check user_sessions table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user_sessions'")
        sessions_exists = cursor.fetchone()
        
        if sessions_exists:
            print("User sessions table exists!")
            # Get session count
            cursor.execute("SELECT COUNT(*) FROM user_sessions")
            session_count = cursor.fetchone()[0]
            print(f"Total sessions: {session_count}")
        else:
            print("User sessions table does not exist!")
        
        conn.close()
        
    except Exception as e:
        print(f"Error checking database: {e}")

if __name__ == "__main__":
    check_database_tables()

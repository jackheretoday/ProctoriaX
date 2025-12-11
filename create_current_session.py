"""
Create Session for Current User
This script creates a session record for the currently logged-in user
"""

def create_current_user_session():
    """Create a session for the current logged-in user"""
    try:
        import sqlite3
        from datetime import datetime
        from os.path import join, dirname
        import uuid
        
        # Find the database file
        db_path = join(dirname(__file__), 'instance', 'app.db')
        
        print(f"Creating session for current user in: {db_path}")
        
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get the current user (assuming admin with ID 1)
        cursor.execute("SELECT id, username, role FROM users WHERE role = 'admin' LIMIT 1")
        user = cursor.fetchone()
        
        if user:
            user_id, username, role = user
            session_id = str(uuid.uuid4())
            ip_address = "127.0.0.1"  # Local
            
            # Create session record
            cursor.execute('''
                INSERT INTO user_sessions 
                (user_id, user_role, username, session_id, ip_address, login_time, last_activity, is_active)
                VALUES (?, ?, ?, ?, ?, ?, ?, 1)
            ''', (
                user_id, role, username, session_id, ip_address,
                datetime.utcnow(), datetime.utcnow()
            ))
            
            conn.commit()
            print(f"Created session for {username} ({role})")
            print(f"Session ID: {session_id}")
            print(f"Active users should now show: 1")
        else:
            print("No admin user found")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"Error creating session: {e}")
        return False

if __name__ == "__main__":
    create_current_user_session()

"""
Update Session in Correct Database
This script ensures the session is updated in the correct database
"""

def update_session_correct_db():
    """Update session in the correct database"""
    try:
        import sqlite3
        from datetime import datetime
        from os.path import join, dirname
        
        # Use the correct database
        db_path = join(dirname(__file__), 'instance', 'testing_platform.db')
        
        print(f"Updating session in correct database: {db_path}")
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Update the admin session to be recent
        cursor.execute("""
            UPDATE user_sessions 
            SET last_activity = datetime('now'),
                is_active = 1
            WHERE user_role = 'admin'
        """)
        
        # If no session exists, create one
        cursor.execute("SELECT changes()")
        changes = cursor.fetchone()[0]
        
        if changes == 0:
            print("No admin session found, creating one...")
            import uuid
            session_id = str(uuid.uuid4())
            
            cursor.execute("""
                INSERT INTO user_sessions 
                (user_id, user_role, username, session_id, ip_address, login_time, last_activity, is_active)
                VALUES (1, 'admin', 'admin', ?, '192.168.193.8', datetime('now'), datetime('now'), 1)
            """, (session_id,))
            print(f"Created new session: {session_id}")
        
        conn.commit()
        
        # Verify active users
        cursor.execute("""
            SELECT COUNT(*) FROM user_sessions 
            WHERE is_active = 1 AND last_activity >= datetime('now', '-5 minutes')
        """)
        active_count = cursor.fetchone()[0]
        
        print(f"Active users in correct database: {active_count}")
        
        # Show session details
        cursor.execute("""
            SELECT username, user_role, last_activity, is_active
            FROM user_sessions
        """)
        sessions = cursor.fetchall()
        
        print("Current sessions:")
        for session in sessions:
            username, role, last_activity, is_active = session
            print(f"  - {username} ({role}) - Active: {is_active} - Last: {last_activity}")
        
        conn.close()
        print("Session updated successfully!")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    update_session_correct_db()

"""
Check Active Sessions
This script checks the current active sessions in the correct database
"""

def check_active_sessions():
    """Check current active sessions"""
    try:
        import sqlite3
        from datetime import datetime
        from os.path import join, dirname
        
        # Use the correct database
        db_path = join(dirname(__file__), 'instance', 'testing_platform.db')
        
        print(f"Checking sessions in: {db_path}")
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check all sessions
        cursor.execute("""
            SELECT user_id, username, user_role, login_time, last_activity, is_active
            FROM user_sessions
        """)
        sessions = cursor.fetchall()
        
        print(f"\nAll sessions ({len(sessions)}):")
        for session in sessions:
            user_id, username, role, login_time, last_activity, is_active = session
            print(f"  - {username} ({role}) - Active: {is_active} - Last: {last_activity}")
        
        # Check active sessions in last 5 minutes
        five_minutes_ago = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("""
            SELECT COUNT(*) FROM user_sessions 
            WHERE is_active = 1 AND last_activity >= datetime('now', '-5 minutes')
        """)
        active_count = cursor.fetchone()[0]
        
        print(f"\nActive users in last 5 minutes: {active_count}")
        
        # Update your session to be recent
        cursor.execute("""
            UPDATE user_sessions 
            SET last_activity = datetime('now')
            WHERE user_role = 'admin' AND is_active = 1
        """)
        
        conn.commit()
        
        # Check again
        cursor.execute("""
            SELECT COUNT(*) FROM user_sessions 
            WHERE is_active = 1 AND last_activity >= datetime('now', '-5 minutes')
        """)
        new_active_count = cursor.fetchone()[0]
        
        print(f"Active users after update: {new_active_count}")
        
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_active_sessions()

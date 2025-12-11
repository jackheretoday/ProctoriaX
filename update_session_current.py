"""
Update Session to Current Time
This script updates the session to be current so it shows as active
"""

def update_session_current():
    """Update session to current time"""
    try:
        from app import create_app
        from app.extensions.database import db
        from sqlalchemy import text
        
        app = create_app()
        with app.app_context():
            # Update the admin session to be current
            db.session.execute(text("""
                UPDATE user_sessions 
                SET last_activity = datetime('now'),
                    is_active = 1
                WHERE user_role = 'admin'
            """))
            
            db.session.commit()
            
            # Verify the update
            result = db.session.execute(text("""
                SELECT COUNT(*) FROM user_sessions 
                WHERE is_active = 1 AND last_activity >= datetime('now', '-5 minutes')
            """)).scalar()
            
            print(f"Active users after update: {result}")
            
            # Show session details
            sessions = db.session.execute(text("""
                SELECT username, user_role, last_activity, is_active
                FROM user_sessions
            """)).fetchall()
            
            print("Current sessions:")
            for session in sessions:
                username, role, last_activity, is_active = session
                print(f"  - {username} ({role}) - Active: {is_active} - Last: {last_activity}")
            
            print("Session updated successfully!")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    update_session_current()

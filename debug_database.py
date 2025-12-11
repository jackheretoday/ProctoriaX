"""
Database Connection Debug
This script checks what database the application is actually using
"""

def debug_database_connection():
    """Debug which database the app is actually using"""
    try:
        from app import create_app
        from app.extensions.database import db
        from app.models.user_session import UserSession
        from app.models.user import User
        from sqlalchemy import text
        
        print("=== Database Connection Debug ===")
        
        # Create app and check database URI
        app = create_app()
        with app.app_context():
            print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
            
            # Test database connection
            try:
                # Try to query user_sessions
                result = db.session.execute(text("SELECT COUNT(*) FROM user_sessions")).scalar()
                print(f"User sessions count: {result}")
                
                # Try to query users
                result = db.session.execute(text("SELECT COUNT(*) FROM users")).scalar()
                print(f"Users count: {result}")
                
                # Check active users
                from datetime import datetime, timedelta
                since = datetime.utcnow() - timedelta(minutes=5)
                
                result = db.session.execute(
                    text("SELECT COUNT(*) FROM user_sessions WHERE is_active = 1 AND last_activity >= :since"), 
                    {"since": since}
                ).scalar()
                print(f"Active users (last 5 min): {result}")
                
                # Show session details
                sessions = db.session.execute(text("""
                    SELECT username, user_role, last_activity, is_active
                    FROM user_sessions
                """)).fetchall()
                
                print("Current sessions:")
                for session in sessions:
                    username, role, last_activity, is_active = session
                    print(f"  - {username} ({role}) - Active: {is_active} - Last: {last_activity}")
                
                # Test UserSession model directly
                try:
                    active_count = UserSession.get_active_user_count(minutes=5)
                    print(f"UserSession.get_active_user_count(): {active_count}")
                except Exception as e:
                    print(f"UserSession.get_active_user_count() error: {e}")
                
            except Exception as e:
                print(f"Database query error: {e}")
                
    except Exception as e:
        print(f"App creation error: {e}")

if __name__ == "__main__":
    debug_database_connection()

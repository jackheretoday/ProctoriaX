"""
Initialize User Session Tracking
This script ensures the user_sessions table exists and creates it if needed
"""

def init_user_sessions():
    """Initialize user session tracking"""
    try:
        from app import create_app
        from app.extensions.database import db
        from app.models.user_session import UserSession
        
        print("Initializing user session tracking...")
        
        app = create_app()
        with app.app_context():
            # Check if table exists
            if UserSession.__table__.exists(db.engine):
                print("UserSession table already exists")
            else:
                print("Creating UserSession table...")
                UserSession.__table__.create(db.engine)
                print("UserSession table created successfully")
            
            # Test the table
            try:
                count = UserSession.get_active_user_count(minutes=5)
                print(f"Current active users: {count}")
            except Exception as e:
                print(f"Error testing table: {e}")
            
            print("User session tracking initialized!")
            
    except Exception as e:
        print(f"Error initializing user sessions: {e}")

if __name__ == "__main__":
    init_user_sessions()

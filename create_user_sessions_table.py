"""
Create user_sessions table for proper active user tracking
"""
from app.extensions.database import db
from app.models.user_session import UserSession

def create_user_sessions_table():
    """Create the user_sessions table"""
    try:
        # Create the table
        UserSession.__table__.create(db.engine, checkfirst=True)
        print("Created user_sessions table successfully")
        return True
    except Exception as e:
        print(f"Error creating user_sessions table: {e}")
        return False

if __name__ == "__main__":
    from app import create_app
    
    app = create_app()
    with app.app_context():
        create_user_sessions_table()

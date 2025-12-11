"""
User Session Model
Tracks active user sessions for real-time monitoring
"""
from datetime import datetime, timedelta
from sqlalchemy import func, and_
from app.extensions.database import db

class UserSession(db.Model):
    """Track active user sessions"""
    __tablename__ = 'user_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # User information
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user_role = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    
    # Session tracking
    session_id = db.Column(db.String(255), nullable=False, unique=True)
    ip_address = db.Column(db.String(45), nullable=False)
    user_agent = db.Column(db.Text, nullable=True)
    
    # Timing
    login_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    last_activity = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    logout_time = db.Column(db.DateTime, nullable=True)
    
    # Status
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    def __repr__(self):
        return f'<UserSession {self.username} - {"Active" if self.is_active else "Inactive"}>'
    
    @classmethod
    def create_session(cls, user, session_id, ip_address, user_agent=None):
        """Create a new user session"""
        try:
            # Clean up any existing active sessions for this user
            cls.deactivate_user_sessions(user.id)
            
            # Create new session
            new_session = cls(
                user_id=user.id,
                user_role=user.role,
                username=user.username,
                session_id=session_id,
                ip_address=ip_address,
                user_agent=user_agent,
                login_time=datetime.utcnow(),
                last_activity=datetime.utcnow(),
                is_active=True
            )
            
            db.session.add(new_session)
            db.session.commit()
            
            print(f"✅ Created session for {user.username} ({user.role}) from {ip_address}")
            return new_session
            
        except Exception as e:
            print(f"❌ Error creating user session: {e}")
            db.session.rollback()
            return None
    
    @classmethod
    def update_activity(cls, user_id, session_id=None):
        """Update last activity time for user session"""
        try:
            query = cls.query.filter(
                cls.user_id == user_id,
                cls.is_active == True
            )
            
            if session_id:
                query = query.filter(cls.session_id == session_id)
            
            session = query.first()
            if session:
                session.last_activity = datetime.utcnow()
                db.session.commit()
                return True
            return False
            
        except Exception as e:
            print(f"❌ Error updating session activity: {e}")
            db.session.rollback()
            return False
    
    @classmethod
    def end_session(cls, user_id=None, session_id=None):
        """End user session(s)"""
        try:
            query = cls.query.filter(cls.is_active == True)
            
            if user_id:
                query = query.filter(cls.user_id == user_id)
            if session_id:
                query = query.filter(cls.session_id == session_id)
            
            sessions = query.all()
            
            for session in sessions:
                session.is_active = False
                session.logout_time = datetime.utcnow()
                print(f"🔴 Ended session for {session.username} ({session.user_role})")
            
            db.session.commit()
            return len(sessions)
            
        except Exception as e:
            print(f"❌ Error ending session: {e}")
            db.session.rollback()
            return 0
    
    @classmethod
    def deactivate_user_sessions(cls, user_id):
        """Deactivate all existing sessions for a user"""
        try:
            sessions = cls.query.filter(
                cls.user_id == user_id,
                cls.is_active == True
            ).all()
            
            for session in sessions:
                session.is_active = False
                session.logout_time = datetime.utcnow()
            
            db.session.commit()
            return len(sessions)
            
        except Exception as e:
            print(f"❌ Error deactivating user sessions: {e}")
            db.session.rollback()
            return 0
    
    @classmethod
    def get_active_users(cls, minutes=5):
        """Get currently active users (users with activity in last N minutes)"""
        since = datetime.utcnow() - timedelta(minutes=minutes)
        
        return db.session.query(
            cls.user_id,
            cls.username,
            cls.user_role,
            cls.ip_address,
            cls.login_time,
            cls.last_activity
        ).filter(
            cls.is_active == True,
            cls.last_activity >= since
        ).all()
    
    @classmethod
    def get_active_user_count(cls, minutes=5):
        """Get count of active users in last N minutes"""
        try:
            since = datetime.utcnow() - timedelta(minutes=minutes)
            
            print(f"Querying active users since {since}")
            
            # Simple query without table existence check
            # SQLAlchemy will handle missing table with an exception
            count = db.session.query(
                func.count(func.distinct(cls.user_id))
            ).filter(
                cls.is_active == True,
                cls.last_activity >= since
            ).scalar() or 0
            
            print(f"Found {count} active users in last {minutes} minutes")
            
            # Show details for debugging
            if count > 0:
                active_sessions = cls.query.filter(
                    cls.is_active == True,
                    cls.last_activity >= since
                ).all()
                print(f"Active sessions:")
                for session in active_sessions:
                    print(f"   - {session.username} ({session.user_role}) - Last activity: {session.last_activity}")
            else:
                print("No active sessions found")
            
            return count
            
        except Exception as e:
            print(f"Error in get_active_user_count: {e}")
            print("This likely means the user_sessions table doesn't exist yet")
            return 0
    
    @classmethod
    def get_active_users_by_role(cls, minutes=5):
        """Get active users grouped by role"""
        since = datetime.utcnow() - timedelta(minutes=minutes)
        
        return db.session.query(
            cls.user_role,
            func.count(func.distinct(cls.user_id)).label('count')
        ).filter(
            cls.is_active == True,
            cls.last_activity >= since
        ).group_by(cls.user_role).all()
    
    @classmethod
    def cleanup_expired_sessions(cls, hours=2):
        """Clean up sessions inactive for more than specified hours"""
        since = datetime.utcnow() - timedelta(hours=hours)
        
        expired_sessions = cls.query.filter(
            cls.is_active == True,
            cls.last_activity < since
        ).all()
        
        count = 0
        for session in expired_sessions:
            session.is_active = False
            session.logout_time = session.last_activity
            count += 1
        
        if count > 0:
            db.session.commit()
            print(f"🧹 Cleaned up {count} expired sessions")
        
        return count
    
    @classmethod
    def get_session_details(cls, user_id):
        """Get detailed session information for a user"""
        return cls.query.filter(
            cls.user_id == user_id,
            cls.is_active == True
        ).first()
    
    @classmethod
    def get_all_active_sessions(cls):
        """Get all currently active sessions"""
        return cls.query.filter(cls.is_active == True).all()
    
    def to_dict(self):
        """Convert session to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.username,
            'user_role': self.user_role,
            'ip_address': self.ip_address,
            'login_time': self.login_time.isoformat() if self.login_time else None,
            'last_activity': self.last_activity.isoformat() if self.last_activity else None,
            'logout_time': self.logout_time.isoformat() if self.logout_time else None,
            'is_active': self.is_active,
            'session_duration': str(datetime.utcnow() - self.login_time) if self.login_time else None
        }

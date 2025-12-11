"""
Traffic Analytics Model
Tracks real-time platform traffic and user activity
"""
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, and_
from app.extensions.database import db

class TrafficLog(db.Model):
    """Real-time traffic logging"""
    __tablename__ = 'traffic_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Request details
    ip_address = db.Column(db.String(45), nullable=False)  # IPv6 compatible
    user_agent = db.Column(db.Text, nullable=True)
    endpoint = db.Column(db.String(255), nullable=False)
    method = db.Column(db.String(10), nullable=False)
    status_code = db.Column(db.Integer, nullable=False)
    
    # User details (if authenticated)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    user_role = db.Column(db.String(20), nullable=True)
    
    # Timing
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    response_time = db.Column(db.Float, nullable=True)  # in milliseconds
    
    # Geographic data (optional)
    country = db.Column(db.String(100), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    
    # Session tracking
    session_id = db.Column(db.String(255), nullable=True)
    
    def __repr__(self):
        return f'<TrafficLog {self.method} {self.endpoint} - {self.status_code}>'
    
    @classmethod
    def log_request(cls, endpoint, method, status_code, ip_address, 
                   user_agent=None, user_id=None, user_role=None, 
                   response_time=None, session_id=None):
        """Log a new request"""
        try:
            log_entry = cls(
                endpoint=endpoint,
                method=method,
                status_code=status_code,
                ip_address=ip_address,
                user_agent=user_agent,
                user_id=user_id,
                user_role=user_role,
                response_time=response_time,
                session_id=session_id
            )
            db.session.add(log_entry)
            db.session.commit()
            return log_entry
        except Exception as e:
            db.session.rollback()
            print(f"Error logging traffic: {e}")
            return None
    
    @classmethod
    def get_real_time_stats(cls, minutes=1):
        """Get truly real-time statistics (current minute only)"""
        since = datetime.utcnow() - timedelta(seconds=30)  # Last 30 seconds for true real-time
        
        # Total requests in last 30 seconds
        total_requests = cls.query.filter(cls.timestamp >= since).count()
        
        # Requests per second (last 30 seconds) - SQLite compatible
        requests_per_second = db.session.query(
            func.strftime('%Y-%m-%d %H:%M:%S', cls.timestamp).label('second'),
            func.count(cls.id).label('count')
        ).filter(cls.timestamp >= since).group_by(func.strftime('%Y-%m-%d %H:%M:%S', cls.timestamp)).order_by('second').all()
        
        # Current active users (users who made requests in last 30 seconds)
        active_users = db.session.query(
            func.count(func.distinct(cls.user_id))
        ).filter(cls.timestamp >= since).filter(cls.user_id.isnot(None)).scalar() or 0
        
        # Status code distribution (last 30 seconds)
        status_distribution = db.session.query(
            cls.status_code,
            func.count(cls.id).label('count')
        ).filter(cls.timestamp >= since).group_by(cls.status_code).all()
        
        # User activity by role (last 30 seconds)
        user_activity = db.session.query(
            cls.user_role,
            func.count(cls.id).label('count')
        ).filter(cls.timestamp >= since).group_by(cls.user_role).all()
        
        # Top endpoints (last 30 seconds)
        top_endpoints = db.session.query(
            cls.endpoint,
            func.count(cls.id).label('count')
        ).filter(cls.timestamp >= since).group_by(cls.endpoint).order_by(
            func.count(cls.id).desc()
        ).limit(10).all()
        
        # Average response time (last 30 seconds)
        avg_response_time = db.session.query(
            func.avg(cls.response_time)
        ).filter(cls.timestamp >= since).filter(cls.response_time.isnot(None)).scalar()
        
        # Current requests per second rate
        current_rps = 0
        if requests_per_second:
            current_rps = sum(r.count for r in requests_per_second) / max(len(requests_per_second), 1)
        
        return {
            'total_requests': total_requests,
            'active_users': active_users,
            'current_rps': round(current_rps, 2),
            'requests_per_second': [(r.second, r.count) for r in requests_per_second],
            'status_distribution': [(s.status_code, s.count) for s in status_distribution],
            'user_activity': [(u.user_role or 'Anonymous', u.count) for u in user_activity],
            'top_endpoints': [(e.endpoint, e.count) for e in top_endpoints],
            'avg_response_time': round(avg_response_time or 0, 2)
        }
    
    @classmethod
    def get_live_requests(cls, limit=50):
        """Get the most recent requests for live monitoring"""
        return cls.query.order_by(cls.timestamp.desc()).limit(limit).all()
    
    @classmethod
    def get_current_activity(cls, seconds=60):
        """Get current activity in the last N seconds"""
        since = datetime.utcnow() - timedelta(seconds=seconds)
        
        return db.session.query(
            cls.endpoint,
            cls.method,
            cls.status_code,
            cls.user_role,
            cls.timestamp,
            cls.response_time,
            cls.ip_address
        ).filter(cls.timestamp >= since).order_by(cls.timestamp.desc()).all()
    
    @classmethod
    def get_hourly_traffic(cls, hours=24):
        """Get hourly traffic data for the last N hours"""
        since = datetime.utcnow() - timedelta(hours=hours)
        
        hourly_data = db.session.query(
            func.strftime('%Y-%m-%d %H:00:00', cls.timestamp).label('hour'),
            func.count(cls.id).label('count')
        ).filter(cls.timestamp >= since).group_by(func.strftime('%Y-%m-%d %H:00:00', cls.timestamp)).order_by('hour').all()
        
        return [(h.hour, h.count) for h in hourly_data]
    
    @classmethod
    def get_daily_summary(cls, days=7):
        """Get daily traffic summary for the last N days"""
        since = datetime.utcnow() - timedelta(days=days)
        
        daily_data = db.session.query(
            func.date(cls.timestamp).label('date'),
            func.count(cls.id).label('count'),
            func.count(func.distinct(cls.ip_address)).label('unique_ips'),
            func.count(func.distinct(cls.user_id)).label('unique_users')
        ).filter(cls.timestamp >= since).group_by('date').order_by('date').all()
        
        return [
            {
                'date': d.date,
                'requests': d.count,
                'unique_ips': d.unique_ips,
                'unique_users': d.unique_users
            }
            for d in daily_data
        ]
    
    @classmethod
    def get_endpoint_performance(cls, limit=20):
        """Get performance metrics for top endpoints"""
        subquery = cls.query(
            cls.endpoint,
            func.count(cls.id).label('request_count'),
            func.avg(cls.response_time).label('avg_response_time'),
            func.sum(func.case([(cls.status_code >= 400, 1)], else_=0)).label('error_count')
        ).filter(cls.timestamp >= datetime.utcnow() - timedelta(hours=24)).group_by(cls.endpoint)
        
        return db.session.query(
            subquery.c.endpoint,
            subquery.c.request_count,
            subquery.c.avg_response_time,
            subquery.c.error_count,
            (subquery.c.error_count.cast(db.Float) / subquery.c.request_count * 100).label('error_rate')
        ).order_by(subquery.c.request_count.desc()).limit(limit).all()
    
    @classmethod
    def cleanup_old_logs(cls, days=30):
        """Clean up logs older than N days"""
        cutoff = datetime.utcnow() - timedelta(days=days)
        deleted = cls.query.filter(cls.timestamp < cutoff).delete()
        db.session.commit()
        return deleted

class SystemMetrics(db.Model):
    """System performance metrics"""
    __tablename__ = 'system_metrics'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Metrics
    cpu_usage = db.Column(db.Float, nullable=True)
    memory_usage = db.Column(db.Float, nullable=True)
    disk_usage = db.Column(db.Float, nullable=True)
    active_connections = db.Column(db.Integer, default=0)
    
    # Database metrics
    db_connections = db.Column(db.Integer, default=0)
    db_query_time = db.Column(db.Float, nullable=True)
    
    # Timestamp
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    @classmethod
    def record_metrics(cls, cpu=None, memory=None, disk=None, 
                      active_connections=None, db_connections=None, db_query_time=None):
        """Record system metrics"""
        try:
            metrics = cls(
                cpu_usage=cpu,
                memory_usage=memory,
                disk_usage=disk,
                active_connections=active_connections,
                db_connections=db_connections,
                db_query_time=db_query_time
            )
            db.session.add(metrics)
            db.session.commit()
            return metrics
        except Exception as e:
            db.session.rollback()
            print(f"Error recording metrics: {e}")
            return None
    
    @classmethod
    def get_latest_metrics(cls):
        """Get the latest system metrics"""
        return cls.query.order_by(cls.timestamp.desc()).first()
    
    @classmethod
    def get_metrics_history(cls, hours=1):
        """Get metrics history for the last N hours"""
        since = datetime.utcnow() - timedelta(hours=hours)
        
        return cls.query.filter(cls.timestamp >= since).order_by(cls.timestamp.asc()).all()

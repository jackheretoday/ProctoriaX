"""
Traffic Analytics Service
Handles real-time traffic monitoring and analytics
"""
from datetime import datetime, timedelta
from flask import request, session
from sqlalchemy import func
from app.models.traffic import TrafficLog, SystemMetrics
from app.models.user_session import UserSession
from app.extensions.database import db
import psutil
import time

class TrafficService:
    """Service for traffic monitoring and analytics"""
    
    @staticmethod
    def log_request(response_time=None):
        """Log incoming request automatically"""
        try:
            # Get user info if authenticated
            from flask_login import current_user
            user_id = current_user.id if current_user.is_authenticated else None
            user_role = current_user.role if current_user.is_authenticated else None
            
            # Update user session activity if authenticated (with error handling)
            if user_id and session:
                try:
                    UserSession.update_activity(user_id, session.get('session_id'))
                except Exception as session_error:
                    # Silently handle session errors to avoid breaking the app
                    print(f"Session update failed: {session_error}")
                    pass  # Continue with request logging even if session fails
            
            # Log the request
            return TrafficLog.log_request(
                endpoint=request.endpoint or 'unknown',
                method=request.method,
                status_code=getattr(request, '_status_code', 200),
                ip_address=request.remote_addr,
                user_agent=request.headers.get('User-Agent'),
                user_id=user_id,
                user_role=user_role,
                response_time=response_time,
                session_id=session.get('session_id') if session else None
            )
        except Exception as e:
            print(f"Error in TrafficService.log_request: {e}")
            return None
    
    @staticmethod
    def get_dashboard_data():
        """Get comprehensive dashboard data"""
        return {
            'real_time': TrafficService.get_real_time_stats(),
            'hourly_traffic': TrafficService.get_hourly_traffic(),
            'daily_summary': TrafficService.get_daily_summary(),
            'endpoint_performance': TrafficService.get_endpoint_performance(),
            'system_metrics': TrafficService.get_system_metrics(),
            'user_activity': TrafficService.get_user_activity_trends()
        }
    
    @staticmethod
    def get_real_time_stats(minutes=5):
        """Get real-time statistics based on actual user sessions"""
        since = datetime.utcnow() - timedelta(seconds=30)  # Last 30 seconds for true real-time
        
        # Total requests in last 30 seconds
        total_requests = TrafficLog.query.filter(TrafficLog.timestamp >= since).count()
        
        # Requests per second (last 30 seconds) - SQLite compatible
        requests_per_second = db.session.query(
            func.strftime('%Y-%m-%d %H:%M:%S', TrafficLog.timestamp).label('second'),
            func.count(TrafficLog.id).label('count')
        ).filter(TrafficLog.timestamp >= since).group_by(func.strftime('%Y-%m-%d %H:%M:%S', TrafficLog.timestamp)).order_by('second').all()
        
        # Current active users (based on actual login sessions, not just requests)
        try:
            active_users = UserSession.get_active_user_count(minutes=5)  # Active in last 5 minutes
            print(f"👥 Real-time active users from sessions: {active_users}")
        except Exception as e:
            print(f"❌ Error getting session-based real-time active users: {e}")
            # Fallback to request-based counting if session tracking fails
            active_users = db.session.query(
                func.count(func.distinct(TrafficLog.user_id))
            ).filter(TrafficLog.timestamp >= since).filter(TrafficLog.user_id.isnot(None)).scalar() or 0
            print(f"🔄 Fallback real-time active users from requests: {active_users}")
        
        # Status code distribution (last 30 seconds)
        status_distribution = db.session.query(
            TrafficLog.status_code,
            func.count(TrafficLog.id).label('count')
        ).filter(TrafficLog.timestamp >= since).group_by(TrafficLog.status_code).all()
        
        # User activity by role (based on active sessions)
        try:
            user_activity = UserSession.get_active_users_by_role(minutes=5)
        except Exception as e:
            print(f"❌ Error getting session-based user activity: {e}")
            # Fallback to request-based activity
            user_activity = db.session.query(
                TrafficLog.user_role,
                func.count(TrafficLog.id).label('count')
            ).filter(TrafficLog.timestamp >= since).group_by(TrafficLog.user_role).all()
        
        # Top endpoints (last 30 seconds)
        top_endpoints = db.session.query(
            TrafficLog.endpoint,
            func.count(TrafficLog.id).label('count')
        ).filter(TrafficLog.timestamp >= since).group_by(TrafficLog.endpoint).order_by(
            func.count(TrafficLog.id).desc()
        ).limit(10).all()
        
        # Average response time (last 30 seconds)
        avg_response_time = db.session.query(
            func.avg(TrafficLog.response_time)
        ).filter(TrafficLog.timestamp >= since).filter(TrafficLog.response_time.isnot(None)).scalar()
        
        # Current requests per second rate
        current_rps = 0
        if requests_per_second:
            current_rps = sum(r.count for r in requests_per_second) / max(len(requests_per_second), 1)
        
        return {
            'total_requests': total_requests,
            'requests_per_second': requests_per_second,
            'current_rps': round(current_rps, 2),
            'active_users': active_users,  # Now based on actual login sessions with fallback
            'avg_response_time': round(avg_response_time or 0, 2),
            'status_distribution': status_distribution,
            'user_activity': user_activity,
            'top_endpoints': top_endpoints,
            'timestamp': datetime.utcnow().isoformat()
        }
    
    @staticmethod
    def get_current_stats():
        """Get current statistics for dashboard"""
        try:
            # Get active users (actual logged-in users)
            active_users = UserSession.get_active_user_count(minutes=5)
            print(f"👥 Real active users from sessions: {active_users}")
        except Exception as e:
            print(f"❌ Error getting session-based active users: {e}")
            # Fallback to request-based counting if session tracking fails
            since = datetime.utcnow() - timedelta(minutes=5)
            active_users = db.session.query(
                func.count(func.distinct(TrafficLog.user_id))
            ).filter(TrafficLog.timestamp >= since).filter(TrafficLog.user_id.isnot(None)).scalar() or 0
            print(f"🔄 Fallback active users from requests: {active_users}")
        
        # Get current requests per second
        since = datetime.utcnow() - timedelta(seconds=30)
        requests = TrafficLog.query.filter(TrafficLog.timestamp >= since).count()
        current_rps = requests / 30  # Divide by 30 seconds
        
        # Get average response time
        avg_response_time = db.session.query(
            func.avg(TrafficLog.response_time)
        ).filter(TrafficLog.timestamp >= since).filter(TrafficLog.response_time.isnot(None)).scalar() or 0
        
        # Get total requests today
        today = datetime.utcnow().date()
        total_requests = TrafficLog.query.filter(
            func.date(TrafficLog.timestamp) == today
        ).count()
        
        return {
            'active_users': active_users,  # Real active users with fallback
            'current_rps': round(current_rps, 2),
            'avg_response_time': round(avg_response_time, 2),
            'total_requests': total_requests
        }
    
    @staticmethod
    def get_hourly_traffic(hours=24):
        """Get hourly traffic data"""
        return TrafficLog.get_hourly_traffic(hours)
    
    @staticmethod
    def get_daily_summary(days=7):
        """Get daily summary"""
        return TrafficLog.get_daily_summary(days)
    
    @staticmethod
    def get_endpoint_performance(limit=20):
        """Get endpoint performance metrics"""
        performance = TrafficLog.get_endpoint_performance(limit)
        return [
            {
                'endpoint': p.endpoint,
                'requests': p.request_count,
                'avg_response_time': round(p.avg_response_time or 0, 2),
                'error_rate': round(p.error_rate or 0, 2),
                'errors': p.error_count
            }
            for p in performance
        ]
    
    @staticmethod
    def get_system_metrics():
        """Get current system metrics"""
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Memory usage
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            
            # Disk usage
            disk = psutil.disk_usage('/')
            disk_percent = (disk.used / disk.total) * 100
            
            # Active connections (approximate)
            active_connections = len(psutil.net_connections())
            
            # Active user sessions
            active_sessions = len(UserSession.get_all_active_sessions())
            
            return {
                'cpu_usage': round(cpu_percent, 2),
                'memory_usage': round(memory_percent, 2),
                'disk_usage': round(disk_percent, 2),
                'active_connections': active_connections,
                'active_sessions': active_sessions,
                'timestamp': datetime.utcnow().isoformat()
            }
        except Exception as e:
            print(f"Error getting system metrics: {e}")
            return {
                'cpu_usage': 0,
                'memory_usage': 0,
                'disk_usage': 0,
                'active_connections': 0,
                'active_sessions': 0,
                'timestamp': datetime.utcnow().isoformat()
            }
    
    @staticmethod
    def get_user_activity_trends(hours=24):
        """Get user activity trends"""
        since = datetime.utcnow() - timedelta(hours=hours)
        
        # Hourly activity by role - SQLite compatible
        hourly_activity = db.session.query(
            func.strftime('%Y-%m-%d %H:00:00', TrafficLog.timestamp).label('hour'),
            TrafficLog.user_role,
            func.count(TrafficLog.id).label('count')
        ).filter(TrafficLog.timestamp >= since).group_by(
            func.strftime('%Y-%m-%d %H:00:00', TrafficLog.timestamp), TrafficLog.user_role
        ).order_by('hour').all()
        
        # Error trends - SQLite compatible
        error_trends = db.session.query(
            func.strftime('%Y-%m-%d %H:00:00', TrafficLog.timestamp).label('hour'),
            func.count(TrafficLog.id).label('total_requests'),
            func.sum(func.case([(TrafficLog.status_code >= 400, 1)], else_=0)).label('errors')
        ).filter(TrafficLog.timestamp >= since).group_by(func.strftime('%Y-%m-%d %H:00:00', TrafficLog.timestamp)).order_by('hour').all()
        
        return {
            'hourly_activity': [
                {
                    'hour': str(item.hour),
                    'role': item.user_role or 'anonymous',
                    'count': item.count
                }
                for item in hourly_activity
            ],
            'error_trends': [
                {
                    'hour': str(item.hour),
                    'total_requests': item.total_requests,
                    'errors': item.errors or 0,
                    'error_rate': round((item.errors or 0) / max(item.total_requests, 1) * 100, 2)
                }
                for item in error_trends
            ]
        }
    
    @staticmethod
    def get_live_activity(limit=20):
        """Get live activity feed"""
        since = datetime.utcnow() - timedelta(minutes=5)
        
        activity = db.session.query(
            TrafficLog.endpoint,
            TrafficLog.method,
            TrafficLog.status_code,
            TrafficLog.user_role,
            TrafficLog.timestamp,
            TrafficLog.response_time,
            TrafficLog.ip_address
        ).filter(TrafficLog.timestamp >= since).order_by(TrafficLog.timestamp.desc()).limit(limit).all()
        
        return [
            {
                'endpoint': item.endpoint,
                'method': item.method,
                'status_code': item.status_code,
                'user_role': item.user_role or 'anonymous',
                'timestamp': item.timestamp.isoformat(),
                'response_time': round(item.response_time or 0, 2),
                'ip_address': item.ip_address
            }
            for item in activity
        ]
    
    @staticmethod
    def cleanup_old_data():
        """Clean up old traffic data"""
        try:
            # Clean up traffic logs older than 30 days
            cutoff_date = datetime.utcnow() - timedelta(days=30)
            deleted_logs = TrafficLog.query.filter(TrafficLog.timestamp < cutoff_date).delete()
            
            # Clean up expired user sessions
            expired_sessions = UserSession.cleanup_expired_sessions(hours=2)
            
            db.session.commit()
            
            print(f"🧹 Cleaned up {deleted_logs} old traffic logs and {expired_sessions} expired sessions")
            return True
            
        except Exception as e:
            print(f"❌ Error cleaning up old data: {e}")
            db.session.rollback()
            return False
            
            # Record metrics
            latest = SystemMetrics.record_metrics(
                cpu=cpu_percent,
                memory=memory_percent,
                disk=disk_percent,
                active_connections=active_connections
            )
            
            return {
                'cpu_usage': cpu_percent,
                'memory_usage': memory_percent,
                'disk_usage': disk_percent,
                'active_connections': active_connections,
                'timestamp': latest.timestamp if latest else datetime.utcnow()
            }
        except Exception as e:
            print(f"Error getting system metrics: {e}")
            return {
                'cpu_usage': 0,
                'memory_usage': 0,
                'disk_usage': 0,
                'active_connections': 0,
                'timestamp': datetime.utcnow()
            }
    
    @staticmethod
    def get_user_activity_trends(hours=24):
        """Get user activity trends by role"""
        since = datetime.utcnow() - timedelta(hours=hours)
        
        # Hourly activity by role - SQLite compatible
        hourly_activity = db.session.query(
            func.strftime('%Y-%m-%d %H:00:00', TrafficLog.timestamp).label('hour'),
            TrafficLog.user_role,
            func.count(TrafficLog.id).label('count')
        ).filter(TrafficLog.timestamp >= since).group_by(
            func.strftime('%Y-%m-%d %H:00:00', TrafficLog.timestamp), TrafficLog.user_role
        ).order_by('hour').all()
        
        # Organize data by role
        activity_by_role = {}
        for activity in hourly_activity:
            role = activity.user_role or 'Anonymous'
            if role not in activity_by_role:
                activity_by_role[role] = []
            activity_by_role[role].append({
                'hour': activity.hour,
                'count': activity.count
            })
        
        return activity_by_role
    
    @staticmethod
    def get_traffic_sources(hours=24):
        """Analyze traffic sources (IP ranges, user agents)"""
        since = datetime.utcnow() - timedelta(hours=hours)
        
        # Top IP ranges
        ip_ranges = db.session.query(
            func.substring(TrafficLog.ip_address, 1, 
                          func.case([
                              (func.position('.' in TrafficLog.ip_address) > 0, 
                               func.substring_index(TrafficLog.ip_address, '.', 3)),
                          ], else_=TrafficLog.ip_address)).label('ip_range'),
            func.count(TrafficLog.id).label('count')
        ).filter(TrafficLog.timestamp >= since).group_by('ip_range').order_by(
            func.count(TrafficLog.id).desc()
        ).limit(10).all()
        
        # Top user agents
        user_agents = db.session.query(
            func.substring(TrafficLog.user_agent, 1, 50).label('agent'),
            func.count(TrafficLog.id).label('count')
        ).filter(TrafficLog.timestamp >= since).filter(
            TrafficLog.user_agent.isnot(None)
        ).group_by('agent').order_by(func.count(TrafficLog.id).desc()).limit(10).all()
        
        return {
            'top_ip_ranges': [(ip.ip_range, ip.count) for ip in ip_ranges],
            'top_user_agents': [(ua.agent, ua.count) for ua in user_agents]
        }
    
    @staticmethod
    def get_error_analysis(hours=24):
        """Analyze errors and issues"""
        since = datetime.utcnow() - timedelta(hours=hours)
        
        # Error trends - SQLite compatible
        error_trends = db.session.query(
            func.strftime('%Y-%m-%d %H:00:00', TrafficLog.timestamp).label('hour'),
            func.count(TrafficLog.id).label('total_requests'),
            func.sum(func.case([(TrafficLog.status_code >= 400, 1)], else_=0)).label('errors')
        ).filter(TrafficLog.timestamp >= since).group_by(func.strftime('%Y-%m-%d %H:00:00', TrafficLog.timestamp)).order_by('hour').all()
        
        # Top error endpoints
        error_endpoints = db.session.query(
            TrafficLog.endpoint,
            TrafficLog.status_code,
            func.count(TrafficLog.id).label('count')
        ).filter(TrafficLog.timestamp >= since).filter(
            TrafficLog.status_code >= 400
        ).group_by(TrafficLog.endpoint, TrafficLog.status_code).order_by(
            func.count(TrafficLog.id).desc()
        ).limit(10).all()
        
        return {
            'trends': [
                {
                    'hour': t.hour,
                    'total_requests': t.total_requests,
                    'errors': t.errors,
                    'error_rate': round((t.errors / t.total_requests * 100) if t.total_requests > 0 else 0, 2)
                }
                for t in error_trends
            ],
            'top_error_endpoints': [
                {
                    'endpoint': e.endpoint,
                    'status_code': e.status_code,
                    'count': e.count
                }
                for e in error_endpoints
            ]
        }
    
    @staticmethod
    def cleanup_old_data(days=30):
        """Clean up old traffic data"""
        deleted_logs = TrafficLog.cleanup_old_logs(days)
        
        # Also clean up old system metrics
        cutoff = datetime.utcnow() - timedelta(days=days)
        deleted_metrics = SystemMetrics.query.filter(SystemMetrics.timestamp < cutoff).delete()
        db.session.commit()
        
        return {
            'deleted_logs': deleted_logs,
            'deleted_metrics': deleted_metrics
        }

class TrafficMiddleware:
    """Middleware to automatically log all requests"""
    
    def __init__(self, app=None):
        self.app = app
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize the middleware with Flask app"""
        app.before_request(self._before_request)
        app.after_request(self._after_request)
    
    def _before_request(self):
        """Called before each request"""
        request._start_time = time.time()
    
    def _after_request(self, response):
        """Called after each request"""
        try:
            # Calculate response time
            if hasattr(request, '_start_time'):
                response_time = (time.time() - request._start_time) * 1000  # Convert to milliseconds
                request._response_time = response_time
            
            # Store status code for logging
            request._status_code = response.status_code
            
            # Log the request asynchronously (don't block response)
            TrafficService.log_request(getattr(request, '_response_time', None))
            
        except Exception as e:
            print(f"Error in traffic middleware: {e}")
        
        return response

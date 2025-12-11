"""
Traffic Monitoring Initialization
Sets up the traffic monitoring system for the Flask application
"""

def init_traffic_monitoring(app):
    """Initialize traffic monitoring for the Flask app"""
    try:
        # Import and initialize the traffic middleware
        from app.services.traffic_service import TrafficMiddleware
        
        # Initialize the middleware
        traffic_middleware = TrafficMiddleware(app)
        
        print("Traffic monitoring middleware initialized")
        
        # Create traffic tables if they don't exist
        from migrations.traffic_monitoring import migrate
        migrate()
        
        print("Traffic monitoring system ready")
        
        return True
        
    except Exception as e:
        print(f"Error initializing traffic monitoring: {e}")
        return False

def setup_scheduled_tasks():
    """Set up scheduled tasks for traffic monitoring"""
    try:
        import threading
        import time
        from app.services.traffic_service import TrafficService
        
        def cleanup_task():
            """Background task to clean up old traffic data"""
            while True:
                try:
                    # Clean up data older than 30 days
                    result = TrafficService.cleanup_old_data(days=30)
                    print(f"Cleaned up {result['deleted_logs']} logs and {result['deleted_metrics']} metrics")
                    
                    # Sleep for 24 hours
                    time.sleep(24 * 60 * 60)
                    
                except Exception as e:
                    print(f"Error in cleanup task: {e}")
                    time.sleep(60 * 60)  # Retry in 1 hour
        
        # Start the cleanup task in a background thread
        cleanup_thread = threading.Thread(target=cleanup_task, daemon=True)
        cleanup_thread.start()
        
        print("Scheduled tasks initialized")
        return True
        
    except Exception as e:
        print(f"Error setting up scheduled tasks: {e}")
        return False

def generate_sample_data():
    """Generate sample traffic data for testing"""
    try:
        import random
        from datetime import datetime, timedelta
        from app.models.traffic import TrafficLog, SystemMetrics
        from app.extensions.database import db
        
        # Generate sample traffic logs for the last 24 hours
        endpoints = [
            'auth.login', 'auth.logout', 'teacher.dashboard', 'student.dashboard',
            'admin.dashboard', 'api.test_results', 'api.user_data', 'static.files'
        ]
        
        user_roles = ['student', 'teacher', 'admin', None]
        status_codes = [200, 200, 200, 200, 201, 302, 400, 404, 500]
        
        for hours_ago in range(24, 0, -1):
            for minute in range(60):
                # Generate 1-5 requests per minute
                for _ in range(random.randint(1, 5)):
                    timestamp = datetime.utcnow() - timedelta(hours=hours_ago, minutes=minute)
                    
                    log = TrafficLog(
                        endpoint=random.choice(endpoints),
                        method=random.choice(['GET', 'POST', 'PUT', 'DELETE']),
                        status_code=random.choice(status_codes),
                        ip_address=f"192.168.1.{random.randint(1, 254)}",
                        user_agent="Sample User Agent",
                        user_role=random.choice(user_roles),
                        response_time=random.uniform(50, 500),
                        timestamp=timestamp
                    )
                    db.session.add(log)
        
        # Generate sample system metrics
        for hours_ago in range(24, 0, -1):
            timestamp = datetime.utcnow() - timedelta(hours=hours_ago)
            
            metrics = SystemMetrics(
                cpu_usage=random.uniform(10, 80),
                memory_usage=random.uniform(30, 90),
                disk_usage=random.uniform(20, 70),
                active_connections=random.randint(5, 50),
                db_connections=random.randint(1, 10),
                timestamp=timestamp
            )
            db.session.add(metrics)
        
        db.session.commit()
        print("Sample traffic data generated")
        return True
        
    except Exception as e:
        print(f"Error generating sample data: {e}")
        db.session.rollback()
        return False

if __name__ == "__main__":
    import sys
    from app import create_app
    
    app = create_app()
    
    with app.app_context():
        # Initialize traffic monitoring
        init_traffic_monitoring(app)
        
        # Setup scheduled tasks
        setup_scheduled_tasks()
        
        # Generate sample data if requested
        if len(sys.argv) > 1 and sys.argv[1] == '--sample-data':
            generate_sample_data()
        
        print("Traffic monitoring system initialization complete!")

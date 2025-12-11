"""
Test Traffic Monitoring
Simple test script to verify traffic monitoring functionality
"""

def test_traffic_monitoring():
    """Test the traffic monitoring system"""
    print("Testing Traffic Monitoring System...")
    
    try:
        # Import the app
        from app import create_app
        app = create_app()
        
        with app.app_context():
            # Import models
            from app.models.traffic import TrafficLog, SystemMetrics
            from app.extensions.database import db
            
            # Create tables manually
            print("Creating traffic monitoring tables...")
            db.create_all()
            
            # Generate sample data
            print("Generating sample traffic data...")
            import random
            from datetime import datetime, timedelta
            
            # Sample traffic logs
            endpoints = ['auth.login', 'admin.dashboard', 'teacher.dashboard', 'student.dashboard']
            user_roles = ['student', 'teacher', 'admin', None]
            status_codes = [200, 200, 200, 201, 404, 500]
            
            for i in range(100):  # Generate 100 sample requests
                log = TrafficLog(
                    endpoint=random.choice(endpoints),
                    method=random.choice(['GET', 'POST']),
                    status_code=random.choice(status_codes),
                    ip_address=f"192.168.1.{random.randint(1, 254)}",
                    user_agent="Test Browser",
                    user_role=random.choice(user_roles),
                    response_time=random.uniform(50, 300),
                    timestamp=datetime.utcnow() - timedelta(minutes=random.randint(0, 60))
                )
                db.session.add(log)
            
            # Sample system metrics
            for i in range(24):  # 24 hours of data
                metrics = SystemMetrics(
                    cpu_usage=random.uniform(10, 80),
                    memory_usage=random.uniform(30, 90),
                    disk_usage=random.uniform(20, 70),
                    active_connections=random.randint(5, 50),
                    db_connections=random.randint(1, 10),
                    timestamp=datetime.utcnow() - timedelta(hours=i)
                )
                db.session.add(metrics)
            
            db.session.commit()
            
            # Test the service
            from app.services.traffic_service import TrafficService
            
            # Test real-time stats
            realtime = TrafficService.get_real_time_stats(minutes=5)
            print(f"Real-time stats: {realtime['total_requests']} requests")
            
            # Test system metrics
            system = TrafficService.get_system_metrics()
            print(f"System metrics: CPU {system['cpu_usage']}%, Memory {system['memory_usage']}%")
            
            # Test endpoint performance
            performance = TrafficService.get_endpoint_performance()
            print(f"Endpoint performance data for {len(performance)} endpoints")
            
            print("\nTraffic monitoring test completed successfully!")
            print("You can now access the admin dashboard at /admin/dashboard")
            
            return True
            
    except Exception as e:
        print(f"Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_traffic_monitoring()

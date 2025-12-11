"""
Generate Demo Traffic Data
Creates sample traffic data to demonstrate the real-time dashboard
"""

def generate_demo_traffic():
    """Generate demonstration traffic data"""
    try:
        from app import create_app
        from app.models.traffic import TrafficLog, SystemMetrics
        from app.extensions.database import db
        import random
        from datetime import datetime, timedelta
        
        app = create_app()
        
        with app.app_context():
            print("Generating demo traffic data...")
            
            # Clear existing demo data
            TrafficLog.query.delete()
            SystemMetrics.query.delete()
            db.session.commit()
            
            # Generate sample traffic logs for the last hour
            endpoints = [
                'auth.login', 'auth.logout', 'admin.dashboard', 'teacher.dashboard', 
                'student.dashboard', 'api.test_results', 'api.user_data', 'static.files'
            ]
            
            user_roles = ['student', 'teacher', 'admin', None]
            status_codes = [200, 200, 200, 200, 201, 302, 400, 404, 500]
            
            for minutes_ago in range(60, 0, -1):
                for seconds_ago in range(60):
                    # Generate 1-3 requests per minute
                    for _ in range(random.randint(1, 3)):
                        timestamp = datetime.utcnow() - timedelta(minutes=minutes_ago, seconds=seconds_ago)
                        
                        log = TrafficLog(
                            endpoint=random.choice(endpoints),
                            method=random.choice(['GET', 'POST', 'PUT', 'DELETE']),
                            status_code=random.choice(status_codes),
                            ip_address=f"192.168.1.{random.randint(1, 254)}",
                            user_agent="Demo Browser",
                            user_role=random.choice(user_roles),
                            response_time=random.uniform(50, 300),
                            timestamp=timestamp
                        )
                        db.session.add(log)
            
            # Generate recent activity (last 5 minutes) with more realistic data
            for minutes_ago in range(5, 0, -1):
                for seconds_ago in range(60):
                    # More activity in recent minutes
                    for _ in range(random.randint(2, 8)):
                        timestamp = datetime.utcnow() - timedelta(minutes=minutes_ago, seconds=seconds_ago)
                        
                        # Bias towards login/dashboard endpoints for recent activity
                        recent_endpoints = ['auth.login', 'admin.dashboard', 'teacher.dashboard', 'student.dashboard']
                        endpoint = random.choice(recent_endpoints + endpoints)
                        
                        log = TrafficLog(
                            endpoint=endpoint,
                            method=random.choice(['GET', 'POST']),
                            status_code=random.choice([200, 200, 200, 201, 302]),  # Mostly successful
                            ip_address=f"10.0.1.{random.randint(1, 254)}",
                            user_agent="Demo Browser",
                            user_role=random.choice(['student', 'teacher', 'admin']),
                            response_time=random.uniform(30, 150),  # Faster responses
                            timestamp=timestamp
                        )
                        db.session.add(log)
            
            # Generate system metrics for the last 24 hours
            for hours_ago in range(24, 0, -1):
                timestamp = datetime.utcnow() - timedelta(hours=hours_ago)
                
                metrics = SystemMetrics(
                    cpu_usage=random.uniform(15, 75),
                    memory_usage=random.uniform(35, 85),
                    disk_usage=random.uniform(25, 65),
                    active_connections=random.randint(8, 45),
                    db_connections=random.randint(2, 12),
                    timestamp=timestamp
                )
                db.session.add(metrics)
            
            db.session.commit()
            
            # Print summary
            total_logs = TrafficLog.query.count()
            total_metrics = SystemMetrics.query.count()
            recent_logs = TrafficLog.query.filter(
                TrafficLog.timestamp >= datetime.utcnow() - timedelta(minutes=5)
            ).count()
            
            print(f"✅ Demo data generated successfully!")
            print(f"   📊 Total traffic logs: {total_logs}")
            print(f"   🔧 System metrics: {total_metrics}")
            print(f"   ⚡ Recent activity (5 min): {recent_logs}")
            print(f"   🌐 Access dashboard at: /admin/dashboard")
            
            return True
            
    except Exception as e:
        print(f"❌ Error generating demo data: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    generate_demo_traffic()

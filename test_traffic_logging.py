"""
Test Traffic Logging
Simple test to verify traffic logging is working
"""

def test_traffic_logging():
    """Test if traffic logging is working"""
    try:
        from app import create_app
        from app.models.traffic import TrafficLog
        from app.extensions.database import db
        from datetime import datetime, timedelta
        
        app = create_app()
        
        with app.app_context():
            # Check if we can query traffic logs
            recent_logs = TrafficLog.query.filter(
                TrafficLog.timestamp >= datetime.utcnow() - timedelta(minutes=5)
            ).all()
            
            print(f"Found {len(recent_logs)} traffic logs in last 5 minutes")
            
            if recent_logs:
                print("Recent traffic:")
                for log in recent_logs[-5:]:  # Show last 5
                    print(f"  {log.timestamp} - {log.method} {log.endpoint} - {log.user_role} - {log.status_code}")
            else:
                print("No recent traffic logs found")
                
                # Let's create a test log entry
                print("Creating test log entry...")
                test_log = TrafficLog.log_request(
                    endpoint='test.endpoint',
                    method='GET',
                    status_code=200,
                    ip_address='127.0.0.1',
                    user_agent='Test Browser',
                    user_role='admin',
                    response_time=100.0
                )
                
                if test_log:
                    print("✅ Test log entry created successfully")
                    print(f"   ID: {test_log.id}")
                    print(f"   Endpoint: {test_log.endpoint}")
                    print(f"   User Role: {test_log.user_role}")
                else:
                    print("❌ Failed to create test log entry")
            
            # Test the real-time stats function
            print("\nTesting real-time stats...")
            stats = TrafficLog.get_real_time_stats(minutes=1)
            print(f"Active users: {stats.get('active_users', 0)}")
            print(f"Total requests: {stats.get('total_requests', 0)}")
            print(f"Current RPS: {stats.get('current_rps', 0)}")
            
            return True
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_traffic_logging()

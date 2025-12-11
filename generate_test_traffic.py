"""
Test Traffic Generator
Creates test traffic to verify the system is working
"""

import sys
import os
import time
import requests
from datetime import datetime

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def generate_test_traffic():
    """Generate test traffic to verify the system"""
    try:
        print("Generating test traffic...")
        
        # Create a test log entry directly using the model
        from app import create_app
        from app.models.traffic import TrafficLog
        
        app = create_app()
        with app.app_context():
            print("Creating test traffic entries...")
            
            # Create multiple test entries with different users
            test_entries = [
                {
                    'endpoint': '/admin/dashboard',
                    'method': 'GET',
                    'status_code': 200,
                    'ip_address': '192.168.1.100',
                    'user_agent': 'Mozilla/5.0 (Test Browser)',
                    'user_id': 1,
                    'user_role': 'admin',
                    'response_time': 45.5
                },
                {
                    'endpoint': '/auth/login',
                    'method': 'POST',
                    'status_code': 302,
                    'ip_address': '192.168.1.101',
                    'user_agent': 'Mozilla/5.0 (Mobile Browser)',
                    'user_id': 2,
                    'user_role': 'student',
                    'response_time': 120.3
                },
                {
                    'endpoint': '/teacher/dashboard',
                    'method': 'GET',
                    'status_code': 200,
                    'ip_address': '192.168.1.102',
                    'user_agent': 'Mozilla/5.0 (Teacher Browser)',
                    'user_id': 3,
                    'user_role': 'teacher',
                    'response_time': 67.8
                }
            ]
            
            created_logs = []
            for i, entry in enumerate(test_entries):
                # Stagger the timestamps
                timestamp = datetime.utcnow()
                if i > 0:
                    timestamp = datetime.utcnow().replace(second=datetime.utcnow().second - i*10)
                
                log = TrafficLog.log_request(**entry)
                if log:
                    created_logs.append(log)
                    print(f"Created test entry {i+1}: {entry['endpoint']} by {entry['user_role']}")
                else:
                    print(f"Failed to create test entry {i+1}")
            
            # Test the real-time stats
            print("\nTesting real-time stats...")
            try:
                stats = TrafficLog.get_real_time_stats(minutes=1)
                print(f"Active users: {stats.get('active_users', 0)}")
                print(f"Total requests: {stats.get('total_requests', 0)}")
                print(f"Current RPS: {stats.get('current_rps', 0)}")
                print(f"Avg response time: {stats.get('avg_response_time', 0)}ms")
                
                # Show user activity
                user_activity = stats.get('user_activity', [])
                if user_activity:
                    print("User activity:")
                    for role, count in user_activity:
                        print(f"  {role}: {count} requests")
                        
                # Show top endpoints
                top_endpoints = stats.get('top_endpoints', [])
                if top_endpoints:
                    print("Top endpoints:")
                    for endpoint, count in top_endpoints[:3]:
                        print(f"  {endpoint}: {count} requests")
                        
            except Exception as e:
                print(f"Error testing stats: {e}")
            
            # Clean up test entries
            print("\nCleaning up test entries...")
            from app.extensions.database import db
            for log in created_logs:
                db.session.delete(log)
            db.session.commit()
            print(f"Cleaned up {len(created_logs)} test entries")
            
        print("\nTest traffic generation completed!")
        return True
        
    except Exception as e:
        print(f"Error generating test traffic: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = generate_test_traffic()
    if success:
        print("\nTest traffic successful - system should be working!")
        print("Now:")
        print("1. RESTART your Flask app")
        print("2. Open admin dashboard")
        print("3. Test logging in from another device")
    else:
        print("\nTest traffic failed - check the errors above")

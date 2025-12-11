"""
Initialize Traffic Monitoring - Simple Version
Creates the traffic_logs table and sets up traffic monitoring
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def init_traffic_monitoring():
    """Initialize traffic monitoring by creating the traffic_logs table"""
    try:
        from app import create_app
        from app.extensions.database import db
        from app.models.traffic import TrafficLog
        
        print("Initializing Traffic Monitoring System...")
        
        # Create Flask app
        app = create_app()
        
        with app.app_context():
            print("Creating traffic_logs table...")
            
            # Create the table
            db.create_all()
            
            # Check if table exists
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            if 'traffic_logs' in tables:
                print("traffic_logs table created successfully!")
                
                # Test creating a log entry
                print("Testing traffic log creation...")
                test_log = TrafficLog.log_request(
                    endpoint='system.init',
                    method='GET',
                    status_code=200,
                    ip_address='127.0.0.1',
                    user_agent='System Initialization',
                    user_role='system',
                    response_time=1.0
                )
                
                if test_log:
                    print(f"Test log entry created with ID: {test_log.id}")
                    
                    # Test querying
                    count = TrafficLog.query.count()
                    print(f"Total traffic logs: {count}")
                    
                    # Clean up test entry
                    db.session.delete(test_log)
                    db.session.commit()
                    print("Test entry cleaned up")
                else:
                    print("Failed to create test log entry")
                    
            else:
                print("traffic_logs table was not created")
                print(f"Available tables: {tables}")
                return False
                
        print("Traffic monitoring initialization complete!")
        return True
        
    except Exception as e:
        print(f"Error initializing traffic monitoring: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = init_traffic_monitoring()
    if success:
        print("\nTraffic monitoring is ready!")
        print("Restart your Flask app to start logging traffic")
        print("Visit /admin/dashboard to see real-time traffic data")
    else:
        print("\nTraffic monitoring initialization failed")
        print("Check the error messages above and fix any issues")

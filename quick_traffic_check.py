"""
Quick Traffic System Check
Simple verification that traffic system components are working
"""

import sys
import os
import sqlite3
from datetime import datetime, timedelta

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def quick_traffic_check():
    """Quick check of traffic system components"""
    print("=" * 50)
    print("QUICK TRAFFIC SYSTEM CHECK")
    print("=" * 50)
    
    # 1. Check database directly
    print("\n1. Direct Database Check:")
    try:
        db_path = "instance/testing_platform.db"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check recent records
        cursor.execute("SELECT COUNT(*) FROM traffic_logs")
        total = cursor.fetchone()[0]
        print(f"Total records: {total}")
        
        # Check records in last 2 minutes
        two_min_ago = (datetime.now() - timedelta(minutes=2)).isoformat()
        cursor.execute("SELECT COUNT(*) FROM traffic_logs WHERE timestamp >= ?", (two_min_ago,))
        recent = cursor.fetchone()[0]
        print(f"Records in last 2 minutes: {recent}")
        
        # Show most recent record
        cursor.execute("""
            SELECT endpoint, method, user_id, user_role, timestamp 
            FROM traffic_logs 
            ORDER BY timestamp DESC 
            LIMIT 1
        """)
        latest = cursor.fetchone()
        if latest:
            print(f"Latest: {latest[1]} {latest[0]} by {latest[3]} (ID: {latest[2]}) at {latest[4]}")
        else:
            print("No records found")
            
        conn.close()
        
    except Exception as e:
        print(f"Database error: {e}")
        return False
    
    # 2. Manual test record
    print("\n2. Creating Manual Test Record:")
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Insert a test record directly
        cursor.execute("""
            INSERT INTO traffic_logs 
            (ip_address, user_agent, endpoint, method, status_code, user_id, user_role, response_time, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            '127.0.0.1',
            'Manual Test',
            '/test/manual',
            'GET',
            200,
            1,
            'admin',
            25.5,
            datetime.now().isoformat()
        ))
        
        conn.commit()
        print("Created manual test record")
        
        # Verify it was created
        cursor.execute("SELECT COUNT(*) FROM traffic_logs WHERE endpoint = '/test/manual'")
        test_count = cursor.fetchone()[0]
        print(f"Test records found: {test_count}")
        
        # Clean up
        cursor.execute("DELETE FROM traffic_logs WHERE endpoint = '/test/manual'")
        conn.commit()
        print("Cleaned up test record")
        
        conn.close()
        
    except Exception as e:
        print(f"Manual test error: {e}")
        return False
    
    # 3. Check Flask app import
    print("\n3. Flask App Import Check:")
    try:
        # Set environment variable for database path
        os.environ['DATABASE_URI'] = f'sqlite:///{os.path.abspath(db_path)}'
        
        from app import create_app
        app = create_app()
        print("Flask app created successfully")
        
        with app.app_context():
            print("Flask app context created")
            
            # Check database URI
            db_uri = app.config.get('SQLALCHEMY_DATABASE_URI')
            print(f"Database URI: {db_uri}")
            
            # Try to import model
            from app.models.traffic import TrafficLog
            print("TrafficLog model imported")
            
            # Try to import service
            from app.services.traffic_service import TrafficService
            print("TrafficService imported")
            
    except Exception as e:
        print(f"Flask import error: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("CHECK COMPLETE")
    print("=" * 50)
    print("If all checks passed, the traffic system should work.")
    print("Next steps:")
    print("1. RESTART your Flask app")
    print("2. Open admin dashboard")
    print("3. Try logging in from another device")
    print("4. Check if 'Active Users' updates")
    
    return True

if __name__ == "__main__":
    success = quick_traffic_check()
    if success:
        print("\nTraffic system check PASSED!")
    else:
        print("\nTraffic system check FAILED!")

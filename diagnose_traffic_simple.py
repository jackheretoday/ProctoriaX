"""
Simple Traffic Monitoring Diagnostic Tool
Checks all aspects of traffic monitoring system
"""

import sys
import os
import sqlite3
from datetime import datetime, timedelta

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def diagnose_traffic_monitoring():
    """Comprehensive diagnosis of traffic monitoring system"""
    print("=" * 60)
    print("TRAFFIC MONITORING DIAGNOSTIC TOOL")
    print("=" * 60)
    
    issues_found = []
    
    # 1. Check database and table
    print("\n1. CHECKING DATABASE AND TABLE...")
    try:
        db_path = "instance/testing_platform.db"
        if not os.path.exists(db_path):
            issues_found.append("Database file does not exist")
            print(f"X Database not found at {db_path}")
        else:
            print(f"OK Database found at {db_path}")
            
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Check if traffic_logs table exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='traffic_logs'")
            if cursor.fetchone():
                print("OK traffic_logs table exists")
                
                # Check table structure
                cursor.execute("PRAGMA table_info(traffic_logs)")
                columns = cursor.fetchall()
                print(f"OK Table has {len(columns)} columns")
                
                # Check indexes
                cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='traffic_logs'")
                indexes = cursor.fetchall()
                print(f"OK Table has {len(indexes)} indexes")
                
                # Check recent records
                cursor.execute("SELECT COUNT(*) FROM traffic_logs")
                total_records = cursor.fetchone()[0]
                print(f"Total traffic records: {total_records}")
                
                # Check records in last 5 minutes
                five_min_ago = (datetime.utcnow() - timedelta(minutes=5)).isoformat()
                cursor.execute("SELECT COUNT(*) FROM traffic_logs WHERE timestamp >= ?", (five_min_ago,))
                recent_records = cursor.fetchone()[0]
                print(f"Records in last 5 minutes: {recent_records}")
                
                # Check records with users
                cursor.execute("SELECT COUNT(*) FROM traffic_logs WHERE user_id IS NOT NULL")
                user_records = cursor.fetchone()[0]
                print(f"Records with user info: {user_records}")
                
                # Show recent records
                if recent_records > 0:
                    cursor.execute("""
                        SELECT endpoint, method, status_code, user_id, user_role, timestamp 
                        FROM traffic_logs 
                        WHERE timestamp >= ? 
                        ORDER BY timestamp DESC 
                        LIMIT 5
                    """, (five_min_ago,))
                    recent = cursor.fetchall()
                    print("\nRecent traffic records:")
                    for record in recent:
                        print(f"  {record[5]} - {record[1]} {record[0]} - User: {record[3]} ({record[4]}) - {record[2]}")
                else:
                    print("WARNING: No recent traffic records found")
                    
            else:
                issues_found.append("traffic_logs table does not exist")
                print("X traffic_logs table does not exist")
                
            conn.close()
            
    except Exception as e:
        issues_found.append(f"Database error: {e}")
        print(f"X Database error: {e}")
    
    # 2. Check Flask app and models
    print("\n2. CHECKING FLASK APP AND MODELS...")
    try:
        from app import create_app
        from app.models.traffic import TrafficLog
        from app.services.traffic_service import TrafficService
        
        print("OK Flask app imports successful")
        
        app = create_app()
        with app.app_context():
            print("OK Flask app context created")
            
            # Test model
            try:
                count = TrafficLog.query.count()
                print(f"OK TrafficLog model works - total records: {count}")
            except Exception as e:
                issues_found.append(f"TrafficLog model error: {e}")
                print(f"X TrafficLog model error: {e}")
            
            # Test service
            try:
                stats = TrafficService.get_real_time_stats()
                print(f"OK TrafficService works - active users: {stats.get('active_users', 0)}")
            except Exception as e:
                issues_found.append(f"TrafficService error: {e}")
                print(f"X TrafficService error: {e}")
                
    except Exception as e:
        issues_found.append(f"Flask app error: {e}")
        print(f"X Flask app error: {e}")
    
    # 3. Create test traffic
    print("\n3. CREATING TEST TRAFFIC...")
    try:
        from app import create_app
        from app.models.traffic import TrafficLog
        
        app = create_app()
        with app.app_context():
            # Create a test log entry
            test_log = TrafficLog.log_request(
                endpoint='diagnostic.test',
                method='GET',
                status_code=200,
                ip_address='127.0.0.1',
                user_agent='Diagnostic Tool',
                user_id=1,
                user_role='admin',
                response_time=50.0
            )
            
            if test_log:
                print(f"OK Test log created with ID: {test_log.id}")
                
                # Test querying
                stats = TrafficLog.get_real_time_stats(minutes=1)
                print(f"OK Real-time stats after test: {stats.get('active_users', 0)} active users")
                
                # Clean up
                from app.extensions.database import db
                db.session.delete(test_log)
                db.session.commit()
                print("OK Test log cleaned up")
            else:
                issues_found.append("Failed to create test log")
                print("X Failed to create test log")
                
    except Exception as e:
        issues_found.append(f"Test traffic error: {e}")
        print(f"X Test traffic error: {e}")
    
    # 4. Summary
    print("\n" + "=" * 60)
    print("DIAGNOSTIC SUMMARY")
    print("=" * 60)
    
    if issues_found:
        print(f"X {len(issues_found)} issues found:")
        for i, issue in enumerate(issues_found, 1):
            print(f"  {i}. {issue}")
    else:
        print("OK No issues found - Traffic monitoring should be working!")
    
    # 5. Recommendations
    print("\n" + "=" * 60)
    print("RECOMMENDATIONS")
    print("=" * 60)
    
    if issues_found:
        print("Fix the issues above first")
    else:
        print("If traffic monitoring still doesn't work:")
        print("  1. RESTART your Flask app")
        print("  2. Check browser console for JavaScript errors")
        print("  3. Try the Debug button on admin dashboard")
        print("  4. Test with different browsers/incognito mode")
        print("  5. Check network requests in browser dev tools")
    
    return len(issues_found) == 0

if __name__ == "__main__":
    success = diagnose_traffic_monitoring()
    if success:
        print("\nTraffic monitoring diagnostics passed!")
    else:
        print("\nTraffic monitoring has issues - see above")

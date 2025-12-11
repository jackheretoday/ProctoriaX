"""
Direct Traffic Table Creation
Creates the traffic_logs table directly using SQL
"""

import sqlite3
import os

def create_traffic_table():
    """Create the traffic_logs table directly"""
    try:
        db_path = "instance/testing_platform.db"
        
        if not os.path.exists(db_path):
            print(f"Database not found at {db_path}")
            return False
            
        print(f"Connecting to database: {db_path}")
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if table already exists
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='traffic_logs'
        """)
        
        if cursor.fetchone():
            print("traffic_logs table already exists")
            
            # Show table structure
            cursor.execute("PRAGMA table_info(traffic_logs)")
            columns = cursor.fetchall()
            print("Table structure:")
            for col in columns:
                print(f"  {col}")
                
            conn.close()
            return True
        
        # Create the traffic_logs table
        print("Creating traffic_logs table...")
        
        create_table_sql = """
        CREATE TABLE traffic_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip_address VARCHAR(45),
            user_agent TEXT,
            endpoint VARCHAR(255),
            method VARCHAR(10),
            status_code INTEGER,
            user_id INTEGER,
            user_role VARCHAR(20),
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            response_time FLOAT,
            country VARCHAR(2),
            city VARCHAR(100),
            session_id VARCHAR(255),
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
        
        cursor.execute(create_table_sql)
        
        # Create indexes for better performance
        print("Creating indexes...")
        
        cursor.execute("CREATE INDEX idx_traffic_logs_timestamp ON traffic_logs(timestamp)")
        cursor.execute("CREATE INDEX idx_traffic_logs_user_id ON traffic_logs(user_id)")
        cursor.execute("CREATE INDEX idx_traffic_logs_endpoint ON traffic_logs(endpoint)")
        cursor.execute("CREATE INDEX idx_traffic_logs_status_code ON traffic_logs(status_code)")
        
        # Commit changes
        conn.commit()
        
        # Verify table was created
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='traffic_logs'")
        if cursor.fetchone():
            print("traffic_logs table created successfully!")
            
            # Show table structure
            cursor.execute("PRAGMA table_info(traffic_logs)")
            columns = cursor.fetchall()
            print("Table structure:")
            for col in columns:
                print(f"  {col}")
                
            # Test inserting a record
            print("Testing insert...")
            cursor.execute("""
                INSERT INTO traffic_logs 
                (ip_address, user_agent, endpoint, method, status_code, user_id, user_role, response_time)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, ('127.0.0.1', 'Test Agent', 'test.endpoint', 'GET', 200, None, None, 1.0))
            
            conn.commit()
            
            # Test querying
            cursor.execute("SELECT COUNT(*) FROM traffic_logs")
            count = cursor.fetchone()[0]
            print(f"Test record inserted. Total records: {count}")
            
            # Clean up test record
            cursor.execute("DELETE FROM traffic_logs WHERE endpoint = 'test.endpoint'")
            conn.commit()
            
            print("Test record cleaned up")
            
        else:
            print("Failed to create traffic_logs table")
            conn.close()
            return False
            
        conn.close()
        print("Traffic table creation complete!")
        return True
        
    except Exception as e:
        print(f"Error creating traffic table: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = create_traffic_table()
    if success:
        print("\nTraffic monitoring is ready!")
        print("Restart your Flask app to start logging traffic")
        print("Visit /admin/dashboard to see real-time traffic data")
    else:
        print("\nFailed to create traffic table")

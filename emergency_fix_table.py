"""
Emergency Fix: Create user_sessions table
This script directly creates the missing table to fix logout errors
"""

def create_user_sessions_table_emergency():
    """Create the user_sessions table immediately"""
    try:
        import sqlite3
        from os.path import join, dirname
        
        # Find the database file
        db_path = join(dirname(__file__), 'instance', 'app.db')
        
        print(f"Creating user_sessions table in: {db_path}")
        
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create the table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                user_role VARCHAR(20) NOT NULL,
                username VARCHAR(100) NOT NULL,
                session_id VARCHAR(255) UNIQUE NOT NULL,
                ip_address VARCHAR(45) NOT NULL,
                user_agent TEXT,
                login_time DATETIME NOT NULL,
                last_activity DATETIME NOT NULL,
                logout_time DATETIME,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        
        conn.commit()
        conn.close()
        
        print("✅ user_sessions table created successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error creating table: {e}")
        return False

if __name__ == "__main__":
    create_user_sessions_table_emergency()

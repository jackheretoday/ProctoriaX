"""
Database Migration: Add Traffic Monitoring Tables
Creates tables for real-time traffic analytics and system metrics
"""
from app.extensions.database import db
from app.models.traffic import TrafficLog, SystemMetrics

def create_traffic_tables():
    """Create traffic monitoring tables"""
    try:
        # Create tables
        TrafficLog.__table__.create(db.engine, checkfirst=True)
        SystemMetrics.__table__.create(db.engine, checkfirst=True)
        
        print("Traffic monitoring tables created successfully")
        return True
    except Exception as e:
        print(f"Error creating traffic tables: {e}")
        return False

def add_indexes():
    """Add performance indexes for traffic queries"""
    try:
        # Add indexes for better query performance
        with db.engine.connect() as conn:
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_traffic_logs_timestamp ON traffic_logs(timestamp);
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_traffic_logs_endpoint ON traffic_logs(endpoint);
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_traffic_logs_status_code ON traffic_logs(status_code);
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_traffic_logs_user_role ON traffic_logs(user_role);
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_system_metrics_timestamp ON system_metrics(timestamp);
            """)
        
        print("Performance indexes created successfully")
        return True
    except Exception as e:
        print(f"Error creating indexes: {e}")
        return False

def migrate():
    """Run the complete migration"""
    print("Starting traffic monitoring migration...")
    
    success = True
    success &= create_traffic_tables()
    success &= add_indexes()
    
    if success:
        print("Traffic monitoring migration completed successfully!")
    else:
        print("Migration failed. Please check the errors above.")
    
    return success

if __name__ == "__main__":
    migrate()

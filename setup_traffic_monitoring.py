"""
Setup Traffic Monitoring
Quick setup script to initialize the traffic monitoring system
"""

def main():
    """Main setup function"""
    print("Setting up Traffic Monitoring System...")
    
    try:
        # Import the app
        from app import create_app
        app = create_app()
        
        with app.app_context():
            # Create traffic tables
            from migrations.traffic_monitoring import migrate
            migrate()
            
            # Generate some sample data for testing
            from init_traffic_monitoring import generate_sample_data
            generate_sample_data()
            
            print("\nTraffic monitoring setup complete!")
            print("\nFeatures now available:")
            print("   • Real-time traffic monitoring")
            print("   • Live dashboard with charts")
            print("   • System performance metrics")
            print("   • Endpoint performance tracking")
            print("   • Error analysis and monitoring")
            print("   • User activity tracking")
            print("\nAccess the dashboard at: /admin/dashboard")
            print("Auto-refresh is enabled by default")
            
    except Exception as e:
        print(f"Setup failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()

"""
Development server entry point
Run with: python run.py
"""
import os
from app import create_app
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create Flask application
app = create_app(os.getenv('FLASK_ENV', 'development'))

if __name__ == '__main__':
    # Get configuration
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    
    print(f"\n{'='*60}")
    print(f"🚀 Testing Platform Server Starting...")
    print(f"{'='*60}")
    print(f"Environment: {os.getenv('FLASK_ENV', 'development')}")
    print(f"Server: http://{host}:{port}")
    print(f"Debug Mode: {debug}")
    print(f"{'='*60}\n")
    
    # Run the application
    app.run(
        host=host,
        port=port,
        debug=debug,
        use_reloader=debug
    )

"""
WSGI entry point for production deployment
Use with Gunicorn: gunicorn wsgi:app
"""
import os
from app import create_app
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create Flask application for production
app = create_app(os.getenv('FLASK_ENV', 'production'))

if __name__ == "__main__":
    app.run()

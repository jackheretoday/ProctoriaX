"""
AWS Elastic Beanstalk Entry Point
Beanstalk looks for 'application' in 'application.py' by default.
"""
import os
from app import create_app
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create Flask application for production
# This variable must be named 'application' for AWS Beanstalk
application = create_app(os.getenv('FLASK_ENV', 'production'))

if __name__ == "__main__":
    application.run()

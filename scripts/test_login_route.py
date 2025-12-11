"""
Test login route via Flask test client
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from dotenv import load_dotenv

load_dotenv()


def run():
    app = create_app(os.getenv('FLASK_ENV', 'development'))
    app.testing = True
    with app.test_client() as client:
        # GET login page
        r = client.get('/auth/login')
        print('GET /auth/login:', r.status_code)
        
        # POST login creds
        resp = client.post('/auth/login', data={
            'username': 'admin',
            'password': 'Admin@123',
            'remember': 'on'
        }, follow_redirects=False)
        print('POST /auth/login:', resp.status_code, resp.headers.get('Location'))
        
        # If redirected, follow once
        if resp.status_code in (301, 302, 303):
            follow = client.get(resp.headers['Location'])
            print('Follow redirect:', follow.status_code, follow.request.path)

if __name__ == '__main__':
    run()

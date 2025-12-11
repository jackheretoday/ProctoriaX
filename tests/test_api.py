"""Test API endpoints"""
import pytest
import json


class TestAuthAPI:
    """Test authentication endpoints"""
    
    def test_login(self, client, admin_user):
        """Test login endpoint"""
        response = client.post('/auth/login', data={
            'username': 'admin',
            'password': 'Admin@123'
        }, follow_redirects=True)
        
        assert response.status_code == 200
    
    def test_login_invalid(self, client):
        """Test login with invalid credentials"""
        response = client.post('/auth/login', data={
            'username': 'admin',
            'password': 'wrong'
        })
        
        assert b'Invalid' in response.data or response.status_code in [401, 302]


class TestAdminAPI:
    """Test admin endpoints"""
    
    def test_dashboard_requires_auth(self, client):
        """Test dashboard requires authentication"""
        response = client.get('/admin/dashboard')
        assert response.status_code in [302, 401, 403]
    
    def test_dashboard_authenticated(self, authenticated_admin):
        """Test dashboard with authentication"""
        response = authenticated_admin.get('/admin/dashboard')
        assert response.status_code == 200


class TestTeacherAPI:
    """Test teacher endpoints"""
    
    def test_requires_auth(self, client):
        """Test endpoints require authentication"""
        response = client.get('/teacher/dashboard')
        assert response.status_code in [302, 401, 403]


class TestStudentAPI:
    """Test student endpoints"""
    
    def test_requires_auth(self, client):
        """Test endpoints require authentication"""
        response = client.get('/student/dashboard')
        assert response.status_code in [302, 401, 403]
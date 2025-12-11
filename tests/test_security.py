"""Test security features"""
import pytest


class TestRBAC:
    """Test Role-Based Access Control"""
    
    def test_admin_access_only(self, authenticated_student):
        """Test students cannot access admin routes"""
        response = authenticated_student.get('/admin/dashboard')
        assert response.status_code in [403, 302]
    
    def test_teacher_access_only(self, authenticated_student):
        """Test students cannot access teacher routes"""
        response = authenticated_student.get('/teacher/dashboard')
        assert response.status_code in [403, 302]
    
    def test_student_access_only(self, authenticated_teacher):
        """Test teachers cannot access student routes"""
        response = authenticated_teacher.get('/student/dashboard')
        assert response.status_code in [403, 302]


class TestPasswordSecurity:
    """Test password security"""
    
    def test_password_not_stored_plaintext(self, admin_user):
        """Test passwords are not stored in plaintext"""
        assert admin_user.password_hash != 'Admin@123'
        assert len(admin_user.password_hash) > 50
    
    def test_password_complexity(self, db_session):
        """Test password complexity requirements"""
        from app.services.auth_service import AuthService
        
        # Weak password should fail
        with pytest.raises(Exception):
            AuthService.create_user(
                username='weak',
                email='weak@test.com',
                password='12345',
                full_name='Weak',
                role='student'
            )
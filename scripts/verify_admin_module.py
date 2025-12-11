"""
Admin Module Verification Script
Verifies all components of the admin module are properly integrated
"""
import sys
import os
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def check_file_exists(filepath, description):
    """Check if a file exists"""
    if os.path.exists(filepath):
        print(f"[OK] {description}: {filepath}")
        return True
    else:
        print(f"[MISSING] {description}: {filepath}")
        return False


def verify_admin_module():
    """Verify all admin module components"""
    print("=" * 70)
    print("ADMIN MODULE VERIFICATION")
    print("=" * 70)
    
    base_path = Path(__file__).parent.parent
    errors = []
    
    # 1. Check Services
    print("\n1. Checking Services...")
    service_files = [
        ('app/services/user_service.py', 'User Service'),
    ]
    
    for filepath, desc in service_files:
        if not check_file_exists(base_path / filepath, desc):
            errors.append(f"Missing: {filepath}")
    
    # 2. Check API Endpoints
    print("\n2. Checking API Endpoints...")
    api_files = [
        ('app/api/v1/admin.py', 'Admin API Blueprint'),
    ]
    
    for filepath, desc in api_files:
        if not check_file_exists(base_path / filepath, desc):
            errors.append(f"Missing: {filepath}")
    
    # 3. Check Templates
    print("\n3. Checking Templates...")
    template_files = [
        ('app/templates/admin/base_admin.html', 'Admin Base Template'),
        ('app/templates/admin/dashboard.html', 'Dashboard Template'),
        ('app/templates/admin/manage_users.html', 'Manage Users Template'),
        ('app/templates/admin/create_user.html', 'Create User Template'),
        ('app/templates/admin/assign_tests.html', 'Assign Tests Template'),
        ('app/templates/admin/manage_test_dates.html', 'Manage Test Dates Template'),
        ('app/templates/admin/system_logs.html', 'System Logs Template'),
    ]
    
    for filepath, desc in template_files:
        if not check_file_exists(base_path / filepath, desc):
            errors.append(f"Missing: {filepath}")
    
    # 4. Check Static Files
    print("\n4. Checking Static Files...")
    static_files = [
        ('app/static/css/admin.css', 'Admin CSS'),
        ('app/static/js/admin-dashboard.js', 'Admin Dashboard JS'),
        ('app/static/js/user-management.js', 'User Management JS'),
    ]
    
    for filepath, desc in static_files:
        if not check_file_exists(base_path / filepath, desc):
            errors.append(f"Missing: {filepath}")
    
    # 5. Check Integration
    print("\n5. Checking Integration...")
    
    # Check if admin blueprint is registered
    try:
        from app import create_app
        app = create_app('development')
        
        # Check if admin blueprint is registered
        admin_registered = any(bp.name == 'admin' for bp in app.blueprints.values())
        if admin_registered:
            print("[OK] Admin blueprint registered in app factory")
        else:
            print("[FAIL] Admin blueprint NOT registered in app factory")
            errors.append("Admin blueprint not registered")
        
        # Check if UserService is importable
        try:
            from app.services import UserService
            print("[OK] UserService is importable")
        except ImportError as e:
            print(f"[FAIL] UserService import failed: {e}")
            errors.append("UserService import failed")
        
        # Check middleware registration
        if hasattr(app, 'before_request_funcs') and app.before_request_funcs:
            print("[OK] Middleware registered")
        else:
            print("[FAIL] Middleware NOT registered")
            errors.append("Middleware not registered")
            
    except Exception as e:
        print(f"[FAIL] App initialization failed: {e}")
        errors.append(f"App initialization error: {e}")
    
    # 6. Summary
    print("\n" + "=" * 70)
    print("VERIFICATION SUMMARY")
    print("=" * 70)
    
    if errors:
        print(f"\n[FAILED] VERIFICATION FAILED - {len(errors)} error(s) found:")
        for error in errors:
            print(f"  - {error}")
        return False
    else:
        print("\n[SUCCESS] ALL CHECKS PASSED - Admin module is properly integrated!")
        return True


if __name__ == '__main__':
    success = verify_admin_module()
    sys.exit(0 if success else 1)

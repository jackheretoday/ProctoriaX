
import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

from app import create_app

def verify_admin_routes():
    app = create_app('testing')
    
    expected_routes = {
        'admin.manage_users': '/admin/manage-users',
        'admin.create_user': '/admin/create-user',
        'admin.system_logs': '/admin/system-logs',
        'admin.manage_test_dates': '/admin/manage-test-dates'
    }
    
    success = True
    
    print("Verifying Admin Routes:")
    found_routes = {}
    
    for rule in app.url_map.iter_rules():
        if rule.endpoint in expected_routes:
            found_routes[rule.endpoint] = rule.rule
            
    for endpoint, expected in expected_routes.items():
        actual = found_routes.get(endpoint)
        if actual == expected:
            print(f"[SUCCESS] {endpoint}: {actual}")
        else:
            print(f"[FAILURE] {endpoint}: Expected {expected}, found {actual}")
            success = False
            
    return success

if __name__ == '__main__':
    if verify_admin_routes():
        sys.exit(0)
    else:
        sys.exit(1)

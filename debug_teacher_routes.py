"""
Debug Teacher Routes
This script checks if teacher routes are properly registered
"""

def debug_teacher_routes():
    """Debug teacher route registration"""
    try:
        from app import create_app
        
        app = create_app()
        with app.app_context():
            print("=== Teacher Routes Debug ===")
            
            # Check if the blueprint is registered
            print("Registered blueprints:")
            for name, blueprint in app.blueprints.items():
                print(f"  - {name}: {blueprint.url_prefix}")
            
            # Check teacher routes specifically
            print("\nTeacher routes:")
            teacher_bp = app.blueprints.get('teacher')
            if teacher_bp:
                for rule in teacher_bp.deferred_functions:
                    print(f"  - Deferred: {rule}")
                
                # Try to access the routes
                print("\nTesting URL building:")
                try:
                    with app.test_request_context():
                        from flask import url_for
                        tests_url = url_for('teacher.manage_tests')
                        print(f"  ✅ teacher.manage_tests: {tests_url}")
                except Exception as e:
                    print(f"  ❌ teacher.manage_tests: {e}")
                
                try:
                    with app.test_request_context():
                        from flask import url_for
                        results_url = url_for('teacher.view_results')
                        print(f"  ✅ teacher.view_results: {results_url}")
                except Exception as e:
                    print(f"  ❌ teacher.view_results: {e}")
            else:
                print("  ❌ Teacher blueprint not found!")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_teacher_routes()

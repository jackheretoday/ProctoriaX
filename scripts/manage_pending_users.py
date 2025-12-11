"""
Manage Pending User Registrations
Approve or reject users waiting for admin approval
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.extensions.database import db
from app.models.user import User
from dotenv import load_dotenv

load_dotenv()


def list_pending_users():
    """List all pending users"""
    app = create_app(os.getenv('FLASK_ENV', 'development'))
    
    with app.app_context():
        pending = User.query.filter_by(is_active=False, is_deleted=False).all()
        
        if not pending:
            print("✅ No pending users!")
            return []
        
        print(f"\n📋 Pending Users ({len(pending)}):")
        print("=" * 80)
        
        for user in pending:
            print(f"\nID: {user.id}")
            print(f"Username: {user.username}")
            print(f"Email: {user.email}")
            print(f"Full Name: {user.full_name}")
            print(f"Role: {user.role}")
            print(f"Student ID: {user.student_id or 'N/A'}")
            print(f"Registered: {user.created_at}")
            print("-" * 80)
        
        return pending


def approve_user(username):
    """Approve a user by username"""
    app = create_app(os.getenv('FLASK_ENV', 'development'))
    
    with app.app_context():
        user = User.query.filter_by(username=username, is_deleted=False).first()
        
        if not user:
            print(f"❌ User '{username}' not found!")
            return False
        
        if user.is_active:
            print(f"ℹ️  User '{username}' is already active!")
            return True
        
        user.is_active = True
        db.session.commit()
        
        print(f"✅ User '{username}' approved successfully!")
        print(f"   Email: {user.email}")
        print(f"   Role: {user.role}")
        return True


def reject_user(username):
    """Reject/delete a user by username"""
    app = create_app(os.getenv('FLASK_ENV', 'development'))
    
    with app.app_context():
        user = User.query.filter_by(username=username, is_deleted=False).first()
        
        if not user:
            print(f"❌ User '{username}' not found!")
            return False
        
        # Soft delete
        user.is_deleted = True
        db.session.commit()
        
        print(f"❌ User '{username}' rejected and deleted!")
        return True


def approve_all():
    """Approve all pending users"""
    app = create_app(os.getenv('FLASK_ENV', 'development'))
    
    with app.app_context():
        pending = User.query.filter_by(is_active=False, is_deleted=False).all()
        
        if not pending:
            print("✅ No pending users to approve!")
            return
        
        count = 0
        for user in pending:
            user.is_active = True
            count += 1
        
        db.session.commit()
        print(f"✅ Approved {count} user(s)!")


def interactive_mode():
    """Interactive mode for managing users"""
    while True:
        print("\n" + "=" * 80)
        print("👥 PENDING USER MANAGEMENT")
        print("=" * 80)
        print("\nOptions:")
        print("  1. List pending users")
        print("  2. Approve user")
        print("  3. Reject user")
        print("  4. Approve all pending")
        print("  5. Exit")
        print()
        
        choice = input("Select option (1-5): ").strip()
        
        if choice == '1':
            list_pending_users()
        
        elif choice == '2':
            username = input("\nEnter username to approve: ").strip()
            if username:
                approve_user(username)
        
        elif choice == '3':
            username = input("\nEnter username to reject: ").strip()
            if username:
                confirm = input(f"Are you sure you want to reject '{username}'? (yes/no): ").strip().lower()
                if confirm == 'yes':
                    reject_user(username)
                else:
                    print("❌ Rejection cancelled.")
        
        elif choice == '4':
            pending = list_pending_users()
            if pending:
                confirm = input(f"\nApprove ALL {len(pending)} pending users? (yes/no): ").strip().lower()
                if confirm == 'yes':
                    approve_all()
                else:
                    print("❌ Bulk approval cancelled.")
        
        elif choice == '5':
            print("\n👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid option!")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'list':
            list_pending_users()
        
        elif command == 'approve' and len(sys.argv) > 2:
            approve_user(sys.argv[2])
        
        elif command == 'reject' and len(sys.argv) > 2:
            reject_user(sys.argv[2])
        
        elif command == 'approve-all':
            approve_all()
        
        else:
            print("Usage:")
            print("  python manage_pending_users.py              # Interactive mode")
            print("  python manage_pending_users.py list         # List pending users")
            print("  python manage_pending_users.py approve <username>")
            print("  python manage_pending_users.py reject <username>")
            print("  python manage_pending_users.py approve-all")
    else:
        interactive_mode()

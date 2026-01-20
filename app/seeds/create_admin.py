"""
Create an admin user for initial system access.
Run this after initializing the database.
"""
from app import create_app
from app.extensions import db
from app.models import User, UserRole
from app.auth.utils import hash_password

def create_admin_user():
    """Create the initial admin user."""
    app = create_app()
    
    with app.app_context():
        # Check if admin already exists
        existing_admin = User.query.filter_by(email='admin@cohortly.com').first()
        
        if existing_admin:
            print("⚠️  Admin user already exists!")
            print(f"Email: admin@cohortly.com")
            return
        
        # Create admin user
        admin = User(
            email='admin@cohortly.com',
            password_hash=hash_password('Admin@123'),
            full_name='System Administrator',
            phone='+1234567890',
            role=UserRole.ADMIN,
            is_active=True
        )
        
        db.session.add(admin)
        db.session.commit()
        
        print("✅ Admin user created successfully!")
        print("\n" + "="*50)
        print("Admin Login Credentials:")
        print("="*50)
        print(f"Email:    admin@cohortly.com")
        print(f"Password: Admin@123")
        print("="*50)
        print("\n⚠️  IMPORTANT: Change this password after first login!")
        print("\nYou can now run the server:")
        print("flask run")

if __name__ == '__main__':
    create_admin_user()

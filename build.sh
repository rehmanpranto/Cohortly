#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Initializing database..."
python -c "
from app import create_app, db
from app.models import User, UserRole
from app.auth.utils import hash_password
import os

app = create_app()

with app.app_context():
    try:
        # Create all tables
        db.create_all()
        print('✓ Database tables created successfully!')
        
        # Check if admin exists
        admin = User.query.filter_by(email='admin@cohortly.com').first()
        
        if not admin:
            # Create admin user
            admin = User(
                email='admin@cohortly.com',
                password=hash_password('Admin@123'),
                full_name='System Administrator',
                role=UserRole.ADMIN,
                is_active=True
            )
            db.session.add(admin)
            db.session.commit()
            print('✓ Admin user created: admin@cohortly.com / Admin@123')
        else:
            print('✓ Admin user already exists')
            
    except Exception as e:
        print(f'✗ Database initialization error: {e}')
        raise
"

echo "Build completed successfully!"

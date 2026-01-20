"""Check database users"""
from app import create_app
from app.models import User
from app.extensions import db

app = create_app()

with app.app_context():
    users = User.query.all()
    print(f'\n📊 Total users in database: {len(users)}\n')
    
    if users:
        for user in users:
            print(f'✓ Email: {user.email}')
            print(f'  Role: {user.role.value}')
            print(f'  Active: {user.is_active}')
            print(f'  Full Name: {user.full_name}')
            print(f'  Password Hash: {user.password_hash[:20]}...')
            print()
    else:
        print('❌ No users found in database!')
        print('   Run: python app/seeds/create_admin.py')

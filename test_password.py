"""Test password verification"""
from app import create_app
from app.models import User
from app.auth.utils import verify_password

app = create_app()

with app.app_context():
    user = User.query.filter_by(email='admin@cohortly.com').first()
    
    if user:
        print(f'\n✓ User found: {user.email}')
        print(f'  Password hash: {user.password_hash[:30]}...\n')
        
        # Test password
        test_password = 'Admin@123'
        result = verify_password(test_password, user.password_hash)
        
        print(f'Testing password: "{test_password}"')
        print(f'Result: {result}')
        
        if result:
            print('\n✅ Password verification WORKS!')
        else:
            print('\n❌ Password verification FAILED!')
            print('   The password hash might be incorrect.')
    else:
        print('❌ User not found!')

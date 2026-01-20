"""
Authentication routes
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import db
from app.models import User, UserRole
from app.auth.utils import hash_password, verify_password
from app.auth.forms import LoginForm, RegisterForm

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/')
def landing():
    """Landing page for unauthenticated users."""
    if current_user.is_authenticated:
        return redirect(url_for('auth.dashboard'))
    return render_template('shared/landing.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login route"""
    if current_user.is_authenticated:
        return redirect(url_for('auth.dashboard'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        email = form.email.data.lower().strip()
        password = form.password.data
        
        print(f"\n🔍 LOGIN ATTEMPT:")
        print(f"   Email: {email}")
        print(f"   Password length: {len(password)}")
        
        user = User.query.filter_by(email=email).first()
        print(f"   User found: {user is not None}")
        
        if user:
            password_valid = verify_password(password, user.password_hash)
            print(f"   Password valid: {password_valid}")
            print(f"   User active: {user.is_active}")
            
            if password_valid:
                if not user.is_active:
                    flash('Your account has been deactivated. Please contact support.', 'danger')
                    return render_template('auth/login.html', form=form)
                
                print(f"   ✅ Login successful! Logging in user...")
                login_user(user, remember=form.remember.data)
                flash(f'Welcome back, {user.full_name}!', 'success')
                
                # Redirect based on role
                next_page = request.args.get('next')
                if next_page:
                    return redirect(next_page)
                
                return redirect(url_for('auth.dashboard'))
        
        print(f"   ❌ Login failed!")
        flash('Invalid email or password.', 'danger')
    else:
        if form.errors:
            print(f"\n❌ FORM VALIDATION ERRORS:")
            for field, errors in form.errors.items():
                print(f"   {field}: {errors}")
    
    return render_template('auth/login.html', form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Register route - for students only"""
    if current_user.is_authenticated:
        return redirect(url_for('auth.dashboard'))
    
    form = RegisterForm()
    
    if form.validate_on_submit():
        email = form.email.data.lower().strip()
        
        # Check if user exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered. Please login.', 'warning')
            return redirect(url_for('auth.login'))
        
        # Create new user (students only via public registration)
        try:
            new_user = User(
                email=email,
                password_hash=hash_password(form.password.data),
                full_name=form.full_name.data,
                phone=form.phone.data,
                role=UserRole.STUDENT,
                is_active=True
            )
            
            db.session.add(new_user)
            db.session.commit()
            
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        
        except Exception as e:
            db.session.rollback()
            flash('Registration failed. Please try again.', 'danger')
            print(f"Registration error: {e}")
    
    return render_template('auth/register.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    """Logout route"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/dashboard')
@login_required
def dashboard():
    """Dashboard router - redirects to role-specific dashboard"""
    
    if current_user.role == UserRole.ADMIN:
        return redirect(url_for('analytics.admin_dashboard'))
    elif current_user.role == UserRole.SALES:
        return redirect(url_for('crm.sales_dashboard'))
    elif current_user.role == UserRole.INSTRUCTOR:
        return redirect(url_for('lms.instructor_dashboard'))
    elif current_user.role == UserRole.MENTOR:
        return redirect(url_for('lms.mentor_dashboard'))
    elif current_user.role == UserRole.STUDENT:
        return redirect(url_for('lms.student_dashboard'))
    else:
        flash('Invalid user role.', 'danger')
        return redirect(url_for('auth.login'))


@auth_bp.route('/profile')
@login_required
def profile():
    """User profile page"""
    return render_template('auth/profile.html', user=current_user)

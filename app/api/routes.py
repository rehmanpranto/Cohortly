"""
API Module for Mobile App Integration
RESTful API endpoints with JWT authentication
"""
from flask import Blueprint, request, jsonify
from flask_login import current_user
from functools import wraps
from datetime import datetime, timedelta
import jwt
import os
from app.extensions import db
from app.models import (
    User, UserRole, Bootcamp, Batch, Enrollment, EnrollmentStatus,
    Payment, PaymentStatus, ClassSchedule, Announcement, 
    StudentProfile, PortfolioItem, Certificate, Milestone, StudentMilestone,
    Lead, LeadStatus
)
from app.auth.utils import hash_password, check_password

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

# JWT Configuration
JWT_SECRET = os.environ.get('JWT_SECRET', 'your-secret-key-change-in-production')
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_HOURS = 24


def token_required(f):
    """Decorator to require valid JWT token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Get token from header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]  # Bearer <token>
            except IndexError:
                return jsonify({'error': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'error': 'Authentication token is missing'}), 401
        
        try:
            # Decode token
            data = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            current_user_id = data['user_id']
            current_user = db.session.get(User, current_user_id)
            
            if not current_user or not current_user.is_active:
                return jsonify({'error': 'Invalid or inactive user'}), 401
            
            # Pass user to the route
            return f(current_user, *args, **kwargs)
            
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
    
    return decorated


def generate_token(user_id):
    """Generate JWT token for user"""
    payload = {
        'user_id': str(user_id),
        'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


# =========================
# AUTHENTICATION ENDPOINTS
# =========================

@api_bp.route('/auth/login', methods=['POST'])
def login():
    """
    Login endpoint
    POST /api/v1/auth/login
    Body: {"email": "user@example.com", "password": "password"}
    Returns: {"token": "...", "user": {...}}
    """
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password required'}), 400
    
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not check_password(data['password'], user.password_hash):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    if not user.is_active:
        return jsonify({'error': 'Account is inactive'}), 403
    
    # Generate token
    token = generate_token(user.id)
    
    return jsonify({
        'token': token,
        'user': {
            'id': str(user.id),
            'email': user.email,
            'full_name': user.full_name,
            'role': user.role.value,
            'phone': user.phone_number,
            'is_active': user.is_active
        }
    }), 200


@api_bp.route('/auth/register', methods=['POST'])
def register():
    """
    Register new student
    POST /api/v1/auth/register
    Body: {"email": "...", "password": "...", "full_name": "...", "phone": "..."}
    """
    data = request.get_json()
    
    required_fields = ['email', 'password', 'full_name']
    if not all(data.get(field) for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Check if user exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 409
    
    try:
        user = User(
            email=data['email'],
            password_hash=hash_password(data['password']),
            full_name=data['full_name'],
            phone_number=data.get('phone'),
            role=UserRole.STUDENT,
            is_active=True
        )
        db.session.add(user)
        db.session.commit()
        
        token = generate_token(user.id)
        
        return jsonify({
            'token': token,
            'user': {
                'id': str(user.id),
                'email': user.email,
                'full_name': user.full_name,
                'role': user.role.value
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@api_bp.route('/auth/refresh', methods=['POST'])
@token_required
def refresh_token(current_user):
    """Refresh JWT token"""
    new_token = generate_token(current_user.id)
    return jsonify({'token': new_token}), 200


# =========================
# USER PROFILE ENDPOINTS
# =========================

@api_bp.route('/user/profile', methods=['GET'])
@token_required
def get_profile(current_user):
    """Get current user profile"""
    profile_data = {
        'id': str(current_user.id),
        'email': current_user.email,
        'full_name': current_user.full_name,
        'phone': current_user.phone_number,
        'role': current_user.role.value,
        'is_active': current_user.is_active,
        'created_at': current_user.created_at.isoformat()
    }
    
    # Add student profile if exists
    if current_user.role == UserRole.STUDENT:
        student_profile = StudentProfile.query.filter_by(user_id=current_user.id).first()
        if student_profile:
            profile_data['student_profile'] = {
                'linkedin_url': student_profile.linkedin_url,
                'github_url': student_profile.github_url,
                'portfolio_url': student_profile.portfolio_url,
                'bio': student_profile.bio
            }
    
    return jsonify(profile_data), 200


@api_bp.route('/user/profile', methods=['PUT'])
@token_required
def update_profile(current_user):
    """Update user profile"""
    data = request.get_json()
    
    try:
        if data.get('full_name'):
            current_user.full_name = data['full_name']
        if data.get('phone'):
            current_user.phone_number = data['phone']
        
        db.session.commit()
        
        return jsonify({'message': 'Profile updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# =========================
# BOOTCAMP ENDPOINTS
# =========================

@api_bp.route('/bootcamps', methods=['GET'])
def get_bootcamps():
    """Get all active bootcamps (public endpoint)"""
    bootcamps = Bootcamp.query.filter_by(is_active=True).all()
    
    return jsonify({
        'bootcamps': [{
            'id': str(bc.id),
            'title': bc.title,
            'description': bc.description,
            'mode': bc.mode,
            'price': float(bc.price),
            'duration_weeks': bc.duration_weeks,
            'created_at': bc.created_at.isoformat()
        } for bc in bootcamps]
    }), 200


@api_bp.route('/bootcamps/<bootcamp_id>', methods=['GET'])
def get_bootcamp_detail(bootcamp_id):
    """Get bootcamp details with batches"""
    bootcamp = db.session.get(Bootcamp, bootcamp_id)
    
    if not bootcamp:
        return jsonify({'error': 'Bootcamp not found'}), 404
    
    return jsonify({
        'id': str(bootcamp.id),
        'title': bootcamp.title,
        'description': bootcamp.description,
        'mode': bootcamp.mode,
        'price': float(bootcamp.price),
        'duration_weeks': bootcamp.duration_weeks,
        'batches': [{
            'id': str(batch.id),
            'name': batch.name,
            'start_date': batch.start_date.isoformat(),
            'end_date': batch.end_date.isoformat(),
            'is_active': batch.is_active
        } for batch in bootcamp.batches if batch.is_active]
    }), 200


# =========================
# ENROLLMENT ENDPOINTS
# =========================

@api_bp.route('/enrollments', methods=['GET'])
@token_required
def get_enrollments(current_user):
    """Get user's enrollments"""
    if current_user.role != UserRole.STUDENT:
        return jsonify({'error': 'Only students can view enrollments'}), 403
    
    enrollments = Enrollment.query.filter_by(student_id=current_user.id).all()
    
    return jsonify({
        'enrollments': [{
            'id': str(e.id),
            'batch': {
                'id': str(e.batch.id),
                'name': e.batch.name,
                'bootcamp': {
                    'id': str(e.batch.bootcamp.id),
                    'title': e.batch.bootcamp.title
                }
            },
            'status': e.status.value,
            'progress_percentage': e.progress_percentage,
            'enrolled_at': e.enrolled_at.isoformat(),
            'completed_at': e.completed_at.isoformat() if e.completed_at else None
        } for e in enrollments]
    }), 200


@api_bp.route('/enrollments/<enrollment_id>/progress', methods=['GET'])
@token_required
def get_enrollment_progress(current_user, enrollment_id):
    """Get detailed progress for an enrollment"""
    enrollment = db.session.get(Enrollment, enrollment_id)
    
    if not enrollment or enrollment.student_id != current_user.id:
        return jsonify({'error': 'Enrollment not found'}), 404
    
    bootcamp = enrollment.batch.bootcamp
    milestones = Milestone.query.filter_by(bootcamp_id=bootcamp.id).order_by(Milestone.order).all()
    student_milestones = {sm.milestone_id: sm for sm in enrollment.milestone_progress}
    
    return jsonify({
        'enrollment_id': str(enrollment.id),
        'progress_percentage': enrollment.progress_percentage,
        'bootcamp': {
            'id': str(bootcamp.id),
            'title': bootcamp.title,
            'duration_weeks': bootcamp.duration_weeks
        },
        'milestones': [{
            'id': str(m.id),
            'title': m.title,
            'description': m.description,
            'order': m.order,
            'percentage_weight': m.percentage_weight,
            'completed': student_milestones.get(m.id).completed if m.id in student_milestones else False,
            'completed_at': student_milestones.get(m.id).completed_at.isoformat() if m.id in student_milestones and student_milestones.get(m.id).completed_at else None
        } for m in milestones]
    }), 200


# =========================
# CLASS SCHEDULE ENDPOINTS
# =========================

@api_bp.route('/enrollments/<enrollment_id>/classes', methods=['GET'])
@token_required
def get_class_schedule(current_user, enrollment_id):
    """Get class schedule for enrollment"""
    enrollment = db.session.get(Enrollment, enrollment_id)
    
    if not enrollment or enrollment.student_id != current_user.id:
        return jsonify({'error': 'Enrollment not found'}), 404
    
    today = datetime.utcnow().date()
    
    upcoming_classes = ClassSchedule.query.filter_by(batch_id=enrollment.batch_id)\
        .filter(ClassSchedule.class_date >= today)\
        .order_by(ClassSchedule.class_date, ClassSchedule.class_time).all()
    
    past_classes = ClassSchedule.query.filter_by(batch_id=enrollment.batch_id)\
        .filter(ClassSchedule.class_date < today)\
        .order_by(ClassSchedule.class_date.desc(), ClassSchedule.class_time.desc())\
        .limit(10).all()
    
    return jsonify({
        'upcoming': [{
            'id': str(c.id),
            'week_number': c.week_number,
            'topic': c.topic,
            'description': c.description,
            'class_date': c.class_date.isoformat(),
            'class_time': c.class_time.strftime('%H:%M'),
            'duration_minutes': c.duration_minutes,
            'zoom_link': c.zoom_link,
            'zoom_meeting_id': c.zoom_meeting_id,
            'zoom_passcode': c.zoom_passcode
        } for c in upcoming_classes],
        'past': [{
            'id': str(c.id),
            'week_number': c.week_number,
            'topic': c.topic,
            'class_date': c.class_date.isoformat(),
            'recording_link': c.recording_link
        } for c in past_classes]
    }), 200


# =========================
# CERTIFICATE ENDPOINTS
# =========================

@api_bp.route('/enrollments/<enrollment_id>/certificate', methods=['GET'])
@token_required
def get_certificate(current_user, enrollment_id):
    """Get certificate for completed enrollment"""
    enrollment = db.session.get(Enrollment, enrollment_id)
    
    if not enrollment or enrollment.student_id != current_user.id:
        return jsonify({'error': 'Enrollment not found'}), 404
    
    if enrollment.progress_percentage < 100:
        return jsonify({'error': 'Course not completed yet'}), 403
    
    certificate = Certificate.query.filter_by(enrollment_id=enrollment_id).first()
    
    if not certificate:
        return jsonify({'error': 'Certificate not generated yet'}), 404
    
    return jsonify({
        'id': str(certificate.id),
        'verification_code': certificate.verification_code,
        'issued_at': certificate.issued_at.isoformat(),
        'certificate_url': certificate.certificate_url,
        'bootcamp': {
            'title': enrollment.batch.bootcamp.title,
            'duration_weeks': enrollment.batch.bootcamp.duration_weeks
        },
        'verification_url': f'/lms/certificate/verify/{certificate.verification_code}'
    }), 200


# =========================
# ANNOUNCEMENT ENDPOINTS
# =========================

@api_bp.route('/announcements', methods=['GET'])
@token_required
def get_announcements(current_user):
    """Get announcements for student's batches"""
    if current_user.role != UserRole.STUDENT:
        return jsonify({'announcements': []}), 200
    
    # Get student's batch IDs
    batch_ids = [e.batch_id for e in current_user.enrollments]
    
    announcements = Announcement.query.filter(
        Announcement.batch_id.in_(batch_ids)
    ).order_by(Announcement.created_at.desc()).limit(20).all()
    
    return jsonify({
        'announcements': [{
            'id': str(a.id),
            'title': a.title,
            'content': a.content,
            'priority': a.priority.value if hasattr(a, 'priority') else 'normal',
            'created_at': a.created_at.isoformat(),
            'author': {
                'name': a.author.full_name,
                'role': a.author.role.value
            }
        } for a in announcements]
    }), 200


# =========================
# PAYMENT ENDPOINTS
# =========================

@api_bp.route('/payments', methods=['GET'])
@token_required
def get_payments(current_user):
    """Get payment history"""
    if current_user.role != UserRole.STUDENT:
        return jsonify({'error': 'Only students can view payments'}), 403
    
    payments = Payment.query.join(Enrollment).filter(
        Enrollment.student_id == current_user.id
    ).order_by(Payment.created_at.desc()).all()
    
    return jsonify({
        'payments': [{
            'id': str(p.id),
            'amount': float(p.amount),
            'payment_method': p.payment_method,
            'status': p.status.value,
            'transaction_id': p.transaction_id,
            'paid_at': p.paid_at.isoformat() if p.paid_at else None,
            'bootcamp': p.enrollment.batch.bootcamp.title
        } for p in payments]
    }), 200


# =========================
# PORTFOLIO ENDPOINTS
# =========================

@api_bp.route('/portfolio', methods=['GET'])
@token_required
def get_portfolio(current_user):
    """Get user's portfolio items"""
    profile = StudentProfile.query.filter_by(user_id=current_user.id).first()
    
    if not profile:
        return jsonify({'portfolio_items': []}), 200
    
    items = PortfolioItem.query.filter_by(student_profile_id=profile.id)\
        .order_by(PortfolioItem.display_order, PortfolioItem.created_at.desc()).all()
    
    return jsonify({
        'portfolio_items': [{
            'id': str(item.id),
            'item_type': item.item_type.value,
            'title': item.title,
            'description': item.description,
            'github_url': item.github_url,
            'demo_url': item.demo_url,
            'image_url': item.image_url,
            'technologies': item.technologies,
            'is_featured': item.is_featured,
            'created_at': item.created_at.isoformat()
        } for item in items]
    }), 200


# =========================
# LEADS ENDPOINTS (For Marketing)
# =========================

@api_bp.route('/leads', methods=['POST'])
def create_lead():
    """Create a new lead (public endpoint)"""
    data = request.get_json()
    
    required_fields = ['full_name', 'email', 'phone']
    if not all(data.get(field) for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        lead = Lead(
            full_name=data['full_name'],
            email=data['email'],
            phone=data['phone'],
            source=data.get('source', 'Mobile App'),
            interested_bootcamp=data.get('interested_bootcamp'),
            status=LeadStatus.NEW
        )
        db.session.add(lead)
        db.session.commit()
        
        return jsonify({
            'message': 'Lead created successfully',
            'lead_id': str(lead.id)
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# =========================
# HEALTH CHECK
# =========================

@api_bp.route('/health', methods=['GET'])
def health_check():
    """API health check"""
    return jsonify({
        'status': 'healthy',
        'version': 'v1',
        'timestamp': datetime.utcnow().isoformat()
    }), 200

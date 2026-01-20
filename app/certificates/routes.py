"""
Certificates Module Routes
"""
from flask import Blueprint, render_template, abort, send_file
from app.models import Certificate, Enrollment
import uuid

certificates_bp = Blueprint('certificates', __name__)


@certificates_bp.route('/verify/<verification_code>')
def verify_certificate(verification_code):
    """Public certificate verification"""
    certificate = Certificate.query.filter_by(verification_code=verification_code).first()
    
    if not certificate:
        return render_template('shared/certificate_invalid.html'), 404
    
    enrollment = certificate.enrollment
    student = enrollment.student
    batch = enrollment.batch
    bootcamp = batch.bootcamp
    
    return render_template('shared/certificate_valid.html',
                         certificate=certificate,
                         student=student,
                         bootcamp=bootcamp,
                         batch=batch)


@certificates_bp.route('/generate/<uuid:enrollment_id>')
def generate_certificate(enrollment_id):
    """Generate certificate (requires completion)"""
    from flask_login import login_required, current_user
    from app.auth.utils import admin_required
    
    enrollment = Enrollment.query.get_or_404(enrollment_id)
    
    # Check if already has certificate
    if enrollment.certificate:
        return render_template('shared/certificate_exists.html', 
                             certificate=enrollment.certificate)
    
    # Check if completed
    if enrollment.status != 'completed':
        abort(400, 'Enrollment not completed')
    
    # Generate certificate
    try:
        verification_code = str(uuid.uuid4())[:8].upper()
        
        certificate = Certificate(
            enrollment_id=enrollment_id,
            verification_code=verification_code
        )
        
        from app.extensions import db
        db.session.add(certificate)
        db.session.commit()
        
        return render_template('shared/certificate_generated.html',
                             certificate=certificate)
    
    except Exception as e:
        return abort(500, f'Certificate generation failed: {str(e)}')

"""
LMS Module - Learning Management System Routes
"""
from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user
from app.models import UserRole, Enrollment, Batch, Bootcamp
from app.auth.utils import student_required, instructor_required, mentor_required

lms_bp = Blueprint('lms', __name__)


@lms_bp.route('/student/dashboard')
@student_required
def student_dashboard():
    """Student dashboard - show enrolled courses"""
    enrollments = Enrollment.query.filter_by(student_id=current_user.id).all()
    return render_template('student/dashboard.html', enrollments=enrollments)


@lms_bp.route('/instructor/dashboard')
@instructor_required
def instructor_dashboard():
    """Instructor dashboard - show assigned batches"""
    # Get batches where user is instructor
    from app.models import InstructorBatch
    instructor_batches = InstructorBatch.query.filter_by(instructor_id=current_user.id).all()
    batches = [ib.batch for ib in instructor_batches]
    return render_template('instructor/dashboard.html', batches=batches)


@lms_bp.route('/mentor/dashboard')
@mentor_required
def mentor_dashboard():
    """Mentor dashboard - show assigned batches"""
    from app.models import MentorBatch
    mentor_batches = MentorBatch.query.filter_by(mentor_id=current_user.id).all()
    batches = [mb.batch for mb in mentor_batches]
    return render_template('instructor/mentor_dashboard.html', batches=batches)


@lms_bp.route('/courses/<uuid:bootcamp_id>')
@login_required
def view_course(bootcamp_id):
    """View course details"""
    bootcamp = Bootcamp.query.get_or_404(bootcamp_id)
    return render_template('shared/course_detail.html', bootcamp=bootcamp)


@lms_bp.route('/batch/<uuid:batch_id>')
@login_required
def view_batch(batch_id):
    """View batch details and curriculum"""
    batch = Batch.query.get_or_404(batch_id)
    
    # Check if user has access
    if current_user.role == UserRole.STUDENT:
        enrollment = Enrollment.query.filter_by(
            student_id=current_user.id,
            batch_id=batch_id
        ).first()
        if not enrollment:
            abort(403)
    
    return render_template('student/batch_detail.html', batch=batch)


@lms_bp.route('/student/classes')
@student_required
def student_classes():
    """View all class schedules for enrolled batches"""
    from app.models import ClassSchedule
    from datetime import datetime
    
    # Get all enrollments for the student
    enrollments = Enrollment.query.filter_by(student_id=current_user.id).all()
    
    # Get all class schedules for these batches
    batch_ids = [e.batch_id for e in enrollments]
    
    # Get upcoming and past classes
    today = datetime.utcnow().date()
    upcoming_classes = ClassSchedule.query.filter(
        ClassSchedule.batch_id.in_(batch_ids),
        ClassSchedule.class_date >= today
    ).order_by(ClassSchedule.class_date, ClassSchedule.class_time).all()
    
    past_classes = ClassSchedule.query.filter(
        ClassSchedule.batch_id.in_(batch_ids),
        ClassSchedule.class_date < today
    ).order_by(ClassSchedule.class_date.desc(), ClassSchedule.class_time.desc()).limit(10).all()
    
    return render_template('student/classes.html', 
                         upcoming_classes=upcoming_classes,
                         past_classes=past_classes,
                         enrollments=enrollments)


@lms_bp.route('/batch/<uuid:batch_id>/classes')
@login_required
def batch_classes(batch_id):
    """View class schedule for a specific batch"""
    from app.models import ClassSchedule
    from datetime import datetime
    
    batch = Batch.query.get_or_404(batch_id)
    
    # Check access
    if current_user.role == UserRole.STUDENT:
        enrollment = Enrollment.query.filter_by(
            student_id=current_user.id,
            batch_id=batch_id
        ).first()
        if not enrollment:
            abort(403)
    
    # Get all class schedules
    today = datetime.utcnow().date()
    upcoming_classes = ClassSchedule.query.filter_by(batch_id=batch_id).filter(
        ClassSchedule.class_date >= today
    ).order_by(ClassSchedule.class_date, ClassSchedule.class_time).all()
    
    past_classes = ClassSchedule.query.filter_by(batch_id=batch_id).filter(
        ClassSchedule.class_date < today
    ).order_by(ClassSchedule.class_date.desc(), ClassSchedule.class_time.desc()).all()
    
    return render_template('student/batch_classes.html',
                         batch=batch,
                         upcoming_classes=upcoming_classes,
                         past_classes=past_classes)


@lms_bp.route('/student/progress/<uuid:enrollment_id>')
@student_required
def student_progress(enrollment_id):
    """View student progress with milestones"""
    from app.models import StudentMilestone, Milestone
    from app.extensions import db
    
    enrollment = Enrollment.query.get_or_404(enrollment_id)
    
    # Check access
    if enrollment.student_id != current_user.id:
        abort(403)
    
    # Get bootcamp milestones
    bootcamp = enrollment.batch.bootcamp
    milestones = Milestone.query.filter_by(bootcamp_id=bootcamp.id).order_by(Milestone.order).all()
    
    # Get student milestone completion
    student_milestones = {sm.milestone_id: sm for sm in enrollment.milestone_progress}
    
    # Calculate progress
    total_milestones = len(milestones)
    completed_milestones = sum(1 for sm in student_milestones.values() if sm.completed)
    progress_percentage = (completed_milestones / total_milestones * 100) if total_milestones > 0 else 0
    
    # Update enrollment progress
    enrollment.progress_percentage = int(progress_percentage)
    db.session.commit()
    
    return render_template('student/progress.html',
                         enrollment=enrollment,
                         bootcamp=bootcamp,
                         milestones=milestones,
                         student_milestones=student_milestones,
                         progress_percentage=progress_percentage,
                         completed_count=completed_milestones,
                         total_count=total_milestones)


@lms_bp.route('/student/certificate/<uuid:enrollment_id>')
@student_required
def view_certificate(enrollment_id):
    """View or generate certificate"""
    from app.models import Certificate
    from app.extensions import db
    import secrets
    
    enrollment = Enrollment.query.get_or_404(enrollment_id)
    
    # Check access
    if enrollment.student_id != current_user.id:
        abort(403)
    
    # Check if course is completed
    if enrollment.progress_percentage < 100:
        abort(403, description="Certificate not available. Complete all milestones first.")
    
    # Check if certificate already exists
    certificate = Certificate.query.filter_by(enrollment_id=enrollment_id).first()
    
    if not certificate:
        # Generate certificate
        verification_code = secrets.token_urlsafe(16).upper()
        certificate = Certificate(
            enrollment_id=enrollment_id,
            verification_code=verification_code
        )
        enrollment.completed_at = db.func.now()
        db.session.add(certificate)
        db.session.commit()
    
    return render_template('student/certificate.html',
                         certificate=certificate,
                         enrollment=enrollment,
                         bootcamp=enrollment.batch.bootcamp,
                         student=current_user)


@lms_bp.route('/certificate/verify/<verification_code>')
def verify_certificate(verification_code):
    """Public certificate verification"""
    from app.models import Certificate
    
    certificate = Certificate.query.filter_by(verification_code=verification_code).first()
    
    if not certificate:
        abort(404, description="Certificate not found")
    
    return render_template('public/verify_certificate.html',
                         certificate=certificate,
                         enrollment=certificate.enrollment,
                         bootcamp=certificate.enrollment.batch.bootcamp,
                         student=certificate.enrollment.student)


@lms_bp.route('/instructor/milestones/<uuid:bootcamp_id>')
@instructor_required
def manage_milestones(bootcamp_id):
    """Manage bootcamp milestones"""
    from app.models import Milestone
    
    bootcamp = Bootcamp.query.get_or_404(bootcamp_id)
    milestones = Milestone.query.filter_by(bootcamp_id=bootcamp_id).order_by(Milestone.order).all()
    
    return render_template('instructor/milestones.html',
                         bootcamp=bootcamp,
                         milestones=milestones)


@lms_bp.route('/instructor/milestone/create/<uuid:bootcamp_id>', methods=['GET', 'POST'])
@instructor_required
def create_milestone(bootcamp_id):
    """Create a new milestone"""
    from app.models import Milestone
    from app.extensions import db
    from flask import request, redirect, url_for, flash
    
    bootcamp = Bootcamp.query.get_or_404(bootcamp_id)
    
    if request.method == 'POST':
        try:
            milestone = Milestone(
                bootcamp_id=bootcamp_id,
                title=request.form['title'],
                description=request.form['description'],
                order=int(request.form['order']),
                percentage_weight=int(request.form['percentage_weight'])
            )
            db.session.add(milestone)
            db.session.commit()
            
            flash(f'Milestone "{milestone.title}" created successfully!', 'success')
            return redirect(url_for('lms.manage_milestones', bootcamp_id=bootcamp_id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating milestone: {str(e)}', 'danger')
    
    return render_template('instructor/create_milestone.html', bootcamp=bootcamp)


@lms_bp.route('/instructor/milestone/toggle/<uuid:enrollment_id>/<uuid:milestone_id>', methods=['POST'])
@instructor_required
def toggle_milestone(enrollment_id, milestone_id):
    """Toggle student milestone completion"""
    from app.models import StudentMilestone, Milestone
    from app.extensions import db
    from flask import request, jsonify
    from datetime import datetime
    
    enrollment = Enrollment.query.get_or_404(enrollment_id)
    milestone = Milestone.query.get_or_404(milestone_id)
    
    # Check if student milestone exists
    student_milestone = StudentMilestone.query.filter_by(
        enrollment_id=enrollment_id,
        milestone_id=milestone_id
    ).first()
    
    if not student_milestone:
        # Create new student milestone
        student_milestone = StudentMilestone(
            enrollment_id=enrollment_id,
            milestone_id=milestone_id,
            completed=True,
            completed_at=datetime.utcnow()
        )
        db.session.add(student_milestone)
    else:
        # Toggle completion
        student_milestone.completed = not student_milestone.completed
        student_milestone.completed_at = datetime.utcnow() if student_milestone.completed else None
    
    db.session.commit()
    
    # Recalculate progress
    total_milestones = Milestone.query.filter_by(bootcamp_id=milestone.bootcamp_id).count()
    completed_milestones = StudentMilestone.query.filter_by(
        enrollment_id=enrollment_id,
        completed=True
    ).count()
    
    progress_percentage = (completed_milestones / total_milestones * 100) if total_milestones > 0 else 0
    enrollment.progress_percentage = int(progress_percentage)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'completed': student_milestone.completed,
        'progress': progress_percentage
    })

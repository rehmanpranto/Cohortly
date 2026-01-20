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

"""
Student Lifecycle Management Routes
Centralized student profile and performance tracking
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from sqlalchemy import func, desc
from datetime import datetime, timedelta
from app.extensions import db
from app.models import (
    User, StudentProfile, PerformanceReview, Enrollment, Attendance,
    Grade, Submission, RAGRating, EnrollmentStatus, UserRole
)
from app.auth.utils import role_required

bp = Blueprint('student_lifecycle', __name__, url_prefix='/student-lifecycle')


@bp.route('/profile/<uuid:student_id>')
@login_required
@role_required([UserRole.ADMIN, UserRole.INSTRUCTOR, UserRole.MENTOR])
def view_profile(student_id):
    """View comprehensive student profile"""
    student = db.session.get(User, student_id)
    if not student:
        flash('Student not found', 'error')
        return redirect(url_for('analytics.admin_dashboard'))
    
    # Get or create profile
    profile = StudentProfile.query.filter_by(user_id=student_id).first()
    if not profile:
        profile = StudentProfile(user_id=student_id)
        db.session.add(profile)
        db.session.commit()
    
    # Get enrollments with progress
    enrollments = Enrollment.query.filter_by(student_id=student_id).all()
    
    # Calculate attendance
    total_sessions = 0
    attended_sessions = 0
    for enrollment in enrollments:
        attendance_records = Attendance.query.filter_by(enrollment_id=enrollment.id).all()
        total_sessions += len(attendance_records)
        attended_sessions += sum(1 for a in attendance_records if a.present)
    
    attendance_percentage = (attended_sessions / total_sessions * 100) if total_sessions > 0 else 0
    
    # Get recent grades
    recent_submissions = Submission.query.filter_by(student_id=student_id).order_by(desc(Submission.submitted_at)).limit(10).all()
    
    # Get performance reviews
    reviews = PerformanceReview.query.filter_by(student_profile_id=profile.id).order_by(desc(PerformanceReview.review_date)).all()
    
    # Calculate overall performance
    if recent_submissions:
        grades = [s.grade.score for s in recent_submissions if s.grade]
        avg_score = sum(grades) / len(grades) if grades else 0
    else:
        avg_score = 0
    
    # Update profile metrics
    profile.attendance_percentage = attendance_percentage
    profile.overall_performance_score = avg_score
    db.session.commit()
    
    return render_template('student_lifecycle/profile.html',
                         student=student,
                         profile=profile,
                         enrollments=enrollments,
                         attendance_percentage=attendance_percentage,
                         recent_submissions=recent_submissions,
                         reviews=reviews,
                         avg_score=avg_score)


@bp.route('/profile/<uuid:student_id>/edit', methods=['GET', 'POST'])
@login_required
@role_required([UserRole.ADMIN])
def edit_profile(student_id):
    """Edit student profile"""
    student = db.session.get(User, student_id)
    if not student:
        flash('Student not found', 'error')
        return redirect(url_for('analytics.admin_dashboard'))
    
    profile = StudentProfile.query.filter_by(user_id=student_id).first()
    if not profile:
        profile = StudentProfile(user_id=student_id)
        db.session.add(profile)
        db.session.commit()
    
    if request.method == 'POST':
        # Update profile
        profile.linkedin_url = request.form.get('linkedin_url', '').strip()
        profile.github_url = request.form.get('github_url', '').strip()
        profile.portfolio_url = request.form.get('portfolio_url', '').strip()
        profile.highest_education = request.form.get('highest_education', '').strip()
        profile.field_of_study = request.form.get('field_of_study', '').strip()
        profile.work_experience_years = int(request.form.get('work_experience_years', 0))
        profile.target_role = request.form.get('target_role', '').strip()
        profile.expected_salary = request.form.get('expected_salary', '').strip()
        profile.emergency_contact_name = request.form.get('emergency_contact_name', '').strip()
        profile.emergency_contact_phone = request.form.get('emergency_contact_phone', '').strip()
        profile.emergency_contact_relationship = request.form.get('emergency_contact_relationship', '').strip()
        
        db.session.commit()
        flash('Profile updated successfully', 'success')
        return redirect(url_for('student_lifecycle.view_profile', student_id=student_id))
    
    return render_template('student_lifecycle/edit_profile.html',
                         student=student,
                         profile=profile)


@bp.route('/performance-review/<uuid:student_id>', methods=['GET', 'POST'])
@login_required
@role_required([UserRole.ADMIN, UserRole.INSTRUCTOR])
def add_performance_review(student_id):
    """Add performance review for student"""
    student = db.session.get(User, student_id)
    if not student:
        flash('Student not found', 'error')
        return redirect(url_for('analytics.admin_dashboard'))
    
    profile = StudentProfile.query.filter_by(user_id=student_id).first()
    if not profile:
        flash('Student profile not found', 'error')
        return redirect(url_for('student_lifecycle.view_profile', student_id=student_id))
    
    if request.method == 'POST':
        rag_rating = request.form.get('rag_rating')
        
        review = PerformanceReview(
            student_profile_id=profile.id,
            reviewer_id=current_user.id,
            rag_rating=RAGRating[rag_rating.upper()],
            technical_skills=int(request.form.get('technical_skills', 5)),
            soft_skills=int(request.form.get('soft_skills', 5)),
            attendance=int(request.form.get('attendance', 5)),
            participation=int(request.form.get('participation', 5)),
            strengths=request.form.get('strengths', '').strip(),
            areas_for_improvement=request.form.get('areas_for_improvement', '').strip(),
            action_plan=request.form.get('action_plan', '').strip(),
            review_date=datetime.utcnow().date()
        )
        
        # Parse next review date if provided
        next_review = request.form.get('next_review_date')
        if next_review:
            review.next_review_date = datetime.strptime(next_review, '%Y-%m-%d').date()
        
        db.session.add(review)
        
        # Update profile RAG rating
        profile.current_rag_rating = review.rag_rating
        
        db.session.commit()
        
        flash('Performance review added successfully', 'success')
        return redirect(url_for('student_lifecycle.view_profile', student_id=student_id))
    
    return render_template('student_lifecycle/performance_review.html',
                         student=student,
                         profile=profile)


@bp.route('/at-risk-students')
@login_required
@role_required([UserRole.ADMIN, UserRole.INSTRUCTOR])
def at_risk_students():
    """View students who need intervention (RED rating)"""
    red_profiles = StudentProfile.query.filter_by(current_rag_rating=RAGRating.RED).all()
    amber_profiles = StudentProfile.query.filter_by(current_rag_rating=RAGRating.AMBER).all()
    
    # Get associated user data
    red_students = []
    for profile in red_profiles:
        user = db.session.get(User, profile.user_id)
        if user:
            red_students.append({
                'user': user,
                'profile': profile,
                'latest_review': PerformanceReview.query.filter_by(
                    student_profile_id=profile.id
                ).order_by(desc(PerformanceReview.review_date)).first()
            })
    
    amber_students = []
    for profile in amber_profiles:
        user = db.session.get(User, profile.user_id)
        if user:
            amber_students.append({
                'user': user,
                'profile': profile,
                'latest_review': PerformanceReview.query.filter_by(
                    student_profile_id=profile.id
                ).order_by(desc(PerformanceReview.review_date)).first()
            })
    
    return render_template('student_lifecycle/at_risk_students.html',
                         red_students=red_students,
                         amber_students=amber_students)


@bp.route('/dashboard')
@login_required
def student_dashboard():
    """Student's own comprehensive dashboard"""
    if current_user.role != UserRole.STUDENT:
        return redirect(url_for('analytics.admin_dashboard'))
    
    # Get or create profile
    profile = StudentProfile.query.filter_by(user_id=current_user.id).first()
    if not profile:
        profile = StudentProfile(user_id=current_user.id)
        db.session.add(profile)
        db.session.commit()
    
    # Get enrollments
    enrollments = Enrollment.query.filter_by(
        student_id=current_user.id,
        status=EnrollmentStatus.ACTIVE
    ).all()
    
    # Get recent performance review
    latest_review = PerformanceReview.query.filter_by(
        student_profile_id=profile.id
    ).order_by(desc(PerformanceReview.review_date)).first()
    
    return render_template('student_lifecycle/student_dashboard.html',
                         profile=profile,
                         enrollments=enrollments,
                         latest_review=latest_review)

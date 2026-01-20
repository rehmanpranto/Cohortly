"""
Career Support & Job Placement Routes
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from sqlalchemy import desc
from datetime import datetime
from app.extensions import db
from app.models import (
    StudentProfile, JobApplication, JobApplicationStatus,
    AlumniNetwork, User, UserRole
)
from app.auth.utils import role_required

bp = Blueprint('career', __name__, url_prefix='/career')


@bp.route('/dashboard')
@login_required
@role_required([UserRole.STUDENT])
def dashboard():
    """Student career dashboard"""
    profile = StudentProfile.query.filter_by(user_id=current_user.id).first()
    if not profile:
        profile = StudentProfile(user_id=current_user.id)
        db.session.add(profile)
        db.session.commit()
    
    applications = JobApplication.query.filter_by(
        student_profile_id=profile.id
    ).order_by(desc(JobApplication.applied_date)).all()
    
    # Calculate stats
    total_apps = len(applications)
    interviews = sum(1 for app in applications if app.status in [
        JobApplicationStatus.INTERVIEW, JobApplicationStatus.OFFER, JobApplicationStatus.ACCEPTED
    ])
    offers = sum(1 for app in applications if app.offer_received)
    
    return render_template('career/dashboard.html',
                         profile=profile,
                         applications=applications,
                         stats={'total': total_apps, 'interviews': interviews, 'offers': offers})


@bp.route('/applications/add', methods=['GET', 'POST'])
@login_required
@role_required([UserRole.STUDENT])
def add_application():
    """Add job application"""
    profile = StudentProfile.query.filter_by(user_id=current_user.id).first()
    if not profile:
        profile = StudentProfile(user_id=current_user.id)
        db.session.add(profile)
        db.session.commit()
    
    if request.method == 'POST':
        application = JobApplication(
            student_profile_id=profile.id,
            company_name=request.form.get('company_name').strip(),
            position=request.form.get('position').strip(),
            job_url=request.form.get('job_url', '').strip(),
            status=JobApplicationStatus.APPLIED,
            applied_date=datetime.strptime(request.form.get('applied_date'), '%Y-%m-%d').date(),
            notes=request.form.get('notes', '').strip()
        )
        
        db.session.add(application)
        db.session.commit()
        
        flash('Job application added successfully!', 'success')
        return redirect(url_for('career.dashboard'))
    
    return render_template('career/add_application.html')


@bp.route('/applications/<uuid:app_id>/update', methods=['GET', 'POST'])
@login_required
@role_required([UserRole.STUDENT])
def update_application(app_id):
    """Update job application status"""
    application = db.session.get(JobApplication, app_id)
    if not application:
        flash('Application not found', 'error')
        return redirect(url_for('career.dashboard'))
    
    # Check permission
    profile = db.session.get(StudentProfile, application.student_profile_id)
    if profile.user_id != current_user.id:
        flash('Unauthorized', 'error')
        return redirect(url_for('career.dashboard'))
    
    if request.method == 'POST':
        status_str = request.form.get('status')
        application.status = JobApplicationStatus[status_str.upper()]
        
        # Update interview details
        interview_date = request.form.get('interview_date')
        if interview_date:
            application.interview_date = datetime.strptime(interview_date, '%Y-%m-%dT%H:%M')
        
        application.interview_notes = request.form.get('interview_notes', '').strip()
        
        # Update offer details
        application.offer_received = request.form.get('offer_received') == 'on'
        if application.offer_received:
            offer_amount = request.form.get('offer_amount')
            if offer_amount:
                application.offer_amount = float(offer_amount)
            application.accepted = request.form.get('accepted') == 'on'
        
        application.notes = request.form.get('notes', '').strip()
        
        db.session.commit()
        
        flash('Application updated successfully!', 'success')
        return redirect(url_for('career.dashboard'))
    
    return render_template('career/update_application.html', application=application)


@bp.route('/placement-tracker')
@login_required
@role_required([UserRole.ADMIN, UserRole.INSTRUCTOR])
def placement_tracker():
    """Admin view of all student placements"""
    profiles = StudentProfile.query.filter(
        StudentProfile.job_search_status.in_(['active', 'placed'])
    ).all()
    
    students_data = []
    for profile in profiles:
        user = db.session.get(User, profile.user_id)
        if user:
            applications = JobApplication.query.filter_by(
                student_profile_id=profile.id
            ).order_by(desc(JobApplication.applied_date)).all()
            
            latest_offer = None
            for app in applications:
                if app.offer_received:
                    latest_offer = app
                    break
            
            students_data.append({
                'user': user,
                'profile': profile,
                'total_applications': len(applications),
                'latest_offer': latest_offer
            })
    
    return render_template('career/placement_tracker.html', students_data=students_data)


@bp.route('/alumni')
def alumni_network():
    """Alumni network hub"""
    alumni = AlumniNetwork.query.order_by(desc(AlumniNetwork.graduation_date)).all()
    
    alumni_data = []
    for alum in alumni:
        user = db.session.get(User, alum.user_id)
        if user:
            alumni_data.append({
                'user': user,
                'alumni': alum
            })
    
    return render_template('career/alumni_network.html', alumni_data=alumni_data)


@bp.route('/alumni/register', methods=['GET', 'POST'])
@login_required
def register_alumni():
    """Register as alumni"""
    # Check if already registered
    existing = AlumniNetwork.query.filter_by(user_id=current_user.id).first()
    
    if request.method == 'POST':
        if existing:
            # Update existing
            alumni = existing
        else:
            alumni = AlumniNetwork(user_id=current_user.id)
        
        alumni.current_company = request.form.get('current_company', '').strip()
        alumni.current_position = request.form.get('current_position', '').strip()
        alumni.current_salary_range = request.form.get('current_salary_range', '').strip()
        alumni.graduation_date = datetime.strptime(request.form.get('graduation_date'), '%Y-%m-%d').date()
        alumni.available_for_mentorship = request.form.get('available_for_mentorship') == 'on'
        alumni.available_for_referrals = request.form.get('available_for_referrals') == 'on'
        alumni.success_story = request.form.get('success_story', '').strip()
        alumni.testimonial = request.form.get('testimonial', '').strip()
        
        if not existing:
            db.session.add(alumni)
        
        db.session.commit()
        
        flash('Alumni profile updated successfully!', 'success')
        return redirect(url_for('career.alumni_network'))
    
    return render_template('career/register_alumni.html', existing=existing)

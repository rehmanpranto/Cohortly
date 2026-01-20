"""
Project-Based Learning Routes
Managing capstone and milestone projects
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from sqlalchemy import desc
from datetime import datetime
from app.extensions import db
from app.models import (
    Project, ProjectSubmission, ProjectStatus, Bootcamp, User,
    UserRole, PortfolioItem, PortfolioItemType, StudentProfile
)
from app.auth.utils import role_required

bp = Blueprint('projects', __name__, url_prefix='/projects')


@bp.route('/')
@login_required
def list_projects():
    """List all projects"""
    if current_user.role == UserRole.STUDENT:
        # Students see projects from their bootcamps
        from app.models import Enrollment
        enrollments = Enrollment.query.filter_by(student_id=current_user.id).all()
        bootcamp_ids = [e.batch.bootcamp_id for e in enrollments]
        projects = Project.query.filter(Project.bootcamp_id.in_(bootcamp_ids)).order_by(Project.deadline).all()
        
        # Get submission status for each project
        project_data = []
        for project in projects:
            submission = ProjectSubmission.query.filter_by(
                project_id=project.id,
                student_id=current_user.id
            ).first()
            project_data.append({
                'project': project,
                'submission': submission
            })
        
        return render_template('projects/student_list.html', project_data=project_data)
    else:
        # Instructors/Admins see all projects
        projects = Project.query.order_by(desc(Project.created_at)).all()
        return render_template('projects/admin_list.html', projects=projects)


@bp.route('/create', methods=['GET', 'POST'])
@login_required
@role_required([UserRole.ADMIN, UserRole.INSTRUCTOR])
def create_project():
    """Create a new project"""
    if request.method == 'POST':
        project = Project(
            bootcamp_id=request.form.get('bootcamp_id'),
            title=request.form.get('title').strip(),
            description=request.form.get('description').strip(),
            requirements=request.form.get('requirements', '').strip(),
            deadline=datetime.strptime(request.form.get('deadline'), '%Y-%m-%dT%H:%M'),
            max_score=int(request.form.get('max_score', 100)),
            is_capstone=request.form.get('is_capstone') == 'on'
        )
        
        db.session.add(project)
        db.session.commit()
        
        flash('Project created successfully', 'success')
        return redirect(url_for('projects.list_projects'))
    
    bootcamps = Bootcamp.query.filter_by(is_active=True).all()
    return render_template('projects/create.html', bootcamps=bootcamps)


@bp.route('/<uuid:project_id>')
@login_required
def view_project(project_id):
    """View project details"""
    project = db.session.get(Project, project_id)
    if not project:
        flash('Project not found', 'error')
        return redirect(url_for('projects.list_projects'))
    
    if current_user.role == UserRole.STUDENT:
        # Get student's submission
        submission = ProjectSubmission.query.filter_by(
            project_id=project_id,
            student_id=current_user.id
        ).first()
        
        return render_template('projects/student_view.html',
                             project=project,
                             submission=submission)
    else:
        # Show all submissions
        submissions = ProjectSubmission.query.filter_by(project_id=project_id).all()
        
        # Get submission stats
        total = len(submissions)
        submitted = sum(1 for s in submissions if s.status in [ProjectStatus.SUBMITTED, ProjectStatus.REVIEWED, ProjectStatus.APPROVED])
        reviewed = sum(1 for s in submissions if s.status in [ProjectStatus.REVIEWED, ProjectStatus.APPROVED])
        
        return render_template('projects/admin_view.html',
                             project=project,
                             submissions=submissions,
                             stats={'total': total, 'submitted': submitted, 'reviewed': reviewed})


@bp.route('/<uuid:project_id>/submit', methods=['GET', 'POST'])
@login_required
@role_required([UserRole.STUDENT])
def submit_project(project_id):
    """Submit a project"""
    project = db.session.get(Project, project_id)
    if not project:
        flash('Project not found', 'error')
        return redirect(url_for('projects.list_projects'))
    
    # Get or create submission
    submission = ProjectSubmission.query.filter_by(
        project_id=project_id,
        student_id=current_user.id
    ).first()
    
    if not submission:
        submission = ProjectSubmission(
            project_id=project_id,
            student_id=current_user.id
        )
        db.session.add(submission)
    
    if request.method == 'POST':
        submission.github_url = request.form.get('github_url', '').strip()
        submission.demo_url = request.form.get('demo_url', '').strip()
        submission.video_url = request.form.get('video_url', '').strip()
        submission.documentation_url = request.form.get('documentation_url', '').strip()
        submission.description = request.form.get('description', '').strip()
        submission.status = ProjectStatus.SUBMITTED
        submission.submitted_at = datetime.utcnow()
        submission.is_late = datetime.utcnow() > project.deadline
        
        db.session.commit()
        
        # Ask if they want to add to portfolio
        if request.form.get('add_to_portfolio') == 'on':
            return redirect(url_for('projects.add_to_portfolio', submission_id=submission.id))
        
        flash('Project submitted successfully!', 'success')
        return redirect(url_for('projects.view_project', project_id=project_id))
    
    return render_template('projects/submit.html',
                         project=project,
                         submission=submission)


@bp.route('/submission/<uuid:submission_id>/review', methods=['GET', 'POST'])
@login_required
@role_required([UserRole.ADMIN, UserRole.INSTRUCTOR])
def review_submission(submission_id):
    """Review and grade a project submission"""
    submission = db.session.get(ProjectSubmission, submission_id)
    if not submission:
        flash('Submission not found', 'error')
        return redirect(url_for('projects.list_projects'))
    
    if request.method == 'POST':
        submission.score = int(request.form.get('score'))
        submission.feedback = request.form.get('feedback', '').strip()
        submission.status = ProjectStatus.REVIEWED
        submission.reviewed_by_id = current_user.id
        submission.reviewed_at = datetime.utcnow()
        
        # Check if approved
        if submission.score >= (submission.project.max_score * 0.7):  # 70% pass threshold
            submission.status = ProjectStatus.APPROVED
        
        db.session.commit()
        
        flash('Submission reviewed successfully', 'success')
        return redirect(url_for('projects.view_project', project_id=submission.project_id))
    
    return render_template('projects/review.html', submission=submission)


@bp.route('/submission/<uuid:submission_id>/add-to-portfolio', methods=['GET', 'POST'])
@login_required
@role_required([UserRole.STUDENT])
def add_to_portfolio(submission_id):
    """Add project submission to portfolio"""
    submission = db.session.get(ProjectSubmission, submission_id)
    if not submission or submission.student_id != current_user.id:
        flash('Submission not found', 'error')
        return redirect(url_for('projects.list_projects'))
    
    # Get or create profile
    profile = StudentProfile.query.filter_by(user_id=current_user.id).first()
    if not profile:
        profile = StudentProfile(user_id=current_user.id)
        db.session.add(profile)
        db.session.commit()
    
    if request.method == 'POST':
        # Parse technologies
        tech_string = request.form.get('technologies', '')
        technologies = [t.strip() for t in tech_string.split(',') if t.strip()]
        
        portfolio_item = PortfolioItem(
            student_profile_id=profile.id,
            item_type=PortfolioItemType.CAPSTONE if submission.project.is_capstone else PortfolioItemType.ASSIGNMENT,
            title=submission.project.title,
            description=submission.description or submission.project.description,
            github_url=submission.github_url,
            demo_url=submission.demo_url,
            image_url=request.form.get('image_url', '').strip(),
            technologies=technologies,
            is_featured=request.form.get('is_featured') == 'on'
        )
        
        db.session.add(portfolio_item)
        db.session.commit()
        
        flash('Added to portfolio successfully!', 'success')
        return redirect(url_for('portfolio.view_portfolio'))
    
    return render_template('projects/add_to_portfolio.html', submission=submission)

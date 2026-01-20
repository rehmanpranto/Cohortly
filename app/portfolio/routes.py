"""
Portfolio Management Routes
Student portfolio showcase
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from sqlalchemy import desc
from app.extensions import db
from app.models import (
    StudentProfile, PortfolioItem, PortfolioItemType, User, UserRole
)
from app.auth.utils import role_required

bp = Blueprint('portfolio', __name__, url_prefix='/portfolio')


@bp.route('/')
def view_portfolio():
    """View own portfolio or redirect to student selection"""
    # If logged in as student, redirect to their portfolio
    if current_user.is_authenticated and current_user.role == UserRole.STUDENT:
        return redirect(url_for('portfolio.view_student_portfolio', student_id=current_user.id))
    
    # For everyone else (including public), show all students with portfolios
    profiles = StudentProfile.query.all()
    students = []
    for profile in profiles:
        user = db.session.get(User, profile.user_id)
        portfolio_count = PortfolioItem.query.filter_by(student_profile_id=profile.id).count()
        if user and portfolio_count > 0:
            students.append({
                'user': user,
                'profile': profile,
                'portfolio_count': portfolio_count
            })
    
    return render_template('portfolio/list_students.html', students=students)


@bp.route('/student/<uuid:student_id>')
def view_student_portfolio(student_id):
    """View a student's portfolio (public or authenticated)"""
    student = db.session.get(User, student_id)
    if not student:
        flash('Student not found', 'error')
        return redirect(url_for('portfolio.view_portfolio'))
    
    profile = StudentProfile.query.filter_by(user_id=student_id).first()
    if not profile:
        flash('Portfolio not found', 'error')
        return redirect(url_for('portfolio.view_portfolio'))
    
    # Get portfolio items
    portfolio_items = PortfolioItem.query.filter_by(
        student_profile_id=profile.id
    ).order_by(
        desc(PortfolioItem.is_featured),
        PortfolioItem.display_order,
        desc(PortfolioItem.created_at)
    ).all()
    
    # Check if viewer can edit
    can_edit = False
    if current_user.is_authenticated:
        can_edit = (current_user.id == student_id or 
                   current_user.role in [UserRole.ADMIN])
    
    return render_template('portfolio/view.html',
                         student=student,
                         profile=profile,
                         portfolio_items=portfolio_items,
                         can_edit=can_edit)


@bp.route('/add', methods=['GET', 'POST'])
@login_required
@role_required([UserRole.STUDENT])
def add_item():
    """Add item to portfolio"""
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
        
        item = PortfolioItem(
            student_profile_id=profile.id,
            item_type=PortfolioItemType[request.form.get('item_type').upper()],
            title=request.form.get('title').strip(),
            description=request.form.get('description', '').strip(),
            github_url=request.form.get('github_url', '').strip(),
            demo_url=request.form.get('demo_url', '').strip(),
            image_url=request.form.get('image_url', '').strip(),
            technologies=technologies,
            is_featured=request.form.get('is_featured') == 'on'
        )
        
        db.session.add(item)
        db.session.commit()
        
        flash('Portfolio item added successfully!', 'success')
        return redirect(url_for('portfolio.view_portfolio'))
    
    return render_template('portfolio/add_item.html')


@bp.route('/edit/<uuid:item_id>', methods=['GET', 'POST'])
@login_required
def edit_item(item_id):
    """Edit portfolio item"""
    item = db.session.get(PortfolioItem, item_id)
    if not item:
        flash('Portfolio item not found', 'error')
        return redirect(url_for('portfolio.view_portfolio'))
    
    # Check permission
    profile = db.session.get(StudentProfile, item.student_profile_id)
    if current_user.role != UserRole.ADMIN and profile.user_id != current_user.id:
        flash('Unauthorized', 'error')
        return redirect(url_for('portfolio.view_portfolio'))
    
    if request.method == 'POST':
        # Parse technologies
        tech_string = request.form.get('technologies', '')
        technologies = [t.strip() for t in tech_string.split(',') if t.strip()]
        
        item.item_type = PortfolioItemType[request.form.get('item_type').upper()]
        item.title = request.form.get('title').strip()
        item.description = request.form.get('description', '').strip()
        item.github_url = request.form.get('github_url', '').strip()
        item.demo_url = request.form.get('demo_url', '').strip()
        item.image_url = request.form.get('image_url', '').strip()
        item.technologies = technologies
        item.is_featured = request.form.get('is_featured') == 'on'
        item.display_order = int(request.form.get('display_order', 0))
        
        db.session.commit()
        
        flash('Portfolio item updated successfully!', 'success')
        return redirect(url_for('portfolio.view_portfolio'))
    
    return render_template('portfolio/edit_item.html', item=item)


@bp.route('/delete/<uuid:item_id>', methods=['POST'])
@login_required
def delete_item(item_id):
    """Delete portfolio item"""
    item = db.session.get(PortfolioItem, item_id)
    if not item:
        flash('Portfolio item not found', 'error')
        return redirect(url_for('portfolio.view_portfolio'))
    
    # Check permission
    profile = db.session.get(StudentProfile, item.student_profile_id)
    if current_user.role != UserRole.ADMIN and profile.user_id != current_user.id:
        flash('Unauthorized', 'error')
        return redirect(url_for('portfolio.view_portfolio'))
    
    db.session.delete(item)
    db.session.commit()
    
    flash('Portfolio item deleted successfully', 'success')
    return redirect(url_for('portfolio.view_portfolio'))


@bp.route('/public/<uuid:student_id>')
def public_portfolio(student_id):
    """Public portfolio view (shareable link)"""
    return view_student_portfolio(student_id)

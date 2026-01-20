"""
Analytics Module Routes
"""
from flask import Blueprint, render_template
from flask_login import login_required
from app.extensions import db
from app.models import Lead, Enrollment, Payment, User, Batch, LeadStatus, UserRole, EnrollmentStatus, PaymentStatus, BatchStatus
from app.auth.utils import admin_required
from sqlalchemy import func
from datetime import datetime, timedelta

analytics_bp = Blueprint('analytics', __name__)


@analytics_bp.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    """Admin analytics dashboard"""
    
    # Lead stats
    total_leads = Lead.query.count()
    new_leads = Lead.query.filter_by(status=LeadStatus.NEW).count()
    converted_leads = Lead.query.filter_by(status=LeadStatus.CONVERTED).count()
    conversion_rate = (converted_leads / total_leads * 100) if total_leads > 0 else 0
    
    # User stats
    total_students = User.query.filter_by(role=UserRole.STUDENT).count()
    total_instructors = User.query.filter_by(role=UserRole.INSTRUCTOR).count()
    
    # Enrollment stats
    total_enrollments = Enrollment.query.count()
    active_enrollments = Enrollment.query.filter_by(status=EnrollmentStatus.ACTIVE).count()
    
    # Revenue stats
    total_revenue = db.session.query(func.sum(Payment.amount)).filter_by(status=PaymentStatus.COMPLETED).scalar() or 0
    
    # Recent activity
    recent_enrollments = Enrollment.query.order_by(Enrollment.created_at.desc()).limit(10).all()
    recent_leads = Lead.query.order_by(Lead.created_at.desc()).limit(10).all()
    
    # Batch stats
    active_batches = Batch.query.filter_by(status=BatchStatus.ONGOING).count()
    upcoming_batches = Batch.query.filter_by(status=BatchStatus.UPCOMING).count()
    
    # Create stats dictionary for template
    stats = {
        'total_leads': total_leads,
        'new_leads': new_leads,
        'converted_leads': converted_leads,
        'conversion_rate': conversion_rate,
        'total_students': total_students,
        'total_instructors': total_instructors,
        'total_enrollments': total_enrollments,
        'active_enrollments': active_enrollments,
        'total_revenue': total_revenue,
        'active_batches': active_batches,
        'upcoming_batches': upcoming_batches
    }
    
    return render_template('admin/admin_dashboard.html',
                         stats=stats,
                         recent_enrollments=recent_enrollments,
                         recent_leads=recent_leads)


@analytics_bp.route('/reports/revenue')
@admin_required
def revenue_report():
    """Revenue report"""
    payments = Payment.query.filter_by(status=PaymentStatus.COMPLETED).all()
    return render_template('admin/revenue_report.html', payments=payments)


@analytics_bp.route('/reports/enrollments')
@admin_required
def enrollment_report():
    """Enrollment trends report"""
    enrollments = Enrollment.query.order_by(Enrollment.created_at.desc()).all()
    return render_template('admin/enrollment_report.html', enrollments=enrollments)

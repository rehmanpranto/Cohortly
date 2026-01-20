"""
Payments Module Routes
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Enrollment, Payment, PaymentStatus
from app.auth.utils import student_required, admin_required
from datetime import datetime, timedelta
from sqlalchemy import func, extract
from decimal import Decimal
import calendar

payments_bp = Blueprint('payments', __name__)


@payments_bp.route('/checkout/<uuid:batch_id>')
@student_required
def checkout(batch_id):
    """Payment checkout page"""
    from app.models import Batch
    batch = Batch.query.get_or_404(batch_id)
    return render_template('payments/checkout.html', batch=batch)


@payments_bp.route('/process', methods=['POST'])
@student_required
def process_payment():
    """Process payment (mock for now)"""
    # This would integrate with real payment gateway
    
    batch_id = request.form['batch_id']
    amount = float(request.form['amount'])
    
    try:
        # Create enrollment
        enrollment = Enrollment(
            student_id=current_user.id,
            batch_id=batch_id,
            status='pending'
        )
        db.session.add(enrollment)
        db.session.flush()
        
        # Create payment record
        payment = Payment(
            enrollment_id=enrollment.id,
            amount=amount,
            payment_method=request.form['payment_method'],
            status=PaymentStatus.COMPLETED,
            transaction_id=f'TXN_{enrollment.id}'
        )
        db.session.add(payment)
        
        # Activate enrollment
        enrollment.status = 'active'
        
        db.session.commit()
        
        flash('Payment successful! You are now enrolled.', 'success')
        return redirect(url_for('lms.student_dashboard'))
    
    except Exception as e:
        db.session.rollback()
        flash(f'Payment failed: {str(e)}', 'danger')
        return redirect(url_for('payments.checkout', batch_id=batch_id))


@payments_bp.route('/history')
@student_required
def payment_history():
    """View payment history"""
    enrollments = Enrollment.query.filter_by(student_id=current_user.id).all()
    payments = []
    for enrollment in enrollments:
        payments.extend(enrollment.payments)
    
    return render_template('payments/history.html', payments=payments)


@payments_bp.route('/finance/dashboard')
@admin_required
def finance_dashboard():
    """Finance dashboard with calendar view and sales reports"""
    from app.models import User, Batch, Bootcamp
    
    # Get current date
    today = datetime.now()
    current_year = today.year
    current_month = today.month
    current_quarter = (current_month - 1) // 3 + 1
    
    # Get year and month from query params
    selected_year = int(request.args.get('year', current_year))
    selected_month = int(request.args.get('month', current_month))
    
    # Calculate daily sales for the selected month
    first_day = datetime(selected_year, selected_month, 1)
    if selected_month == 12:
        last_day = datetime(selected_year + 1, 1, 1) - timedelta(days=1)
    else:
        last_day = datetime(selected_year, selected_month + 1, 1) - timedelta(days=1)
    
    # Query daily sales
    daily_sales = db.session.query(
        func.date(Payment.paid_at).label('date'),
        func.sum(Payment.amount).label('total'),
        func.count(Payment.id).label('count')
    ).filter(
        Payment.status == PaymentStatus.COMPLETED,
        Payment.paid_at >= first_day,
        Payment.paid_at <= last_day
    ).group_by(
        func.date(Payment.paid_at)
    ).all()
    
    # Create calendar data structure
    cal = calendar.monthcalendar(selected_year, selected_month)
    daily_sales_dict = {sale.date.day: {'total': float(sale.total), 'count': sale.count} for sale in daily_sales}
    
    # Calculate monthly totals for the year
    monthly_sales = db.session.query(
        extract('month', Payment.paid_at).label('month'),
        func.sum(Payment.amount).label('total'),
        func.count(Payment.id).label('count')
    ).filter(
        Payment.status == PaymentStatus.COMPLETED,
        extract('year', Payment.paid_at) == selected_year
    ).group_by(
        extract('month', Payment.paid_at)
    ).all()
    
    monthly_data = {int(sale.month): {'total': float(sale.total), 'count': sale.count} for sale in monthly_sales}
    
    # Calculate quarterly sales
    quarterly_sales = []
    for quarter in range(1, 5):
        quarter_months = [(quarter - 1) * 3 + i for i in range(1, 4)]
        quarter_total = sum(monthly_data.get(m, {'total': 0})['total'] for m in quarter_months)
        quarter_count = sum(monthly_data.get(m, {'count': 0})['count'] for m in quarter_months)
        quarterly_sales.append({
            'quarter': quarter,
            'total': quarter_total,
            'count': quarter_count
        })
    
    # Current month stats
    current_month_total = monthly_data.get(selected_month, {'total': 0, 'count': 0})
    
    # Year total
    year_total = sum(m['total'] for m in monthly_data.values())
    year_count = sum(m['count'] for m in monthly_data.values())
    
    # Recent transactions
    recent_payments = Payment.query.filter_by(status=PaymentStatus.COMPLETED)\
        .order_by(Payment.paid_at.desc()).limit(10).all()
    
    # Top students by payment
    top_students = db.session.query(
        User.id,
        User.full_name,
        User.email,
        func.sum(Payment.amount).label('total_paid'),
        func.count(Payment.id).label('payment_count')
    ).join(
        Enrollment, Enrollment.student_id == User.id
    ).join(
        Payment, Payment.enrollment_id == Enrollment.id
    ).filter(
        Payment.status == PaymentStatus.COMPLETED
    ).group_by(
        User.id, User.full_name, User.email
    ).order_by(
        func.sum(Payment.amount).desc()
    ).limit(5).all()
    
    # Top bootcamps by revenue
    top_bootcamps = db.session.query(
        Bootcamp.id,
        Bootcamp.name,
        func.sum(Payment.amount).label('total_revenue'),
        func.count(Payment.id).label('enrollments')
    ).join(
        Batch, Batch.bootcamp_id == Bootcamp.id
    ).join(
        Enrollment, Enrollment.batch_id == Batch.id
    ).join(
        Payment, Payment.enrollment_id == Enrollment.id
    ).filter(
        Payment.status == PaymentStatus.COMPLETED
    ).group_by(
        Bootcamp.id, Bootcamp.name
    ).order_by(
        func.sum(Payment.amount).desc()
    ).limit(5).all()
    
    return render_template('payments/finance_dashboard.html',
                         calendar_data=cal,
                         daily_sales=daily_sales_dict,
                         monthly_data=monthly_data,
                         quarterly_sales=quarterly_sales,
                         selected_year=selected_year,
                         selected_month=selected_month,
                         current_month_total=current_month_total,
                         year_total=year_total,
                         year_count=year_count,
                         recent_payments=recent_payments,
                         top_students=top_students,
                         top_bootcamps=top_bootcamps,
                         month_name=calendar.month_name[selected_month])


@payments_bp.route('/finance/api/sales/<int:year>/<int:month>/<int:day>')
@admin_required
def get_daily_sales_details(year, month, day):
    """Get detailed sales for a specific day"""
    target_date = datetime(year, month, day)
    next_date = target_date + timedelta(days=1)
    
    payments = Payment.query.filter(
        Payment.status == PaymentStatus.COMPLETED,
        Payment.paid_at >= target_date,
        Payment.paid_at < next_date
    ).order_by(Payment.paid_at.desc()).all()
    
    details = []
    for payment in payments:
        enrollment = payment.enrollment
        details.append({
            'time': payment.paid_at.strftime('%I:%M %p'),
            'student': enrollment.student.full_name,
            'bootcamp': enrollment.batch.bootcamp.name,
            'batch': enrollment.batch.name,
            'amount': float(payment.amount),
            'method': payment.payment_method
        })
    
    return jsonify({
        'date': target_date.strftime('%B %d, %Y'),
        'total': sum(d['amount'] for d in details),
        'count': len(details),
        'transactions': details
    })

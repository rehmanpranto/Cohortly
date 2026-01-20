"""
Payments Module Routes
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Enrollment, Payment, PaymentStatus
from app.auth.utils import student_required

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

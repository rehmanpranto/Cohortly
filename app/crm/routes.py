"""
CRM Module - Lead Management Routes
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Lead, LeadLog, LeadStatus, User, UserRole
from app.auth.utils import sales_required, admin_required
from datetime import datetime

crm_bp = Blueprint('crm', __name__)


@crm_bp.route('/dashboard')
@sales_required
def sales_dashboard():
    """Sales dashboard"""
    # Get leads assigned to current user (or all if admin)
    if current_user.role == UserRole.ADMIN:
        leads = Lead.query.order_by(Lead.created_at.desc()).all()
    else:
        leads = Lead.query.filter_by(assigned_to_id=current_user.id).order_by(Lead.created_at.desc()).all()
    
    # Stats
    total_leads = len(leads)
    new_leads = len([l for l in leads if l.status == LeadStatus.NEW])
    converted_leads = len([l for l in leads if l.status == LeadStatus.CONVERTED])
    
    return render_template('admin/sales_dashboard.html',
                         leads=leads,
                         total_leads=total_leads,
                         new_leads=new_leads,
                         converted_leads=converted_leads)


@crm_bp.route('/leads')
@sales_required
def list_leads():
    """List all leads"""
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status')
    
    query = Lead.query
    
    # Filter by status if provided
    if status:
        try:
            status_enum = LeadStatus[status.upper()]
            query = query.filter_by(status=status_enum)
        except KeyError:
            pass
    
    # Filter by assigned user if not admin
    if current_user.role != UserRole.ADMIN:
        query = query.filter_by(assigned_to_id=current_user.id)
    
    leads = query.order_by(Lead.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('admin/leads.html', leads=leads)


@crm_bp.route('/leads/create', methods=['GET', 'POST'])
@sales_required
def create_lead():
    """Create new lead"""
    if request.method == 'POST':
        try:
            # Get status from form or default to NEW
            status_value = request.form.get('status', 'new')
            status = LeadStatus[status_value.upper()]
            
            lead = Lead(
                full_name=request.form['full_name'],
                email=request.form['email'],
                phone=request.form.get('phone'),
                source=request.form.get('source'),
                status=status,
                assigned_to_id=current_user.id
            )
            
            db.session.add(lead)
            db.session.flush()  # Get the lead ID
            
            # Add initial note if provided
            notes = request.form.get('notes')
            if notes and notes.strip():
                from app.models import LeadLog
                log = LeadLog(
                    lead_id=lead.id,
                    user_id=current_user.id,
                    action='created',
                    notes=notes
                )
                db.session.add(log)
            
            db.session.commit()
            
            flash('Lead created successfully!', 'success')
            return redirect(url_for('crm.view_lead', lead_id=lead.id))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating lead: {str(e)}', 'danger')
    
    return render_template('admin/create_lead.html')


@crm_bp.route('/leads/<uuid:lead_id>')
@sales_required
def view_lead(lead_id):
    """View lead details"""
    lead = Lead.query.get_or_404(lead_id)
    
    # Check permission (admin can see all, sales can only see assigned)
    if current_user.role != UserRole.ADMIN and lead.assigned_to_id != current_user.id:
        flash('You do not have permission to view this lead.', 'danger')
        return redirect(url_for('crm.list_leads'))
    
    logs = LeadLog.query.filter_by(lead_id=lead_id).order_by(LeadLog.created_at.desc()).all()
    
    return render_template('admin/lead_detail.html', lead=lead, logs=logs)


@crm_bp.route('/leads/<uuid:lead_id>/log', methods=['POST'])
@sales_required
def add_lead_log(lead_id):
    """Add log entry to lead"""
    lead = Lead.query.get_or_404(lead_id)
    
    # Check permission
    if current_user.role != UserRole.ADMIN and lead.assigned_to_id != current_user.id:
        flash('You do not have permission to update this lead.', 'danger')
        return redirect(url_for('crm.list_leads'))
    
    try:
        log = LeadLog(
            lead_id=lead_id,
            note=request.form['note'],
            next_follow_up=datetime.strptime(request.form['next_follow_up'], '%Y-%m-%d') if request.form.get('next_follow_up') else None,
            created_by_id=current_user.id
        )
        
        db.session.add(log)
        db.session.commit()
        
        flash('Log added successfully!', 'success')
    
    except Exception as e:
        db.session.rollback()
        flash(f'Error adding log: {str(e)}', 'danger')
    
    return redirect(url_for('crm.view_lead', lead_id=lead_id))


@crm_bp.route('/leads/<uuid:lead_id>/status', methods=['POST'])
@sales_required
def update_lead_status(lead_id):
    """Update lead status"""
    lead = Lead.query.get_or_404(lead_id)
    
    # Check permission
    if current_user.role != UserRole.ADMIN and lead.assigned_to_id != current_user.id:
        flash('You do not have permission to update this lead.', 'danger')
        return redirect(url_for('crm.list_leads'))
    
    try:
        new_status = LeadStatus[request.form['status'].upper()]
        lead.status = new_status
        db.session.commit()
        
        flash('Lead status updated!', 'success')
    
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating status: {str(e)}', 'danger')
    
    return redirect(url_for('crm.view_lead', lead_id=lead_id))


@crm_bp.route('/leads/<uuid:lead_id>/convert', methods=['POST'])
@sales_required
def convert_lead(lead_id):
    """Convert lead to student"""
    lead = Lead.query.get_or_404(lead_id)
    
    # Check permission
    if current_user.role != UserRole.ADMIN and lead.assigned_to_id != current_user.id:
        flash('You do not have permission to convert this lead.', 'danger')
        return redirect(url_for('crm.list_leads'))
    
    # Check if already converted
    if lead.status == LeadStatus.CONVERTED:
        flash('Lead is already converted.', 'warning')
        return redirect(url_for('crm.view_lead', lead_id=lead_id))
    
    try:
        from app.auth.utils import hash_password
        
        # Create student user
        student = User(
            email=lead.email,
            password_hash=hash_password(request.form['temporary_password']),
            full_name=lead.full_name,
            phone=lead.phone,
            role=UserRole.STUDENT,
            is_active=True
        )
        
        db.session.add(student)
        
        # Update lead
        lead.status = LeadStatus.CONVERTED
        lead.converted_to_user_id = student.id
        
        # Add log
        log = LeadLog(
            lead_id=lead_id,
            note=f'Lead converted to student. Temporary password set.',
            created_by_id=current_user.id
        )
        db.session.add(log)
        
        db.session.commit()
        
        flash(f'Lead converted to student! Email: {student.email}. Now enroll them in a bootcamp.', 'success')
        return redirect(url_for('crm.quick_enroll', student_id=student.id))
    
    except Exception as e:
        db.session.rollback()
        flash(f'Error converting lead: {str(e)}', 'danger')
        return redirect(url_for('crm.view_lead', lead_id=lead_id))


@crm_bp.route('/enrollments')
@sales_required
def list_enrollments():
    """List all enrollments"""
    from app.models import Enrollment
    
    enrollments = Enrollment.query.order_by(Enrollment.created_at.desc()).all()
    return render_template('admin/enrollments.html', enrollments=enrollments)


@crm_bp.route('/enrollments/create/<uuid:student_id>', methods=['GET', 'POST'])
@sales_required
def enroll_student(student_id):
    """Enroll a student in a bootcamp"""
    from app.models import User, Bootcamp, Batch, Enrollment, EnrollmentStatus
    
    student = User.query.get_or_404(student_id)
    
    if student.role != UserRole.STUDENT:
        flash('Only students can be enrolled in bootcamps.', 'danger')
        return redirect(url_for('crm.list_enrollments'))
    
    if request.method == 'POST':
        try:
            batch_ids = request.form.getlist('batch_ids[]')
            
            if not batch_ids:
                flash('Please select at least one batch.', 'warning')
                return redirect(url_for('crm.enroll_student', student_id=student_id))
            
            enrolled_count = 0
            for batch_id in batch_ids:
                # Check if already enrolled
                existing = Enrollment.query.filter_by(
                    student_id=student_id,
                    batch_id=batch_id
                ).first()
                
                if existing:
                    continue
                
                enrollment = Enrollment(
                    student_id=student_id,
                    batch_id=batch_id,
                    status=EnrollmentStatus.ACTIVE,
                    enrolled_at=datetime.utcnow(),
                    progress_percentage=0
                )
                db.session.add(enrollment)
                enrolled_count += 1
            
            db.session.commit()
            
            if enrolled_count > 0:
                flash(f'Successfully enrolled student in {enrolled_count} batch(es)!', 'success')
            else:
                flash('Student is already enrolled in all selected batches.', 'info')
            
            return redirect(url_for('crm.list_enrollments'))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error enrolling student: {str(e)}', 'danger')
    
    # Get all batches grouped by bootcamp
    bootcamps = Bootcamp.query.all()
    student_enrollments = Enrollment.query.filter_by(student_id=student_id).all()
    enrolled_batch_ids = [e.batch_id for e in student_enrollments]
    
    return render_template('admin/enroll_student.html', 
                         student=student, 
                         bootcamps=bootcamps,
                         enrolled_batch_ids=enrolled_batch_ids)


@crm_bp.route('/batches')
@sales_required
def list_batches():
    """List all batches"""
    from app.models import Batch
    
    batches = Batch.query.order_by(Batch.created_at.desc()).all()
    return render_template('admin/batches.html', batches=batches)


@crm_bp.route('/students')
@sales_required
def list_students():
    """List all students with enrollment options"""
    from app.models import User, Enrollment, Lead
    
    # Get all students
    students = User.query.filter_by(role=UserRole.STUDENT).order_by(User.created_at.desc()).all()
    
    # Get enrollment counts for each student
    student_data = []
    for student in students:
        enrollments_count = Enrollment.query.filter_by(student_id=student.id).count()
        
        # Check if student was converted from a lead
        lead = Lead.query.filter_by(email=student.email).first()
        
        student_data.append({
            'student': student,
            'enrollments_count': enrollments_count,
            'lead': lead
        })
    
    return render_template('admin/students_list.html', student_data=student_data)


@crm_bp.route('/quick-enroll/<uuid:student_id>', methods=['GET', 'POST'])
@sales_required
def quick_enroll(student_id):
    """Quick enrollment form with lead matching"""
    from app.models import User, Bootcamp, Batch, Enrollment, EnrollmentStatus, Lead
    
    student = User.query.get_or_404(student_id)
    
    if student.role != UserRole.STUDENT:
        flash('Only students can be enrolled in bootcamps.', 'danger')
        return redirect(url_for('crm.list_students'))
    
    # Get lead data if exists
    lead = Lead.query.filter_by(email=student.email).first()
    
    if request.method == 'POST':
        try:
            batch_id = request.form.get('batch_id')
            
            if not batch_id:
                flash('Please select a batch.', 'warning')
                return redirect(url_for('crm.quick_enroll', student_id=student_id))
            
            # Check if already enrolled
            existing = Enrollment.query.filter_by(
                student_id=student_id,
                batch_id=batch_id
            ).first()
            
            if existing:
                flash('Student is already enrolled in this batch.', 'info')
                return redirect(url_for('crm.list_students'))
            
            # Create enrollment
            enrollment = Enrollment(
                student_id=student_id,
                batch_id=batch_id,
                status=EnrollmentStatus.ACTIVE,
                enrolled_by_id=current_user.id
            )
            db.session.add(enrollment)
            
            # Update lead status if exists
            if lead and lead.status != 'converted':
                lead.status = 'converted'
                lead.converted_at = datetime.utcnow()
            
            db.session.commit()
            flash(f'Successfully enrolled {student.full_name}!', 'success')
            return redirect(url_for('crm.list_students'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error enrolling student: {str(e)}', 'danger')
            return redirect(url_for('crm.quick_enroll', student_id=student_id))
    
    # Get all bootcamps with their batches
    bootcamps = Bootcamp.query.all()
    student_enrollments = Enrollment.query.filter_by(student_id=student_id).all()
    enrolled_batch_ids = [e.batch_id for e in student_enrollments]
    
    return render_template('admin/quick_enroll.html', 
                         student=student,
                         lead=lead,
                         bootcamps=bootcamps,
                         enrolled_batch_ids=enrolled_batch_ids)

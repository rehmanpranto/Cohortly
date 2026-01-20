"""
Database models for the Bootcamp Management System
"""
import uuid
from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy.dialects.postgresql import UUID
from flask_login import UserMixin
from app.extensions import db


class UserRole(PyEnum):
    """User roles enum"""
    ADMIN = 'admin'
    SALES = 'sales'
    INSTRUCTOR = 'instructor'
    MENTOR = 'mentor'
    STUDENT = 'student'


class LeadStatus(PyEnum):
    """Lead status enum"""
    NEW = 'new'
    CONTACTED = 'contacted'
    QUALIFIED = 'qualified'
    CONVERTED = 'converted'
    LOST = 'lost'


class BatchStatus(PyEnum):
    """Batch status enum"""
    UPCOMING = 'upcoming'
    ONGOING = 'ongoing'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'


class EnrollmentStatus(PyEnum):
    """Enrollment status enum"""
    PENDING = 'pending'
    ACTIVE = 'active'
    COMPLETED = 'completed'
    DROPPED = 'dropped'


class PaymentStatus(PyEnum):
    """Payment status enum"""
    PENDING = 'pending'
    COMPLETED = 'completed'
    FAILED = 'failed'
    REFUNDED = 'refunded'


class RAGRating(PyEnum):
    """RAG (Red-Amber-Green) Performance Rating"""
    RED = 'red'  # At risk - needs immediate intervention
    AMBER = 'amber'  # Needs attention
    GREEN = 'green'  # On track


class ProjectStatus(PyEnum):
    """Project submission status"""
    NOT_STARTED = 'not_started'
    IN_PROGRESS = 'in_progress'
    SUBMITTED = 'submitted'
    REVIEWED = 'reviewed'
    APPROVED = 'approved'


class PortfolioItemType(PyEnum):
    """Portfolio item types"""
    CAPSTONE = 'capstone'
    ASSIGNMENT = 'assignment'
    PERSONAL = 'personal'
    HACKATHON = 'hackathon'


class JobApplicationStatus(PyEnum):
    """Job application tracking status"""
    APPLIED = 'applied'
    SCREENING = 'screening'
    INTERVIEW = 'interview'
    OFFER = 'offer'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'


class SurveyType(PyEnum):
    """Survey types"""
    INSTRUCTOR_EVAL = 'instructor_evaluation'
    COURSE_FEEDBACK = 'course_feedback'
    EXIT_SURVEY = 'exit_survey'


class ContentType(PyEnum):
    """Content type enum"""
    VIDEO = 'video'
    DOCUMENT = 'document'
    QUIZ = 'quiz'
    LIVE_SESSION = 'live_session'


# =========================
# USER & AUTHENTICATION
# =========================

class User(UserMixin, db.Model):
    """User model"""
    __tablename__ = 'users'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(UserRole), nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20))
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    refresh_tokens = db.relationship('RefreshToken', back_populates='user', cascade='all, delete-orphan')
    assigned_leads = db.relationship('Lead', foreign_keys='Lead.assigned_to_id', back_populates='assigned_to')
    created_bootcamps = db.relationship('Bootcamp', back_populates='creator')
    instructor_batches = db.relationship('InstructorBatch', back_populates='instructor')
    mentor_batches = db.relationship('MentorBatch', back_populates='mentor')
    enrollments = db.relationship('Enrollment', back_populates='student')
    submissions = db.relationship('Submission', back_populates='student')
    graded_submissions = db.relationship('Grade', foreign_keys='Grade.graded_by_id', back_populates='grader')
    notifications = db.relationship('Notification', back_populates='user', cascade='all, delete-orphan')
    
    def get_id(self):
        """Override Flask-Login's get_id to return string representation of UUID"""
        return str(self.id)
    
    def __repr__(self):
        return f'<User {self.email}>'


class RefreshToken(db.Model):
    """Refresh token model"""
    __tablename__ = 'refresh_tokens'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    token = db.Column(db.Text, nullable=False, unique=True, index=True)
    expires_at = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    user = db.relationship('User', back_populates='refresh_tokens')


# =========================
# LEAD & CRM
# =========================

class Lead(db.Model):
    """Lead model"""
    __tablename__ = 'leads'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, index=True)
    phone = db.Column(db.String(20))
    source = db.Column(db.String(100))  # e.g., 'website', 'referral', 'facebook'
    status = db.Column(db.Enum(LeadStatus), nullable=False, default=LeadStatus.NEW)
    assigned_to_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id', ondelete='SET NULL'))
    converted_to_user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id', ondelete='SET NULL'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    assigned_to = db.relationship('User', foreign_keys=[assigned_to_id], back_populates='assigned_leads')
    logs = db.relationship('LeadLog', back_populates='lead', cascade='all, delete-orphan')


class LeadLog(db.Model):
    """Lead log model"""
    __tablename__ = 'lead_logs'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lead_id = db.Column(UUID(as_uuid=True), db.ForeignKey('leads.id', ondelete='CASCADE'), nullable=False)
    note = db.Column(db.Text, nullable=False)
    next_follow_up = db.Column(db.DateTime)
    created_by_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id', ondelete='SET NULL'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    lead = db.relationship('Lead', back_populates='logs')
    created_by = db.relationship('User')


# =========================
# BOOTCAMP & BATCH
# =========================

class Bootcamp(db.Model):
    """Bootcamp model"""
    __tablename__ = 'bootcamps'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    mode = db.Column(db.String(50), nullable=False)  # 'live', 'recorded', 'hybrid'
    price = db.Column(db.Numeric(10, 2), nullable=False)
    duration_weeks = db.Column(db.Integer, nullable=False)
    created_by_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id', ondelete='SET NULL'))
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    creator = db.relationship('User', back_populates='created_bootcamps')
    batches = db.relationship('Batch', back_populates='bootcamp', cascade='all, delete-orphan')
    modules = db.relationship('Module', back_populates='bootcamp', cascade='all, delete-orphan')


class Batch(db.Model):
    """Batch model"""
    __tablename__ = 'batches'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    bootcamp_id = db.Column(UUID(as_uuid=True), db.ForeignKey('bootcamps.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    capacity = db.Column(db.Integer, nullable=False, default=30)
    status = db.Column(db.Enum(BatchStatus), nullable=False, default=BatchStatus.UPCOMING)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    bootcamp = db.relationship('Bootcamp', back_populates='batches')
    instructors = db.relationship('InstructorBatch', back_populates='batch', cascade='all, delete-orphan')
    mentors = db.relationship('MentorBatch', back_populates='batch', cascade='all, delete-orphan')
    enrollments = db.relationship('Enrollment', back_populates='batch', cascade='all, delete-orphan')
    announcements = db.relationship('Announcement', back_populates='batch', cascade='all, delete-orphan')
    class_schedules = db.relationship('ClassSchedule', back_populates='batch', cascade='all, delete-orphan')


class InstructorBatch(db.Model):
    """Instructor-Batch association"""
    __tablename__ = 'instructor_batches'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    instructor_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    batch_id = db.Column(UUID(as_uuid=True), db.ForeignKey('batches.id', ondelete='CASCADE'), nullable=False)
    assigned_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    instructor = db.relationship('User', back_populates='instructor_batches')
    batch = db.relationship('Batch', back_populates='instructors')


class MentorBatch(db.Model):
    """Mentor-Batch association"""
    __tablename__ = 'mentor_batches'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    mentor_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    batch_id = db.Column(UUID(as_uuid=True), db.ForeignKey('batches.id', ondelete='CASCADE'), nullable=False)
    assigned_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    mentor = db.relationship('User', back_populates='mentor_batches')
    batch = db.relationship('Batch', back_populates='mentors')


class ClassSchedule(db.Model):
    """Weekly class schedule with Zoom links for batches"""
    __tablename__ = 'class_schedules'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    batch_id = db.Column(UUID(as_uuid=True), db.ForeignKey('batches.id', ondelete='CASCADE'), nullable=False)
    
    week_number = db.Column(db.Integer, nullable=False)  # Week 1, 2, 3, etc.
    class_date = db.Column(db.Date, nullable=False)
    class_time = db.Column(db.Time, nullable=False)
    duration_minutes = db.Column(db.Integer, default=120)  # Default 2 hours
    
    topic = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    
    zoom_link = db.Column(db.Text, nullable=False)
    zoom_meeting_id = db.Column(db.String(100))
    zoom_passcode = db.Column(db.String(50))
    
    recording_link = db.Column(db.Text)  # Link to recording after class
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    batch = db.relationship('Batch', back_populates='class_schedules')
    
    def __repr__(self):
        return f'<ClassSchedule Week {self.week_number}: {self.topic}>'


# =========================
# ENROLLMENT & PAYMENTS
# =========================

class Enrollment(db.Model):
    """Enrollment model"""
    __tablename__ = 'enrollments'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    batch_id = db.Column(UUID(as_uuid=True), db.ForeignKey('batches.id', ondelete='CASCADE'), nullable=False)
    status = db.Column(db.Enum(EnrollmentStatus), nullable=False, default=EnrollmentStatus.PENDING)
    enrolled_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    completed_at = db.Column(db.DateTime)
    progress_percentage = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    student = db.relationship('User', back_populates='enrollments')
    batch = db.relationship('Batch', back_populates='enrollments')
    payments = db.relationship('Payment', back_populates='enrollment', cascade='all, delete-orphan')
    attendance_records = db.relationship('Attendance', back_populates='enrollment', cascade='all, delete-orphan')
    certificate = db.relationship('Certificate', back_populates='enrollment', uselist=False, cascade='all, delete-orphan')


class Payment(db.Model):
    """Payment model"""
    __tablename__ = 'payments'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    enrollment_id = db.Column(UUID(as_uuid=True), db.ForeignKey('enrollments.id', ondelete='CASCADE'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_method = db.Column(db.String(100))  # 'credit_card', 'bank_transfer', etc.
    status = db.Column(db.Enum(PaymentStatus), nullable=False, default=PaymentStatus.PENDING)
    transaction_id = db.Column(db.String(255), unique=True)
    paid_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    enrollment = db.relationship('Enrollment', back_populates='payments')


# =========================
# LMS - CURRICULUM
# =========================

class Module(db.Model):
    """Module model"""
    __tablename__ = 'modules'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    bootcamp_id = db.Column(UUID(as_uuid=True), db.ForeignKey('bootcamps.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    order_index = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    bootcamp = db.relationship('Bootcamp', back_populates='modules')
    lessons = db.relationship('Lesson', back_populates='module', cascade='all, delete-orphan', order_by='Lesson.order_index')


class Lesson(db.Model):
    """Lesson model"""
    __tablename__ = 'lessons'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    module_id = db.Column(UUID(as_uuid=True), db.ForeignKey('modules.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    content_type = db.Column(db.Enum(ContentType), nullable=False)
    content_url = db.Column(db.Text)  # Video URL, document URL, etc.
    duration_minutes = db.Column(db.Integer)
    order_index = db.Column(db.Integer, nullable=False)
    is_published = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    module = db.relationship('Module', back_populates='lessons')
    resources = db.relationship('Resource', back_populates='lesson', cascade='all, delete-orphan')
    assignments = db.relationship('Assignment', back_populates='lesson', cascade='all, delete-orphan')


class Resource(db.Model):
    """Resource model"""
    __tablename__ = 'resources'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lesson_id = db.Column(UUID(as_uuid=True), db.ForeignKey('lessons.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    resource_type = db.Column(db.String(50), nullable=False)  # 'pdf', 'link', 'video'
    url = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    lesson = db.relationship('Lesson', back_populates='resources')


class Attendance(db.Model):
    """Attendance model"""
    __tablename__ = 'attendance'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    enrollment_id = db.Column(UUID(as_uuid=True), db.ForeignKey('enrollments.id', ondelete='CASCADE'), nullable=False)
    session_date = db.Column(db.Date, nullable=False)
    present = db.Column(db.Boolean, nullable=False, default=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    enrollment = db.relationship('Enrollment', back_populates='attendance_records')


# =========================
# ASSIGNMENTS & GRADING
# =========================

class Assignment(db.Model):
    """Assignment model"""
    __tablename__ = 'assignments'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lesson_id = db.Column(UUID(as_uuid=True), db.ForeignKey('lessons.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    deadline = db.Column(db.DateTime, nullable=False)
    max_score = db.Column(db.Integer, nullable=False, default=100)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    lesson = db.relationship('Lesson', back_populates='assignments')
    submissions = db.relationship('Submission', back_populates='assignment', cascade='all, delete-orphan')


class Submission(db.Model):
    """Submission model"""
    __tablename__ = 'submissions'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    assignment_id = db.Column(UUID(as_uuid=True), db.ForeignKey('assignments.id', ondelete='CASCADE'), nullable=False)
    student_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    submission_url = db.Column(db.Text)  # Link to GitHub, Drive, etc.
    submission_text = db.Column(db.Text)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    is_late = db.Column(db.Boolean, default=False)
    
    # Relationships
    assignment = db.relationship('Assignment', back_populates='submissions')
    student = db.relationship('User', back_populates='submissions')
    grade = db.relationship('Grade', back_populates='submission', uselist=False, cascade='all, delete-orphan')


class Grade(db.Model):
    """Grade model"""
    __tablename__ = 'grades'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    submission_id = db.Column(UUID(as_uuid=True), db.ForeignKey('submissions.id', ondelete='CASCADE'), nullable=False, unique=True)
    score = db.Column(db.Integer, nullable=False)
    feedback = db.Column(db.Text)
    graded_by_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id', ondelete='SET NULL'))
    graded_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    submission = db.relationship('Submission', back_populates='grade')
    grader = db.relationship('User', foreign_keys=[graded_by_id], back_populates='graded_submissions')


# =========================
# COMMUNICATION
# =========================

class Announcement(db.Model):
    """Announcement model"""
    __tablename__ = 'announcements'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    batch_id = db.Column(UUID(as_uuid=True), db.ForeignKey('batches.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_by_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id', ondelete='SET NULL'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    batch = db.relationship('Batch', back_populates='announcements')
    created_by = db.relationship('User')


class Notification(db.Model):
    """Notification model"""
    __tablename__ = 'notifications'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    notification_type = db.Column(db.String(50))  # 'info', 'warning', 'success', 'error'
    read = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    user = db.relationship('User', back_populates='notifications')


# =========================
# CERTIFICATES
# =========================

class Certificate(db.Model):
    """Certificate model"""
    __tablename__ = 'certificates'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    enrollment_id = db.Column(UUID(as_uuid=True), db.ForeignKey('enrollments.id', ondelete='CASCADE'), nullable=False, unique=True)
    verification_code = db.Column(db.String(100), unique=True, nullable=False, index=True)
    issued_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    certificate_url = db.Column(db.Text)  # URL to PDF
    
    # Relationships
    enrollment = db.relationship('Enrollment', back_populates='certificate')


# =========================
# STUDENT LIFECYCLE & PERFORMANCE
# =========================

class StudentProfile(db.Model):
    """Extended student profile for comprehensive tracking"""
    __tablename__ = 'student_profiles'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, unique=True)
    
    # Personal Information
    linkedin_url = db.Column(db.String(255))
    github_url = db.Column(db.String(255))
    portfolio_url = db.Column(db.String(255))
    resume_url = db.Column(db.Text)
    
    # Academic Background
    highest_education = db.Column(db.String(100))
    field_of_study = db.Column(db.String(100))
    work_experience_years = db.Column(db.Integer, default=0)
    
    # Current Status
    current_rag_rating = db.Column(db.Enum(RAGRating), default=RAGRating.GREEN)
    overall_performance_score = db.Column(db.Float, default=0.0)  # 0-100
    attendance_percentage = db.Column(db.Float, default=0.0)
    engagement_score = db.Column(db.Float, default=0.0)  # Participation metric
    
    # Career Support
    job_search_status = db.Column(db.String(50))  # 'active', 'placed', 'not_started'
    target_role = db.Column(db.String(100))
    expected_salary = db.Column(db.String(50))
    placement_date = db.Column(db.Date)
    
    # Emergency Contact
    emergency_contact_name = db.Column(db.String(255))
    emergency_contact_phone = db.Column(db.String(20))
    emergency_contact_relationship = db.Column(db.String(50))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('profile', uselist=False))
    performance_reviews = db.relationship('PerformanceReview', back_populates='student_profile', cascade='all, delete-orphan')
    portfolio_items = db.relationship('PortfolioItem', back_populates='student_profile', cascade='all, delete-orphan')
    job_applications = db.relationship('JobApplication', back_populates='student_profile', cascade='all, delete-orphan')


class PerformanceReview(db.Model):
    """Regular performance reviews for students"""
    __tablename__ = 'performance_reviews'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_profile_id = db.Column(UUID(as_uuid=True), db.ForeignKey('student_profiles.id', ondelete='CASCADE'), nullable=False)
    reviewer_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id', ondelete='SET NULL'))
    
    rag_rating = db.Column(db.Enum(RAGRating), nullable=False)
    technical_skills = db.Column(db.Integer)  # 1-10
    soft_skills = db.Column(db.Integer)  # 1-10
    attendance = db.Column(db.Integer)  # 1-10
    participation = db.Column(db.Integer)  # 1-10
    
    strengths = db.Column(db.Text)
    areas_for_improvement = db.Column(db.Text)
    action_plan = db.Column(db.Text)
    next_review_date = db.Column(db.Date)
    
    review_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    student_profile = db.relationship('StudentProfile', back_populates='performance_reviews')
    reviewer = db.relationship('User')


# =========================
# PROJECT-BASED LEARNING
# =========================

class Project(db.Model):
    """Capstone and milestone projects"""
    __tablename__ = 'projects'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    bootcamp_id = db.Column(UUID(as_uuid=True), db.ForeignKey('bootcamps.id', ondelete='CASCADE'), nullable=False)
    
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.Text)
    deadline = db.Column(db.DateTime, nullable=False)
    max_score = db.Column(db.Integer, default=100)
    is_capstone = db.Column(db.Boolean, default=False)
    
    # Evaluation Criteria
    rubric = db.Column(db.JSON)  # JSON structure for grading rubric
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    bootcamp = db.relationship('Bootcamp')
    project_submissions = db.relationship('ProjectSubmission', back_populates='project', cascade='all, delete-orphan')


class ProjectSubmission(db.Model):
    """Student project submissions"""
    __tablename__ = 'project_submissions'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = db.Column(UUID(as_uuid=True), db.ForeignKey('projects.id', ondelete='CASCADE'), nullable=False)
    student_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    
    status = db.Column(db.Enum(ProjectStatus), default=ProjectStatus.NOT_STARTED)
    
    # Submission Details
    github_url = db.Column(db.String(255))
    demo_url = db.Column(db.String(255))
    video_url = db.Column(db.String(255))
    documentation_url = db.Column(db.String(255))
    description = db.Column(db.Text)
    
    submitted_at = db.Column(db.DateTime)
    is_late = db.Column(db.Boolean, default=False)
    
    # Feedback
    score = db.Column(db.Integer)
    feedback = db.Column(db.Text)
    reviewed_by_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id', ondelete='SET NULL'))
    reviewed_at = db.Column(db.DateTime)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    project = db.relationship('Project', back_populates='project_submissions')
    student = db.relationship('User', foreign_keys=[student_id])
    reviewer = db.relationship('User', foreign_keys=[reviewed_by_id])


# =========================
# PORTFOLIO MANAGEMENT
# =========================

class PortfolioItem(db.Model):
    """Student portfolio items"""
    __tablename__ = 'portfolio_items'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_profile_id = db.Column(UUID(as_uuid=True), db.ForeignKey('student_profiles.id', ondelete='CASCADE'), nullable=False)
    
    item_type = db.Column(db.Enum(PortfolioItemType), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    
    # Links
    github_url = db.Column(db.String(255))
    demo_url = db.Column(db.String(255))
    image_url = db.Column(db.String(255))
    
    # Technologies Used
    technologies = db.Column(db.JSON)  # Array of tech stack
    
    # Metrics
    is_featured = db.Column(db.Boolean, default=False)
    display_order = db.Column(db.Integer, default=0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    student_profile = db.relationship('StudentProfile', back_populates='portfolio_items')


# =========================
# CAREER SUPPORT & JOB PLACEMENT
# =========================

class JobApplication(db.Model):
    """Track student job applications"""
    __tablename__ = 'job_applications'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_profile_id = db.Column(UUID(as_uuid=True), db.ForeignKey('student_profiles.id', ondelete='CASCADE'), nullable=False)
    
    company_name = db.Column(db.String(255), nullable=False)
    position = db.Column(db.String(255), nullable=False)
    job_url = db.Column(db.String(255))
    
    status = db.Column(db.Enum(JobApplicationStatus), default=JobApplicationStatus.APPLIED)
    applied_date = db.Column(db.Date, nullable=False)
    
    # Interview tracking
    interview_date = db.Column(db.DateTime)
    interview_notes = db.Column(db.Text)
    
    # Outcome
    offer_received = db.Column(db.Boolean, default=False)
    offer_amount = db.Column(db.Numeric(10, 2))
    accepted = db.Column(db.Boolean)
    
    notes = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    student_profile = db.relationship('StudentProfile', back_populates='job_applications')


class AlumniNetwork(db.Model):
    """Alumni information and networking"""
    __tablename__ = 'alumni_network'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    
    current_company = db.Column(db.String(255))
    current_position = db.Column(db.String(255))
    current_salary_range = db.Column(db.String(50))
    
    graduation_date = db.Column(db.Date, nullable=False)
    
    # Networking
    available_for_mentorship = db.Column(db.Boolean, default=False)
    available_for_referrals = db.Column(db.Boolean, default=False)
    
    success_story = db.Column(db.Text)
    testimonial = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User')


# =========================
# SURVEYS & FEEDBACK
# =========================

class Survey(db.Model):
    """Instructor evaluations and course feedback"""
    __tablename__ = 'surveys'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    batch_id = db.Column(UUID(as_uuid=True), db.ForeignKey('batches.id', ondelete='CASCADE'), nullable=False)
    instructor_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id', ondelete='SET NULL'))
    
    survey_type = db.Column(db.Enum(SurveyType), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    
    questions = db.Column(db.JSON)  # Array of question objects
    
    is_anonymous = db.Column(db.Boolean, default=True)
    is_active = db.Column(db.Boolean, default=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    closes_at = db.Column(db.DateTime)
    
    # Relationships
    batch = db.relationship('Batch')
    instructor = db.relationship('User')
    responses = db.relationship('SurveyResponse', back_populates='survey', cascade='all, delete-orphan')


class SurveyResponse(db.Model):
    """Student survey responses"""
    __tablename__ = 'survey_responses'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    survey_id = db.Column(UUID(as_uuid=True), db.ForeignKey('surveys.id', ondelete='CASCADE'), nullable=False)
    student_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id', ondelete='CASCADE'))
    
    responses = db.Column(db.JSON)  # Array of answer objects matching questions
    
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    survey = db.relationship('Survey', back_populates='responses')
    student = db.relationship('User')


# =========================
# COMMUNICATION ENHANCEMENTS
# =========================

class Message(db.Model):
    """Direct messaging between users"""
    __tablename__ = 'messages'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sender_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    recipient_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    
    subject = db.Column(db.String(255))
    message = db.Column(db.Text, nullable=False)
    
    is_read = db.Column(db.Boolean, default=False)
    read_at = db.Column(db.DateTime)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    sender = db.relationship('User', foreign_keys=[sender_id])
    recipient = db.relationship('User', foreign_keys=[recipient_id])


class DiscussionForum(db.Model):
    """Discussion forums for batches"""
    __tablename__ = 'discussion_forums'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    batch_id = db.Column(UUID(as_uuid=True), db.ForeignKey('batches.id', ondelete='CASCADE'), nullable=False)
    
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    
    created_by_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id', ondelete='SET NULL'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    batch = db.relationship('Batch')
    created_by = db.relationship('User')
    posts = db.relationship('ForumPost', back_populates='forum', cascade='all, delete-orphan')


class ForumPost(db.Model):
    """Posts in discussion forums"""
    __tablename__ = 'forum_posts'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    forum_id = db.Column(UUID(as_uuid=True), db.ForeignKey('discussion_forums.id', ondelete='CASCADE'), nullable=False)
    author_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    parent_post_id = db.Column(UUID(as_uuid=True), db.ForeignKey('forum_posts.id', ondelete='CASCADE'))
    
    content = db.Column(db.Text, nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    forum = db.relationship('DiscussionForum', back_populates='posts')
    author = db.relationship('User')
    parent_post = db.relationship('ForumPost', remote_side=[id], backref='replies')


# =========================
# DOCUMENT MANAGEMENT
# =========================

class Document(db.Model):
    """Student document storage (onboarding, agreements, etc.)"""
    __tablename__ = 'documents'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    enrollment_id = db.Column(UUID(as_uuid=True), db.ForeignKey('enrollments.id', ondelete='CASCADE'))
    
    document_type = db.Column(db.String(100), nullable=False)  # 'id_proof', 'agreement', 'resume'
    document_name = db.Column(db.String(255), nullable=False)
    document_url = db.Column(db.Text, nullable=False)
    
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    verified = db.Column(db.Boolean, default=False)
    verified_by_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id', ondelete='SET NULL'))
    verified_at = db.Column(db.DateTime)
    
    # Relationships
    user = db.relationship('User', foreign_keys=[user_id])
    enrollment = db.relationship('Enrollment')
    verified_by = db.relationship('User', foreign_keys=[verified_by_id])

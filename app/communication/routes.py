"""
Communication & Survey Routes
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from sqlalchemy import desc, or_
from datetime import datetime
from app.extensions import db
from app.models import (
    Message, DiscussionForum, ForumPost, Survey, SurveyResponse,
    SurveyType, Batch, User, UserRole, Notification
)
from app.auth.utils import role_required

bp = Blueprint('communication', __name__, url_prefix='/communication')


# =========================
# MESSAGING
# =========================

@bp.route('/messages')
@login_required
def inbox():
    """View inbox"""
    messages = Message.query.filter_by(
        recipient_id=current_user.id
    ).order_by(desc(Message.created_at)).all()
    
    sent_messages = Message.query.filter_by(
        sender_id=current_user.id
    ).order_by(desc(Message.created_at)).all()
    
    unread_count = sum(1 for m in messages if not m.is_read)
    
    return render_template('communication/inbox.html',
                         messages=messages,
                         sent_messages=sent_messages,
                         unread_count=unread_count)


@bp.route('/messages/send', methods=['GET', 'POST'])
@login_required
def send_message():
    """Send a message"""
    if request.method == 'POST':
        recipient_id = request.form.get('recipient_id')
        
        message = Message(
            sender_id=current_user.id,
            recipient_id=recipient_id,
            subject=request.form.get('subject', '').strip(),
            message=request.form.get('message').strip()
        )
        
        db.session.add(message)
        
        # Create notification
        notification = Notification(
            user_id=recipient_id,
            title='New Message',
            message=f'You have a new message from {current_user.full_name}',
            notification_type='info'
        )
        db.session.add(notification)
        
        db.session.commit()
        
        flash('Message sent successfully!', 'success')
        return redirect(url_for('communication.inbox'))
    
    # Get potential recipients
    if current_user.role == UserRole.STUDENT:
        # Students can message instructors and admins
        recipients = User.query.filter(
            User.role.in_([UserRole.ADMIN, UserRole.INSTRUCTOR, UserRole.MENTOR])
        ).all()
    else:
        # Staff can message anyone
        recipients = User.query.filter(User.id != current_user.id).all()
    
    return render_template('communication/send_message.html', recipients=recipients)


@bp.route('/messages/<uuid:message_id>')
@login_required
def view_message(message_id):
    """View a message"""
    message = db.session.get(Message, message_id)
    if not message:
        flash('Message not found', 'error')
        return redirect(url_for('communication.inbox'))
    
    # Check permission
    if message.recipient_id != current_user.id and message.sender_id != current_user.id:
        flash('Unauthorized', 'error')
        return redirect(url_for('communication.inbox'))
    
    # Mark as read
    if message.recipient_id == current_user.id and not message.is_read:
        message.is_read = True
        message.read_at = datetime.utcnow()
        db.session.commit()
    
    return render_template('communication/view_message.html', message=message)


# =========================
# DISCUSSION FORUMS
# =========================

@bp.route('/forums')
@login_required
def list_forums():
    """List all forums"""
    if current_user.role == UserRole.STUDENT:
        # Get forums for student's batches
        from app.models import Enrollment
        enrollments = Enrollment.query.filter_by(student_id=current_user.id).all()
        batch_ids = [e.batch_id for e in enrollments]
        forums = DiscussionForum.query.filter(DiscussionForum.batch_id.in_(batch_ids)).all()
    else:
        forums = DiscussionForum.query.order_by(desc(DiscussionForum.created_at)).all()
    
    return render_template('communication/forums.html', forums=forums)


@bp.route('/forums/create', methods=['GET', 'POST'])
@login_required
@role_required([UserRole.ADMIN, UserRole.INSTRUCTOR])
def create_forum():
    """Create a new forum"""
    if request.method == 'POST':
        forum = DiscussionForum(
            batch_id=request.form.get('batch_id'),
            title=request.form.get('title').strip(),
            description=request.form.get('description', '').strip(),
            created_by_id=current_user.id
        )
        
        db.session.add(forum)
        db.session.commit()
        
        flash('Forum created successfully!', 'success')
        return redirect(url_for('communication.list_forums'))
    
    batches = Batch.query.all()
    return render_template('communication/create_forum.html', batches=batches)


@bp.route('/forums/<uuid:forum_id>')
@login_required
def view_forum(forum_id):
    """View forum and posts"""
    forum = db.session.get(DiscussionForum, forum_id)
    if not forum:
        flash('Forum not found', 'error')
        return redirect(url_for('communication.list_forums'))
    
    # Get root posts (not replies)
    posts = ForumPost.query.filter_by(
        forum_id=forum_id,
        parent_post_id=None
    ).order_by(desc(ForumPost.created_at)).all()
    
    return render_template('communication/view_forum.html', forum=forum, posts=posts)


@bp.route('/forums/<uuid:forum_id>/post', methods=['POST'])
@login_required
def create_post(forum_id):
    """Create a forum post"""
    forum = db.session.get(DiscussionForum, forum_id)
    if not forum:
        flash('Forum not found', 'error')
        return redirect(url_for('communication.list_forums'))
    
    parent_post_id = request.form.get('parent_post_id')
    
    post = ForumPost(
        forum_id=forum_id,
        author_id=current_user.id,
        parent_post_id=parent_post_id if parent_post_id else None,
        content=request.form.get('content').strip()
    )
    
    db.session.add(post)
    db.session.commit()
    
    flash('Post created successfully!', 'success')
    return redirect(url_for('communication.view_forum', forum_id=forum_id))


# =========================
# SURVEYS
# =========================

@bp.route('/surveys')
@login_required
def list_surveys():
    """List available surveys"""
    if current_user.role == UserRole.STUDENT:
        # Get surveys for student's batches
        from app.models import Enrollment
        enrollments = Enrollment.query.filter_by(student_id=current_user.id).all()
        batch_ids = [e.batch_id for e in enrollments]
        surveys = Survey.query.filter(
            Survey.batch_id.in_(batch_ids),
            Survey.is_active == True
        ).all()
        
        # Check which surveys have been completed
        survey_data = []
        for survey in surveys:
            response = SurveyResponse.query.filter_by(
                survey_id=survey.id,
                student_id=current_user.id
            ).first()
            survey_data.append({
                'survey': survey,
                'completed': response is not None
            })
        
        return render_template('communication/student_surveys.html', survey_data=survey_data)
    else:
        # Admins/instructors see all surveys
        surveys = Survey.query.order_by(desc(Survey.created_at)).all()
        return render_template('communication/admin_surveys.html', surveys=surveys)


@bp.route('/surveys/create', methods=['GET', 'POST'])
@login_required
@role_required([UserRole.ADMIN, UserRole.INSTRUCTOR])
def create_survey():
    """Create a new survey"""
    if request.method == 'POST':
        # Parse questions JSON
        import json
        questions_json = request.form.get('questions', '[]')
        questions = json.loads(questions_json)
        
        survey = Survey(
            batch_id=request.form.get('batch_id'),
            instructor_id=request.form.get('instructor_id') if request.form.get('instructor_id') else None,
            survey_type=SurveyType[request.form.get('survey_type').upper()],
            title=request.form.get('title').strip(),
            description=request.form.get('description', '').strip(),
            questions=questions,
            is_anonymous=request.form.get('is_anonymous') == 'on'
        )
        
        # Set closing date if provided
        closes_at = request.form.get('closes_at')
        if closes_at:
            survey.closes_at = datetime.strptime(closes_at, '%Y-%m-%dT%H:%M')
        
        db.session.add(survey)
        db.session.commit()
        
        flash('Survey created successfully!', 'success')
        return redirect(url_for('communication.list_surveys'))
    
    batches = Batch.query.all()
    instructors = User.query.filter_by(role=UserRole.INSTRUCTOR).all()
    
    return render_template('communication/create_survey.html',
                         batches=batches,
                         instructors=instructors)


@bp.route('/surveys/<uuid:survey_id>/take', methods=['GET', 'POST'])
@login_required
@role_required([UserRole.STUDENT])
def take_survey(survey_id):
    """Take a survey"""
    survey = db.session.get(Survey, survey_id)
    if not survey:
        flash('Survey not found', 'error')
        return redirect(url_for('communication.list_surveys'))
    
    # Check if already completed
    existing_response = SurveyResponse.query.filter_by(
        survey_id=survey_id,
        student_id=current_user.id
    ).first()
    
    if existing_response:
        flash('You have already completed this survey', 'info')
        return redirect(url_for('communication.list_surveys'))
    
    if request.method == 'POST':
        # Parse responses
        import json
        responses_json = request.form.get('responses', '[]')
        responses = json.loads(responses_json)
        
        response = SurveyResponse(
            survey_id=survey_id,
            student_id=current_user.id if not survey.is_anonymous else None,
            responses=responses
        )
        
        db.session.add(response)
        db.session.commit()
        
        flash('Thank you for completing the survey!', 'success')
        return redirect(url_for('communication.list_surveys'))
    
    return render_template('communication/take_survey.html', survey=survey)


@bp.route('/surveys/<uuid:survey_id>/results')
@login_required
@role_required([UserRole.ADMIN, UserRole.INSTRUCTOR])
def survey_results(survey_id):
    """View survey results"""
    survey = db.session.get(Survey, survey_id)
    if not survey:
        flash('Survey not found', 'error')
        return redirect(url_for('communication.list_surveys'))
    
    responses = SurveyResponse.query.filter_by(survey_id=survey_id).all()
    
    # Analyze responses
    total_responses = len(responses)
    
    return render_template('communication/survey_results.html',
                         survey=survey,
                         responses=responses,
                         total_responses=total_responses)

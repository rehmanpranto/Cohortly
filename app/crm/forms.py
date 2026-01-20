from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateTimeField, SubmitField
from wtforms.validators import DataRequired, Email, Optional

class LeadForm(FlaskForm):
    """Form for creating/editing leads."""
    full_name = StringField('Full Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired()])
    source = StringField('Source', validators=[Optional()])
    notes = TextAreaField('Notes', validators=[Optional()])
    submit = SubmitField('Create Lead')

class LeadLogForm(FlaskForm):
    """Form for adding call logs to leads."""
    note = TextAreaField('Call Notes', validators=[DataRequired()])
    next_follow_up = DateTimeField('Next Follow-up Date', validators=[Optional()], format='%Y-%m-%d %H:%M')
    submit = SubmitField('Add Log')

class LeadStatusForm(FlaskForm):
    """Form for updating lead status."""
    status = SelectField('Status', 
                        choices=[
                            ('new', 'New'),
                            ('contacted', 'Contacted'),
                            ('qualified', 'Qualified'),
                            ('converted', 'Converted'),
                            ('lost', 'Lost')
                        ],
                        validators=[DataRequired()])
    submit = SubmitField('Update Status')

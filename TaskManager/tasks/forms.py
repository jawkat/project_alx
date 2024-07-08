""" forms tasks """
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, TextAreaField, SelectField, DateField)
from wtforms.validators import DataRequired, Length






class CreateTaskForm(FlaskForm):
    """Form to create """
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=255)])
    description = TextAreaField('Description')
    status = SelectField('Status', choices=[
        ('in progress', 'In Progress'), ('completed','Completed'),('pending', 'Pending')
        ], default='in progress')
    priority = SelectField('Priority', choices=[('low', 'Low'), ('medium', 'Medium'),
                                                ('high', 'High')], default='medium')
    due_date = DateField(
        'Due Date', validators=[DataRequired()], default=datetime.utcnow ,format='%Y-%m-%d')
    submit = SubmitField('Save Task')

class UpdateTaskForm(FlaskForm):
    """Form to update a task"""
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=255)])
    description = TextAreaField('Description')
    status = SelectField('Status', choices=[
        ('in progress', 'In Progress'), ('completed','Completed'),('pending', 'Pending')
        ], default='in progress')
    priority = SelectField('Priority', choices=[('low', 'Low'), ('medium', 'Medium'),
                                                ('high', 'High')], default='medium')
    due_date = DateField(
        'Due Date', validators=[DataRequired()], default=datetime.utcnow ,format='%Y-%m-%d')
    submit = SubmitField('Update Task')


class NoteForm(FlaskForm):
    """Form to create or update a note"""
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Save Note')

class NoteFormUpdate(FlaskForm):
    """Form to create or update a note"""
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Update Note')





class TaskCollaboratorForm(FlaskForm):
    """Form to add a collaborator to a task"""
    user_id = SelectField('User', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Add Collaborator')

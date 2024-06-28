from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, DateField

from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from TaskManager.models import User, Task


class RegistrationUserForm(FlaskForm):
    """ Regstration form """
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    """ Login form """
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    """ Regstration form """
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Update')

    def validate_username(self, username):
        """Validate username on account update"""
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        """Validate email on account update"""
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

class TaskForm(FlaskForm):
    """Form to create or update a task"""
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=255)])
    description = TextAreaField('Description')
    status = SelectField('Status', choices=[
        ('in progress', 'In Progress'), ('completed','Completed'),('pending', 'Pending')
        ], default='in progress')
    priority = SelectField('Priority', choices=[('low', 'Low'), ('medium', 'Medium'),
                                                ('high', 'High')], default='medium')
    due_date = DateField('Due Date', validators=[DataRequired()], format='%Y-%m-%d')
    submit = SubmitField('Save Task')




class NoteForm(FlaskForm):
    """Form to create or update a note"""
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Save Note')

class TaskCollaboratorForm(FlaskForm):
    """Form to add a collaborator to a task"""
    user_id = SelectField('User', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Add Collaborator')

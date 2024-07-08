""" Models """
from datetime import datetime
from flask_login import UserMixin
from flask import current_app
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
from TaskManager import db, login_manager





@login_manager.user_loader
def load_user(user_id):
    """Standard user loader function from Flask-Login documentation"""
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    """User class"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    date_joined = db.Column(db.DateTime, default=datetime.now)
    last_login = db.Column(db.DateTime, default=datetime.now)
    tasks = db.relationship('Task', backref='user', lazy=True)
    task_collaborators = db.relationship('TaskCollaborator', backref='user', lazy=True)



    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id})

    @staticmethod
    def verify_reset_token(token,expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token,max_age=expires_sec)['user_id']
        except Exception:
            return None
        return User.query.get(user_id)




    # def get_reset(self):
    #     serial =  Serializer(current_app.config['SECRET_KEY'])
    #     return serial.dumps({'user_id': self.id}).decode('utf-8')

    # @staticmethod
    # def verify_token(token, expiration=1800):
    #     serial = Serializer(current_app.config['SECRET_KEY'], expiration)
    #     try:
    #         user_id = serial.loads(token)['user_id']
    #     except :
    #         return None

    #     return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Task(db.Model):
    """Task class"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.Enum('in progress', 'completed', 'pending'), default='in progress')
    priority = db.Column(db.Enum('low', 'medium', 'high'), default='medium')
    due_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    notes = db.relationship(
        'Note', backref='task', lazy=True, cascade='all, delete-orphan')

    task_collaborators = db.relationship(
        'TaskCollaborator', backref='task', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f"Task('{self.title}', '{self.status}', '{self.priority}')"


class Note(db.Model):
    """Note class"""
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"Note for Task ID('{self.task_id}')"


class TaskCollaborator(db.Model):
    """TaskCollaborator class"""
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"TaskCollaborator(Task ID: '{self.task_id}', User ID: '{self.user_id}')"

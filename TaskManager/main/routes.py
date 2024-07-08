""" main routes"""

from flask import render_template, Blueprint
from flask_login import  current_user, login_required
from sqlalchemy import func
from TaskManager.models import Task,TaskCollaborator
from TaskManager import db



main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    """Route to display all tasks on the home page."""
    return render_template('home.html')


@main.route("/dashbord")
@login_required
def dashbord():
    """ Home page display some indicators dashbord """
   # Count total tasks for the current user
    num_tasks = Task.query.filter_by(user_id=current_user.id).count()

    # Count tasks by status for the current user
    status_counts = db.session.query(Task.status, func.count(Task.id)).filter_by(user_id=current_user.id).group_by(Task.status).all()
    num_tasks_by_status = {status: count for status, count in status_counts}

    # Count distinct collaborators for the current user's tasks
    num_collaborators = db.session.query(
        func.count(func.distinct(TaskCollaborator.user_id))).filter(
            TaskCollaborator.task_id.in_(
        db.session.query(Task.id).filter_by(user_id=current_user.id)
    )
).scalar()

    return render_template('dashbord.html', title='Dashbord', num_tasks=num_tasks,
                           num_tasks_by_status=num_tasks_by_status,
                           num_collaborators=num_collaborators)

@main.route("/about")
def about():
    """Route to display the about page."""
    return render_template('about.html', title='About')

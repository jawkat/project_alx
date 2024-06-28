from datetime import datetime
from flask import render_template, url_for, flash, redirect, request,abort
from TaskManager import app, db, bcrypt
from TaskManager.forms import RegistrationUserForm, LoginForm, UpdateAccountForm, TaskForm, NoteForm, TaskCollaboratorForm
from TaskManager.models import User, Task, Note, TaskCollaborator
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import func


@app.route("/")
@app.route("/welcome")
def welcome():
    """Route to display all tasks on the home page."""
    return render_template('welcome.html')


@app.route("/home")
@login_required
def home():
    # Query statistics
    num_tasks = Task.query.count()

    # Count tasks by status
    status_counts = db.session.query(Task.status, func.count(Task.id)).group_by(Task.status).all()
    num_tasks_by_status = {status: count for status, count in status_counts}

    # Count collaborators
    num_collaborators = TaskCollaborator.query.distinct(TaskCollaborator.user_id).count()

    # Render template with statistics
    return render_template('home.html', title='Home', num_tasks=num_tasks,
                           num_tasks_by_status=num_tasks_by_status,
                           num_collaborators=num_collaborators)

@app.route("/about")
def about():
    """Route to display the about page."""
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    """Route to handle user registration."""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationUserForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pwd)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    """Route to handle user login."""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Login successful.', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    """Route to handle user logout."""
    logout_user()
    return redirect(url_for('home'))

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    """Route to handle account updates."""
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        if current_user.is_authenticated:
            form.username.data = current_user.username
            form.email.data = current_user.email
    return render_template('account.html', title='Account', form=form)

@app.route("/tasks")
@login_required
def all_tasks():
    """Route to display all tasks on the home page."""
    tasks = current_user.tasks
    return render_template('all_tasks.html', tasks=tasks)

@app.route("/task/new", methods=['GET', 'POST'])
@login_required
def new_task():
    """Route to create a new task."""
    form = TaskForm()
    if form.validate_on_submit():
        due_date = form.due_date.data
        task = Task(
            title=form.title.data, description=form.description.data, status=form.status.data,
            priority=form.priority.data, due_date=due_date,user_id=current_user.id,
            created_at=datetime.utcnow(), updated_at=datetime.utcnow())

        db.session.add(task)
        db.session.commit()
        flash('Your task has been created!', 'success')
        return redirect(url_for('all_tasks'))
    return render_template('create_task.html', title='New Task', form=form)

@app.route("/task/<int:task_id>")
def task(task_id):
    """Route to view a specific task."""
    task = Task.query.get_or_404(task_id)
    return render_template('task.html', title=task.title, task=task)

@app.route("/task/<int:task_id>/update", methods=['GET', 'POST'])
@login_required
def update_task(task_id):
    """Route to update an existing task."""
    task = Task.query.get_or_404(task_id)
    if task.user != current_user:
        abort(403)  # Forbidden error, user is not the owner of the task
    form = TaskForm()
    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.status = form.status.data
        task.priority = form.priority.data
        task.due_date = form.due_date.data
        task.updated_at = datetime.utcnow()
        db.session.commit()
        flash('Your task has been updated!', 'success')
        return redirect(url_for('task', task_id=task.id))
    elif request.method == 'GET':
        form.title.data = task.title
        form.description.data = task.description
        form.status.data = task.status
        form.priority.data = task.priority
        form.due_date.data = task.due_date
    return render_template('create_task.html', title='Update Task', form=form)

@app.route("/task/<int:task_id>/delete", methods=['POST'])
@login_required
def delete_task(task_id):
    """Route to delete an existing task."""
    task = Task.query.get_or_404(task_id)
    if task.user != current_user:
        abort(403)  # Forbidden error, user is not the owner of the task

    Note.query.filter_by(task_id=task.id).delete()
    TaskCollaborator.query.filter_by(task_id=task.id).delete()

    db.session.delete(task)
    db.session.commit()
    flash('Your task has been deleted!', 'success')
    return redirect(url_for('all_tasks'))



@app.route("/note/new/<int:task_id>", methods=['GET', 'POST'])
@login_required
def new_note(task_id):
    """Route to create a new note for a specific task."""
    form = NoteForm()
    if form.validate_on_submit():
        note = Note(content=form.content.data, task_id=task_id)
        db.session.add(note)
        db.session.commit()
        flash('Your note has been created!', 'success')
        return redirect(url_for('task', task_id=task_id))
    return render_template('create_note.html', title='New Note', form=form)

@app.route("/collaborator/new/<int:task_id>", methods=['GET', 'POST'])
@login_required
def new_collaborator(task_id):
    """Route to add a new collaborator to a specific task."""
    form = TaskCollaboratorForm()
    form.user_id.choices = [(user.id, user.username) for user in User.query.all()]

    if form.validate_on_submit():
        user_id = form.user_id.data

        # Check if the collaborator already exists for this task
        existing_collaborator = TaskCollaborator.query.filter_by(task_id=task_id, user_id=user_id).first()
        if existing_collaborator:
            flash('This collaborator is already added to the task.', 'warning')
            return redirect(url_for('task', task_id=task_id))

        # If collaborator doesn't exist, add them
        collaborator = TaskCollaborator(task_id=task_id, user_id=user_id)
        db.session.add(collaborator)
        db.session.commit()

        flash('Collaborator has been added!', 'success')
        return redirect(url_for('task', task_id=task_id))

    return render_template('create_collaborator.html', title='Add Collaborator', form=form)

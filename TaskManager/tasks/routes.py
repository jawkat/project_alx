""" tasks routes """


from datetime import datetime
from flask import render_template, url_for, flash, redirect, request,abort , Blueprint
from flask_login import current_user, login_required
from TaskManager import db
from TaskManager.tasks.forms import (CreateTaskForm, UpdateTaskForm,
                               NoteForm, TaskCollaboratorForm,NoteFormUpdate)

from TaskManager.models import User, Task, Note, TaskCollaborator






tasks = Blueprint('tasks', __name__)

@tasks.route("/tasks")
@login_required
def all_tasks():
    """Route to display all tasks on the home page."""
    tasks = current_user.tasks
    return render_template('all_tasks.html', tasks=tasks)

@tasks.route("/task/new", methods=['GET', 'POST'])
@login_required
def new_task():
    """Route to create a new task."""
    form = CreateTaskForm()
    if form.validate_on_submit():
        task = Task(
            title=form.title.data, description=form.description.data, status=form.status.data,
            priority=form.priority.data, due_date=form.due_date.data,user_id=current_user.id,
            created_at=datetime.utcnow(), updated_at=datetime.utcnow())

        db.session.add(task)
        db.session.commit()
        flash('Your task has been created!', 'success')
        return redirect(url_for('tasks.all_tasks'))
    return render_template('create_task.html', title='New Task', form=form)



@tasks.route("/task/<int:task_id>")
def task(task_id):
    """Route to view a specific task."""

    if not current_user.is_authenticated:
        flash('You need to be logged in to access this page.', 'warning')
        return redirect(url_for('users.login'))

    # get all related data with task (notes and collborators)
    task = Task.query.get_or_404(task_id)

        # Find the previous task
    previous_task = Task.query.filter(
        Task.id < task_id, Task.user_id == current_user.id).order_by(Task.id.desc()).first()


    # Find the next task
    next_task = Task.query.filter(
        Task.id > task_id, Task.user_id == current_user.id).order_by(Task.id.asc()).first()

    return render_template('task.html',
                           title=task.title,
                           task=task,
                           previous_task=previous_task,
                           next_task=next_task)

@tasks.route("/task/<int:task_id>/update", methods=['GET', 'POST'])
@login_required
def update_task(task_id):
    """Route to update an existing task."""
    task = Task.query.get_or_404(task_id)
    if task.user != current_user:
        abort(403)  # Forbidden error, user is not the owner of the task
    form = UpdateTaskForm()
    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.status = form.status.data
        task.priority = form.priority.data
        task.due_date = form.due_date.data
        task.updated_at = datetime.utcnow()
        db.session.commit()
        flash('Your task has been updated!', 'success')
        return redirect(url_for('tasks.task', task_id=task.id))
    elif request.method == 'GET':
        form.title.data = task.title
        form.description.data = task.description
        form.status.data = task.status
        form.priority.data = task.priority
        form.due_date.data = task.due_date
    return render_template('create_task.html', title='Update Task', form=form)

@tasks.route("/task/<int:task_id>/delete", methods=['POST'])
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
    return redirect(url_for('tasks.all_tasks'))



@tasks.route("/note/new/<int:task_id>", methods=['GET', 'POST'])
@login_required
def new_note(task_id):
    """Route to create a new note for a specific task."""
    form = NoteForm()
    if form.validate_on_submit():
        note = Note(content=form.content.data, task_id=task_id)
        db.session.add(note)
        db.session.commit()
        flash('Your note has been created!', 'success')
        return redirect(url_for('tasks.task', task_id=task_id))
    return render_template('create_note.html', title='New Note', form=form)

@tasks.route("/collaborator/new/<int:task_id>", methods=['GET', 'POST'])
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
            return redirect(url_for('tasks.task', task_id=task_id))

        # If collaborator doesn't exist, add them
        collaborator = TaskCollaborator(task_id=task_id, user_id=user_id)
        db.session.add(collaborator)
        db.session.commit()

        flash('Collaborator has been added!', 'success')
        return redirect(url_for('tasks.task', task_id=task_id))

    return render_template('create_collaborator.html', title='Add Collaborator', form=form)

@tasks.route("/note/<int:note_id>/update", methods=['GET', 'POST'])
@login_required
def update_note(note_id):
    """Route pour mettre à jour une note existante."""
    note = Note.query.get_or_404(note_id)
    task = Task.query.get_or_404(note.task_id)

    if task.user != current_user:
        abort(403)  # Erreur 403, l'utilisateur n'est pas le propriétaire de la tâche

    form = NoteFormUpdate()

    if form.validate_on_submit():
        note.content = form.content.data
        note.updated_at = datetime.utcnow()
        db.session.commit()
        flash('Votre note a été mise à jour !', 'success')
        return redirect(url_for('tasks.task', task_id=note.task_id))
    elif request.method == 'GET':
        form.content.data = note.content

    return render_template('create_note.html', title='Update Note', form=form)


@tasks.route("/note/<int:note_id>/delete", methods=['POST'])
@login_required
def remove_note(note_id):
    """Route to delete an existing note"""

    note = Note.query.get_or_404(note_id)
    task = Task.query.get_or_404(note.task_id)

    if task.user != current_user:
        abort(403)  # Forbidden error, user is not the owner of the task

    db.session.delete(note)
    db.session.commit()
    flash('Your note has been deleted!', 'success')

        # Find the previous task
    previous_task = Task.query.filter(
        Task.id < note.task_id, Task.user_id == current_user.id).order_by(Task.id.desc()).first()

    # Find the next task
    next_task = Task.query.filter(
        Task.id > note.task_id, Task.user_id == current_user.id).order_by(Task.id.asc()).first()


    return redirect(url_for('tasks.task', task_id=note.task_id,
                            title=task.title, note_id=note_id,
                            task=task,
                            previous_task=previous_task,
                            next_task=next_task))

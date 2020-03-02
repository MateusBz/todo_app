from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_required
from flask import request
from app.models import User
from app import db
from app.main.forms import EditProfileForm
from app.main.forms import TaskForm
from app.models import Task
from app.main import bp


@bp.route('/home', methods=["GET", "POST"])
@login_required
def home():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(body=form.task.data, author=current_user)
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('main.home'))
    tasks = Task.query.filter_by(user_id=current_user.id)
    return render_template('home.html', title='Home', form=form, tasks=tasks)


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


@bp.route('/edit_profile', methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
    return render_template('edit_profile.html', title='Edit Profile', form=form)


@bp.route('/delete/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return redirect(url_for('main.home'))
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('main.home'))


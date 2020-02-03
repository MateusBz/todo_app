from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from flask import request
from werkzeug.urls import url_parse
from app import app
from app.forms import LoginForm
from app.models import User


@app.route('/')
@app.route('/index')
@login_required
def index():
    user= {'username': 'Mateusz'}
    tasks = [
        'Python Learning',
        'Go swim',
        'Go to school'
    ]
    return render_template('index.html', title='Home', tasks=tasks)


@app.route('/login', methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(f'Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc !='':
            next_page = url_parse('index')
        return redirect('/index')
    return render_template('login.html', form=form, title='Sign In')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

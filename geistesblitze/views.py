from flask import render_template, redirect, flash, url_for
from flask_login import login_required, login_user, logout_user, current_user

from geistesblitze import app
from geistesblitze.forms import AddIdeaForm, LoginForm, RegisterForm
from geistesblitze.models import db, User, Idea


@app.route('/')
def index():
    return render_template('index.html', register_form=RegisterForm(), login_form=LoginForm())


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, True)
            return redirect(url_for('get_ideas'))
        flash('Invalid username of password')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('login'))


@app.route('/ideas/<int:id>')
@login_required
def get_idea(id):
    idea = Idea.query.filter_by(id=id).first()
    ideas = Idea.query.filter_by(user=current_user).all()

    if idea is None:
        return render_template('404.html'), 404
    if idea.user != current_user:
        return render_template('403.html'), 403
    return render_template('idea.html', idea=idea, ideas=ideas)


@app.route('/ideas')
@login_required
def get_ideas():
    ideas = Idea.query.filter_by(user=current_user).all()
    return render_template('ideas.html', ideas=ideas)


@app.route('/add_idea', methods=['GET', 'POST'])
@login_required
def add_idea():
    form = AddIdeaForm()

    if form.validate_on_submit():
        idea = Idea(name=form.name.data, description=form.description.data)
        idea.user = current_user
        db.session.add(idea)
        db.session.commit()
        flash('Your idea has been saved')
        return redirect(url_for('get_ideas'))
    return render_template('add_idea.html', form=form)

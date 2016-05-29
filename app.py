from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, redirect, flash, url_for
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import Form
from wtforms import PasswordField, StringField, SubmitField, TextAreaField, ValidationError
from wtforms.validators import EqualTo, DataRequired
from os.path import abspath, dirname, join

basedir = abspath(dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////{0}'.format(join(basedir, 'geistesblitze.sqlite'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128), unique=False)
    ideas = db.relationship('Idea', backref='user', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username


class Idea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=False)
    description = db.Column(db.Text(), nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Idea %r>' % self.name


class RegisterForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(),
                                                     EqualTo('password2',
                                                             message='Passwords must match.')])
    password2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class LoginForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class AddIdeaForm(Form):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Save')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, True)
            return redirect(url_for('ideas'))
        flash('Invalid username of password')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('login'))


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


@app.route('/ideas/<int:id>')
@login_required
def idea(id):
    idea = Idea.query.filter_by(id=id).first()
    ideas = Idea.query.filter_by(user=current_user).all()

    if idea is None:
        return render_template('404.html'), 404
    if idea.user != current_user:
        return render_template('403.html'), 403
    return render_template('idea.html', idea=idea, ideas=ideas)


@app.route('/ideas')
@login_required
def ideas():
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
        return redirect(url_for('ideas'))
    return render_template('add_idea.html', form=form)

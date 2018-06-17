from os.path import abspath, dirname, join

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

from geistesblitze.models import db, User

basedir = abspath(dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////%s' % join(basedir, 'geistesblitze.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

bootstrap = Bootstrap(app)

login_manager = LoginManager(app)
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'

import geistesblitze.views


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.cli.command()
def create_all():
    """Create all the tables"""
    db.create_all()

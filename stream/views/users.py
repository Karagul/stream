# -*- encoding: utf8 -*-
from flask import g, Blueprint, request, flash, render_template, session, redirect, url_for
from werkzeug import check_password_hash, generate_password_hash

from stream import db
from stream.forms import RegisterForm, LoginForm
from stream.database import User
from stream.utils import requires_login

from sqlalchemy.sql import exists as sqlalch_exists
from sqlalchemy.exc import IntegrityError

mod = Blueprint('users', __name__)

@mod.route('/')
def index():
    return redirect(url_for('general.index'))

@mod.route('/profile/')
@mod.route('/profile/<username>/')
@requires_login
def profile(username=None):
    return render_template('users/profile.html', user=g.user)

@mod.route('/database/')
@requires_login
def database():
    # get all database entries
    entries = User.query.all()
    return render_template('users/database.html', entries=entries)

@mod.before_request
def before_request():
    """ Pull user's profile from database before every request """
    g.user = None
    if 'user_email' in session:
        g.user = User.query.get(session['user_email'])

@mod.route('/logout/', methods=['GET'])
@requires_login
def logout():
    del session['user_email']
    flash('logged out!')
    return redirect(url_for('users.login'))

@mod.route('/login/', methods=['GET', 'POST'])
def login():
    """ Login form """
    if g.user is not None:
        # no need to go back to login if session already exists
        return redirect(url_for('users.profile', username=g.user.name))

    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # use Werkzeug to validate a user's password
        if user and check_password_hash(user.password, form.password.data):
            # session is signed and is thus unmodifiable, store the email
            # for session identification
            session['user_email'] = user.email
            flash('Welcome %s!' % user.name)
            return redirect(url_for('users.profile', username=user.name))
        flash('Wrong email or password', 'error-message')
    return render_template('users/login.html', form=form)

@mod.route('/register/', methods=['GET', 'POST'])
def register():
    """ User registration form """
    form = RegisterForm(request.form)

    if form.validate_on_submit():
        # Check if user already exists in database
        exists = db.session.query(sqlalch_exists().where(
                                  User.email==form.email.data)).scalar()
        if exists:
            flash('user already exists!')
            return render_template('users/register.html', form=form)

        # add new user instance to database
        user = User(name=form.name.data, email=form.email.data,
                    password=generate_password_hash(form.password.data))
        try:
            db.session.add(user)
            db.session.commit()
        except:
            flash('Unexpected error!')
            return render_template('users/register.html', form=form)

        # log the user e-mail
        session['user_email'] = user.email

        flash('You are now registered!')
        return redirect(url_for('users.profile', username=user.name))
    return render_template('users/register.html', form=form)

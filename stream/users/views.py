# -*- encoding: utf8 -*-

from flask import g, Blueprint, request, flash, render_template, session, redirect, url_for
from werkzeug import check_password_hash, generate_password_hash

from stream import db
from stream.users.forms import RegisterForm, LoginForm
from stream.users.models import User
from stream.users.decorators import requires_login

user_bp = Blueprint('users', __name__, url_prefix='/users')

@user_bp.route('/me/')
@requires_login
def home():
    return render_template('users/profile.html', user=g.user)

@user_bp.before_request
def before_request():
    """ Pull user's profile from database before every request """
    g.user = None
    if 'user_email' in session:
        print 'user_email found:', session['user_email']
        g.user = User.query.get(session['user_email'])

@user_bp.route('/login/', methods=['GET', 'POST'])
def login():
    """ Login form """
    if 'user_email' in session:
        # no need to go back to login if session already exists
        return redirect(url_for('users.home'))

    form = LoginForm(request.form)
    # ensures data is valid but does not validate passwords
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # use Werkzeug to validate a user's password
        # TODO: change to flask-login/security
        if user and check_password_hash(user.password, form.password.data):
            # session is signed and is thus unmodifiable, store the email
            # for session identification
            session['user_email'] = user.email
            flash('Welcome %s!' % user.name)
            return redirect(url_for('users.home'))
        flash('Wrong email or password', 'error-message')
    return render_template('users/login.html', form=form)

@user_bp.route('/logout/')
def logout():
    session.pop('user_email', None)
    flash('logged out!')
    return redirect(url_for('users.login'))

@user_bp.route('/register/', methods=['GET', 'POST'])
def register():
    """ User registration form """
    form = RegisterForm(request.form)

    if form.validate_on_submit():
        # add new user instance to database
        user = User(name=form.name.data, email=form.email.data,
                    password=generate_password_hash(form.password.data))
        db.session.add(user)
        db.session.commit()

        # log the user e-mail
        session['user_email'] = user.email

        flash('You are now registered!')
        return redirect(url_for('users.home'))
    return render_template('users/register.html', form=form)

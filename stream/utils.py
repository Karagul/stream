from functools import wraps

from flask import g, flash, redirect, url_for, request

def requires_login(f):
    @wraps(f)
    def wrapped_function(*args, **kwargs):
        if g.user is None:
            flash(u'You must be logged in to view this page.')
            print 'request.path:',request.path
            return redirect(url_for('users.login', next=request.path))
        return f(*args, **kwargs)
    return wrapped_function

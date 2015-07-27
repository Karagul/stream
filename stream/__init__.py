import os
import sys

from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

def install_secret_key(app, filename='secret_key'):
    """ Configure secret key from file in the instance directory.

        If the file does not exist, print instructions
        to create it from a shell with a random key,
        then exit (generate inside the app instead?).

        TODO: determine why we would ever want to do this...
        wouldn't it be easier to generate a secret key randomly
        at app startup? Then only the app knows the key in case of
        employee tampering.
    """
    filename = os.path.join(app.instance_path, filename)

    try:
        with open(filename, 'rb') as sf:
            app.config['SECRET_KEY'] = sf.read()
    except IOError:
        print('Error: No secret key. Create it with:')
        full_path = os.path.dirname(filename)
        if not os.path.isdir(full_path):
            print('mkdir -p {filename}'.format(filename=full_path))
        print('head -c 24 /dev/urandom > {filename}'.format(filename=filename))
        sys.exit(1)

if not app.config['DEBUG']:
    install_secret_key(app)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# Import and register all blueprints here:

# This also implicitly imports our SQLAlchemy db instance and models
# into namespace so that db.create_all() actually does something.
from stream.views import users
app.register_blueprint(users.mod)

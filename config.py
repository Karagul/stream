# -*- encoding: utf8 -*-

import os
_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = False

ADMINS = frozenset(['e-mail@domain.com'])
SECRET_KEY = 'secret'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'app.db')
DATABSE_CONNECT_OPTIONS = {}

THREADS_PER_PAGE = 4 # num cores * 2

CSRF_ENABLED = True
CSRF_SESSION_KEY = 'csrf-secret'

RECAPTCHA_USE_SSL = False
RECAPTCHA_PUBLIC_KEY = 'pubkey'
RECAPTCHA_PRIVATE_KEY = 'privkey'
RECAPTCHA_OPTIONS = {'theme': 'white'}

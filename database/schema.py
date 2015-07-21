# -*- encoding: utf-8 -*-
'''
    stream.database.schema
    ~~~~~~~~~~~~~~~~~~~~~

    Defines the stream application's data  schema and implements
    it in table form and as class objects.

    :copyright: (c) 2015 by Calvin Maguranis.
    :license: BSD, see LICENSE for more details.
'''
from flask.ext.sqlalchemy import SQLAlchemy as db

def userdatamodel():
    return db.Table('finance_stream',
                    db.Column('user_email', db.String(120), db.ForeignKey('user.email')),
                    db.Column('userinstitution_id', db.Integer, db.ForeignKey('userinstitution.id')),
                    db.Column('transaction_account', db.String(12), db.ForeignKey('transaction.account')),
                    db.Column('institution_id', db.Integer, db.ForeignKey('institution.id'))
                )

class User(db.Model):
    email = db.Column(db.String(120), primary_key=True)
    salt = db.Column(db.String(120), unique=True)
    hash = db.Column(db.string(120), unique=True)
    active = db.Column(db.Boolean())
    confirmedat = db.Column(db.DateTime())

    def __init__(self, email, salt, hashfunc):
        self.email = email
        self.salt = salt
        self.hash = hashfunc(str(email)+str(salt))

    def __repr__(self):
        return '<User %r>' % self.id

class UserInstitution(db.model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(255))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<UserInstitutions %r>' % self.id

class Transaction(db.model):
    account = db.Column(db.String(12), primary_key=True)
    trntype = db.Column(db.String(20))
    date = db.Column(db.DateTime)
    amount = db.Column(db.Integer(20))
    name = db.Column(db.String(32))

    def __init__(self, account):
        self.account = account

    def __repr__(self):
        return '<Transaction %r>' % self.name

class Institution(db.model):
    id = db.Column(db.Integer, primary_key=True)
    org = db.Column(db.String(64), )
    url = db.Column(db.String(255), unique=True)
    brokerid = db.Column(db.String(255))

    def __init__(self, id, org, url, brokerid):
        self.id = id
        self.org = org
        self.url = url
        self.brokerid = brokerid

    def __repr__(self):
        return '<Institution %r>' % self.id

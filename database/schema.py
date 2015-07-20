# -*- encoding: utf-8 -*-
from flask.ext.sqlalchemy import SQLAlchemy as db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    salt = db.Column(db.String(120), unique=True)
    hash = db.Column(db.string(120), unique=True)

    def __init__(self, email, salt):
        self.email = email
        self.salt = salt

    def __repr__(self):
        return '<id %r>' % self.id

class UserInstitutions(db.model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(255))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<id %r>' % self.id

class Transactions(db.model):
    account = db.Column(db.String(10), primary_key=True)
    trntype = db.Column(db.String(20))
    date = db.Column(db.String(14))
    amount = db.Column(db.Integer(20))
    name = db.Column(db.String(32))

    def __init__(self, account):
        self.account = account

    def __repr__(self):
        return '<name %r>' % self.name

class Institutions(db.model):
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
        return '<id %r>' % self.id

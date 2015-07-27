# -*- encoding: utf8 -*-

from stream import db
import constants as USER

def userdatamodel():
    return db.Table('finance_stream',
                    db.Column('user_email', db.String(120), db.ForeignKey('user.email')),
                    db.Column('userinstitution_id', db.Integer, db.ForeignKey('userinstitution.id')),
                    db.Column('transaction_account', db.String(12), db.ForeignKey('transaction.account')),
                    db.Column('institution_id', db.Integer, db.ForeignKey('institution.id')) )

class User(db.Model):
    name = db.Column(db.String(120))
    email = db.Column(db.String(120), primary_key=True)
    password = db.Column(db.String(120), unique=True)
    role = db.Column(db.SmallInteger, default=USER.USER)
    status = db.Column(db.SmallInteger, default=USER.NEW)

    def __init__(self, name=None, email=None, password=None,
                 role=None, status=None):
        self.name = name
        self.email = email
        self.password = password
        self.role = role
        self.status = status

    def getStatus(self):
          return USER.STATUS[self.status]

    def getRole(self):
        return USER.ROLE[self.role]

    def __repr__(self):
        return '<User %r>' % self.email

class UserInstitution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(255))
    institution = db.Column(db.Integer, db.Foreign_Key)

    def __init__(self, id=None, username=None, password=None):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return '<UserInstitutions %r>' % self.id

class Institution(db.Model):
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

class Transaction(db.Model):
    account = db.Column(db.String(12), primary_key=True)
    trntype = db.Column(db.String(20))
    date = db.Column(db.DateTime)
    amount = db.Column(db.Integer)
    name = db.Column(db.String(32))

    def __init__(self, account=None, trntype=None, date=None,
                 amount=None, name=None):
        self.account = account
        self.trntype = trntype
        self.date = date
        self.amount = amount
        self.name = name


    def __repr__(self):
        return '<Transaction %r>' % self.name

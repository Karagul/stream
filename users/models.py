# -*- encoding: utf8 -*-

from stream import db
from stream.users import constants as USER

class User(db.Model):
    __tablename__ = 'users_user'

    name= db.Column(db.String(120))
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

# -*- encoding: utf-8 -*-
import time
import os

from ofx.ofxclient import OFXClient
from ofx.parse import Parse

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

# Flask setup
app = Flask(__name__)
app.config.from_envvar('FLASK_STREAM_APP_CONFIG')

# SQLAlchemy setup
db = SQLAlchemy(app)

def userdatamodel():
    return db.Table('finance_stream',
                    db.Column('user_email', db.String(120), db.ForeignKey('user.email')),
                    db.Column('userinstitution_id', db.Integer, db.ForeignKey('userinstitution.id')),
                    db.Column('transaction_account', db.String(12), db.ForeignKey('transaction.account')),
                    db.Column('institution_id', db.Integer, db.ForeignKey('institution.id')) )

class User(db.Model):
    email = db.Column(db.String(120), primary_key=True)
    salt = db.Column(db.String(120), unique=True)
    hash = db.Column(db.String(120), unique=True)
    active = db.Column(db.Boolean())
    confirmed = db.Column(db.DateTime())

    def __init__(self, email, salt, hashfunc):
        self.email = email
        self.salt = salt
        self.hash = hashfunc(str(email)+str(salt))

    def __repr__(self):
        return '<User %r>' % self.email

class UserInstitution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(255))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<UserInstitutions %r>' % self.id

class Transaction(db.Model):
    account = db.Column(db.String(12), primary_key=True)
    trntype = db.Column(db.String(20))
    date = db.Column(db.DateTime)
    amount = db.Column(db.Integer)
    name = db.Column(db.String(32))

    def __init__(self, account):
        self.account = account

    def __repr__(self):
        return '<Transaction %r>' % self.name

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


def get_user_dev():
    ''' Import development institution, username and password tuple. '''
    lst=[]
    with open('userdev') as cfg:
        lst = [v.strip('\n') for v in cfg]
    return lst

def init_db():
    ''' Initialize SQL database using SQLAlchemy '''

@app.route('/')
def frontpage():
    user = get_user_dev()
    dtstart = time.strftime('%Y%m%d',time.localtime(time.time()-31*86400))
    client = OFXClient(user[0], user[1], user[2])
    rawxml = client.query(qtype='account', dtstart=dtstart)
    p = Parse(rawxml)

    allnodes=[]
    for n in p.nodes:
        allnodes.append(n.show())
    print 'nodes=', len(allnodes)
    tags=[]
    for v in p.tree:
        tags.append(p.nodes[v].show())
    print 'tags=', len(tags)
    # if session exists:
    #   redirect(url_for('<username>'))
    # else:
    #   redirect(url_for('login'))
    strdata = [str.join('\n',allnodes), str.join('\n',tags)]
    return ''.join(strdata)

@app.route('/<username>')
def userpage(username):
    return 'userpage'

@app.route('/register')
def register():
    return 'register'

@app.route('/login')
def login():
    return 'login'

@app.route('/logout')
def logout():
    return 'logout'

if __name__ == "__main__":
    app.run()

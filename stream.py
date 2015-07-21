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

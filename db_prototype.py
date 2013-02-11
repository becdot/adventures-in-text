import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing

DATABASE = '/tmp/prototype.db'
SECRET_KEY = '\xf0$V\xe52\x1e\xc4\x9b\xe5\xb8\x06\xcda\x90\x93W\xca\xe8c\xec\xe6\x1b\xa3\xa1'
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])
def init_db():
    with closing(connect_db) as db:
        with app.open_resource('schema.sql') as instr:
            db.cursor().executescript(instr.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()
@app.teardown_request
def teardown_request(exception):
    g.db.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        pass
    else:
        pass
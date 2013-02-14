import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     render_template, flash
from contextlib import closing
from pickle import dumps, loads


SECRET_KEY = '\xf0$V\xe52\x1e\xc4\x9b\xe5\xb8\x06\xcda\x90\x93W\xca\xe8c\xec\xe6\x1b\xa3\xa1'
DEBUG = True
DATABASE = 'game.db'

app = Flask(__name__)
app.config.from_object(__name__)


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('adv_schema.sql') as instr:
            db.cursor().executescript(instr.read())
        db.commit()

def save_game(user_id, game):
    pickled = dumps(game)
    g.db.execute('UPDATE game SET data = (?) WHERE id = (?)', [pickled, user_id])
    assert unicode(pickled) == g.db.execute('SELECT data FROM game WHERE id = (?)', [user_id]).fetchall()[0][0]
    g.db.commit()

def get_game(user_id):
    cur = g.db.execute('SELECT data FROM game WHERE id = (?)', [user_id])
    data = cur.fetchall()[0][0]
    if data:
        print "game data:", data
        return loads(data)
    return None

def delete_game(user_id):
    g.db.execute('DELETE FROM game WHERE id = (?)', [user_id])
    assert unicode(user_id) not in g.db.execute('SELECT id FROM game').fetchall()
    print "game deleted successfully"
    g.db.commit()

def create_user(blank_game):
    pickled = dumps(blank_game)
    g.db.execute('INSERT INTO game (data) VALUES (?)', [pickled])
    g.db.commit()
    flash('New user successfully created')
    user_id = g.db.execute('SELECT id FROM game ORDER BY id DESC').fetchall()[0][0]
    return user_id
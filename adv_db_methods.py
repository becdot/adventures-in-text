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
    g.db.execute('UPDATE game SET data VALUES (?) WHERE id = (?)', [pickled, user_id])
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

def create_user():
    g.db.execute('INSERT INTO game (data) VALUES (NULL)')
    g.db.commit()
    flash('New user successfully created')
    user_id = g.db.execute('SELECT id FROM game ORDER BY id DESC').fetchall()[0][0]
    return user_id







# def update_object_location(obj, location):
#     "update object's location in objects table"

#     name = obj.unique_name
#     g.db.execute('UPDATE objects SET location VALUES (?) WHERE name = (?)', [location, name])
#     g.db.commit()

# def update_object_data(obj):

#     data = dumps(obj)
#     g.db.execute('UPDATE objects SET data VALUES (?) WHERE name = (?)', [data, name])
#     g.db.commit()

# def update_user_location(location):
#     "update user's location in users table"

#     name = location.unique_name
#     user_id = session['id']
#     g.db.execute('UPDATE users SET location VALUES (?) WHERE id = (?)', [name, user_id])
#     assert name == g.db.execute('SELECT location FROM users WHERE id = (?)').fetchall()[0][0]
#     g.db.commit()

# def update_user_message(message):
#     "update user message in users table"

#     user_id = session['id']
#     g.db.execute('UPDATE users SET message VALUES (?) WHERE id = (?)', [message, user_id])

# def save_game(game_dict, msg):
#     pass




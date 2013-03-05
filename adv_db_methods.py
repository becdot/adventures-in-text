from flask import Flask, request, session, redirect, url_for, \
     render_template, flash
from contextlib import closing
from json import loads, dumps
from game import Game


SECRET_KEY = 'my_secret_key'
DEBUG = True
DATABASE = 'database.txt'

app = Flask(__name__)
app.config.from_object(__name__)


def connect_db(mode='r'):
    return open(app.config['DATABASE'], mode)

def init_db():
    with closing(connect_db(mode='w')) as db:
        pass

def user_exists(user_id):
    "Returns True if user_id exists in the database"
    with closing(connect_db('r')) as db:
        data = [loads(line) for line in db.readlines() if loads(line)[u'user_id'] == user_id]
        if data:
            return True
        return False

def save_game(user_id, game):
    "Serialises game and overwrites user's last saved game, if it exists"
    with closing(connect_db('a')) as db:
        serial = dumps({'user_id': user_id, 'game': game.serialise()})
        serial += '\n'
        if user_exists(user_id):
            delete_game(user_id)
            db.write(serial)
        else:
            db.write(serial)            

def get_game(user_id):
    """If the user exists in the database, returns a Game object initialised with the user's last saved game.
        Otherwise, returns None."""
    with closing(connect_db('r')) as db:
        if user_exists(user_id):
            data = [loads(line) for line in db.readlines() if loads(line)[u'user_id'] == user_id]
            return Game(data[0]['game'])
        return None

def delete_game(user_id):
    "Deletes the data associated with a user's id"
    with closing(connect_db('r+')) as db:
        data = db.readlines()
        for i, line in enumerate(data):
            decoded = loads(line)
            if decoded['user_id'] == user_id:
                del(data[i])
        if data:
            db.seek(0)
            db.writelines(data)
            db.truncate()
        else:
            db.seek(0)
            db.write('')
            db.truncate()

def get_new_id():
    "Returns the unused id"
    with closing(connect_db('r')) as db:       
        ids = [loads(line)['user_id'] for line in db.readlines()]
        user_id = 1
        if ids: 
            user_id = sorted(ids)[-1] + 1
        return user_id

def create_user(blank_game, user_id=None):
    """Saves a blank game and returns a new unique user id if one is not provided.
        Otherwise, saves the game and returns the provided id."""
    with closing(connect_db('r')) as db:
        if not user_id:
            user_id = get_new_id()
        save_game(user_id, blank_game)
        flash('New user successfully created')
        return user_id

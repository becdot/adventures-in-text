from flask import Flask, request, session, g, redirect, url_for, \
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
    with closing(connect_db('r')) as db:
        data = [loads(line) for line in db.readlines() if loads(line)[u'user_id'] == user_id]
        if data:
            return True
        return False

def save_game(user_id, game):
    "DB mode = a"
    with closing(connect_db('a')) as db:
        serial = dumps({'user_id': user_id, 'game': game.serialise()})
        serial += '\n'
        print "saving", serial
        if user_exists(user_id):
            delete_game(user_id)
            db.write(serial)
        else:
            db.write(serial)            

def get_game(user_id):
    "DB mode = r"
    with closing(connect_db('r')) as db:
        data = [loads(line) for line in db.readlines() if loads(line)[u'user_id'] == user_id]
        print "data", data
        if data:
            return Game(data[0]['game'])
        return None

def delete_game(user_id):
    "DB mode = rw"
    with closing(connect_db('r+')) as db:
        data = db.readlines()
        for i, line in enumerate(data):
            decoded = loads(line)
            if decoded['user_id'] == user_id:
                print "deleting", decoded['user_id']
                del(data[i])
        print "remaining data", data
        if data:
            db.seek(0)
            db.writelines(data)
            db.truncate()
        else:
            db.seek(0)
            db.write('')
            db.truncate()

def create_user(blank_game, user_id=None):
    "DB mode = r"
    with closing(connect_db('r')) as db:
        if not user_id:
            user_id = 1        
            ids = [loads(line)['user_id'] for line in db.readlines()]
            if ids: 
                user_id = sorted(ids)[-1] + 1
        save_game(user_id, blank_game)
        flash('New user successfully created')
        return user_id

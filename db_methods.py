# DATABASE METHODS

# Uses pymongo to write to a Mongo DB
# Defines get_game, save_game, and new_game functions

from flask import Flask, request, session, redirect, url_for, \
     render_template, flash, g
from contextlib import closing
from pymongo import MongoClient

from game import Game


SECRET_KEY = 'my_secret_key'
DEBUG = True
DATABASE = 'game'
COLLECTION = 'games'

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    "Connect to the database -- must have a mongod client running"
    return MongoClient()

def init_db():
    "If the database exists, drop it"
    if g.connection:
        g.connection[DATABASE][COLLECTION].drop()

def save_game(user_id, game):
    "Serialises game and overwrites user's last saved game, if it exists"
    serial = game.serialise()
    g.db.update({'_id': user_id}, {'game': serial}, upsert=True)           

def get_game(user_id):
    """If the user exists in the database, returns a Game object initialised with the user's last saved game.
        Otherwise, returns None."""
    data = g.db.find_one({'_id': user_id})
    if data:
        return Game(data['game'])
    return None

def new_game(blank_game, user_id=None):
    """Saves the blank game in the database and returns either the provided user_id or a new unique id.
        If a user_id is provided, deletes that entry from the database before creating a new entry."""
    if user_id:
        g.db.remove({'_id': user_id}, justOne=True)
    new_id = g.db.insert({'game': blank_game.serialise()})
    flash('New user successfully created')
    return new_id

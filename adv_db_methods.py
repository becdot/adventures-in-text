from schema import object_attributes, column_names, COLUMNS, set_rows, create_database

import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     render_template, flash
from contextlib import closing
from pickle import dumps, loads


SECRET_KEY = 'my_secret_key'
DEBUG = True
DATABASE = 'game.db'

app = Flask(__name__)
app.config.from_object(__name__)


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        user_info, rooms_table, objects_table = create_database()
        db.cursor().executescript(user_info)
        db.cursor().executescript(rooms_table)
        db.cursor().executescript(objects_table)
        db.commit()

# def did_object_change(object):
#     "Returns True if the object's field changed, and False if no change occurred"
#     # check all columns in objects table
#     # check object's location (room_id)
#     pass

# def did_location_change(user_id):
#     "Returns True if user's location changed, and False otherwise"
#     pass

# def save_game(user_id, game):
#     "Updates relevant fields in the database"
#     if did_location_change(user_id):
#         # update location in user_info table
#         pass
#     room = game['location']
#     inventory = game['inventory']
#     for obj in room.objects + inventory:
#         if did_object_change(obj):
#             # update object data in objects table
#             pass


def save_game(user_id, game):
    # update user_info table
    location = game['location'].name
    g.db.execute('UPDATE user_info SET location = (?) WHERE game_id = (?) and location != (?)',
                    [location, user_id, location])
    # get a list of objects in the current room with their attributes in database-ready form
    objects = game['location'].objects
    db_objects = set_rows()




    db.execute('UPDATE objects SET unique_name = (?) and room_id = (?) and subtype = (?)\
        and _room = (?)and is_open = (?) and has_user = (?) and is_lit = (?) and block = (?)\
        WHERE id = (?)\
        and (unique_name != (?) and room_id != (?) and subtype != (?)\
        and _room != (?) and is_open != (?) and has_user != (?) and is_lit != (?) and block != (?))',
        [])

def new_game(blank_game):
    "Stores the blank game in the database and returns a new user_id"
    # insert game['location'] in user_info table and get updated game_id
    # store rooms in rooms table (don't need to store inventory since it's empty)
    # store all objects
    pass

def get_game(user_id):
    "Returns a game dictionary with the appropriate data"
    # get all rows from rooms table where game_id = user_id
    # recreate rooms with empty room.objects
    # for room in list_of_rooms:
      # get all objects from objects table where room_id == room_id
      # recreate objects from row values
    pass

def delete_game(user_id):
    # remove row from user_info table
    # remove all rows in rooms table where game_id == user_id
    # but store the room ids
    # remove all rows from objects table where room_id == room ids








# def new_game(blank_game):
#     """Creates new rows in user_info, rooms, and objects tables
#         Returns current game_id (session id)"""
#     with closing(connect_db()) as db:
#         # Set location in user_info table
#         db.execute('INSERT INTO user_info (location) VALUES (?)', [blank_game['location'].name])
#         # Get new game_id
#         game_id = db.execute('SELECT game_id from user_info ORDER BY game_id DESC').fetchall()[0][0]
#         for room in blank_game['rooms']:
#             # Add new row to rooms table
#             db.execute('INSERT INTO rooms (name, game_id) VALUES (?, ?)', [room.name, game_id])
#             # Get new room_id
#             room_id = db.execute('SELECT id from rooms ORDER BY id DESC').fetchall()[0][0]
#             # Add static object information (unique_name, room_id, subtype)
#             for obj in room.objects:
#                 db.execute('INSERT INTO objects (unique_name, room_id, subtype) VALUES (?, ?, ?)',\
#                             [obj.unique_name, room_id, obj.__class__.__name__])
#                 # Get new object id
#                 obj_id = db.execute('SELECT id from objects ORDER BY id DESC').fetchall()[0][0]
#                 valid_attributes = unique_object_attributes(obj)
#                 # Add dynamic object attributes
#                 for key, value in valid_attributes.iteritems():
#                     db.execute('UPDATE objects SET (?) = (?) WHERE id = (?)', [key, value, obj_id])
#         db.commit()
#     return game_id





# def save_game(user_id, game):
#     pickled = dumps(game)
#     g.db.execute('UPDATE game SET data = (?) WHERE id = (?)', [pickled, user_id])
#     assert unicode(pickled) == g.db.execute('SELECT data FROM game WHERE id = (?)', [user_id]).fetchall()[0][0]
#     g.db.commit()

# def get_game(user_id):
#     cur = g.db.execute('SELECT data FROM game WHERE id = (?)', [user_id])
#     data = cur.fetchall()[0][0]
#     if data:
#         return loads(data)
#     return None

# def delete_game(user_id):
#     g.db.execute('DELETE FROM game WHERE id = (?)', [user_id])
#     assert unicode(user_id) not in g.db.execute('SELECT id FROM game').fetchall()
#     print "game deleted successfully"
#     g.db.commit()

# def create_user(blank_game):
#     pickled = dumps(blank_game)
#     g.db.execute('INSERT INTO game (data) VALUES (?)', [pickled])
#     g.db.commit()
#     flash('New user successfully created')
#     user_id = g.db.execute('SELECT id FROM game ORDER BY id DESC').fetchall()[0][0]
#     return user_id
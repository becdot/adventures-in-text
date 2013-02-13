import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing


SECRET_KEY = '\xf0$V\xe52\x1e\xc4\x9b\xe5\xb8\x06\xcda\x90\x93W\xca\xe8c\xec\xe6\x1b\xa3\xa1'
DEBUG = True
DATABASE = 'prototype.db'

app = Flask(__name__)
app.config.from_object(__name__)



def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as instr:
            db.cursor().executescript(instr.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    g.db.close()

def create_user():
    "inserts new user into the users table, and returns the id"

    g.db.execute('INSERT INTO users (id) VALUES (NULL)')
    g.db.commit()
    flash('New user successfully created')
    user_id = g.db.execute('SELECT id FROM users ORDER BY id DESC').fetchall()[0][0]
    print user_id
    return user_id

def get_user_actions():
    "return a list of all actions where user = user_id, sorted in descending order"

    cur = g.db.execute('SELECT action FROM actions WHERE user = (?) ORDER BY num desc', [session['id']])
    actions = [str(action[0]) for action in cur.fetchall()]
    print actions
    return actions

def store_action(action):
    "store action in actions table"

    g.db.execute('INSERT INTO actions (action, user) VALUES (?, ?)', [action, session['id']])
    user_actions = [pair[0] for pair in g.db.execute('SELECT action FROM actions').fetchall()]
    assert unicode(action) in user_actions
    g.db.commit()

def delete_user():
    "remove both user_id and all user actions from the users table and actions table, respectively"

    cur_id = session['id']
    g.db.execute('DELETE FROM users WHERE id = (?)', [cur_id])
    assert cur_id not in g.db.execute('SELECT id FROM users').fetchall()
    g.db.execute('DELETE FROM actions WHERE user = (?)', [cur_id])
    assert cur_id not in g.db.execute('SELECT user FROM actions').fetchall()
    g.db.commit()


@app.route('/', methods=['GET', 'POST'])
def index():
        if request.method == 'GET':
            try:
                if session['id']:
                    actions = get_user_actions()
                    print "user actions", actions
                    return render_template('game_prototype.html', actions=actions)
            except KeyError:
                user_id = create_user()
                session['id'] = user_id
                return render_template('game_prototype.html')
        else:
            action = request.form['action']
            store_action(action)
            actions = get_user_actions()
            return render_template('game_prototype.html', actions=actions)

@app.route('/newgame', methods=['GET'])
def newgame():
    delete_user()
    print "user deleted"
    new_id = create_user()
    session['id'] = new_id
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)
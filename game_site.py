from game import game as initial
from play_game import play_game
from adv_db_methods import SECRET_KEY, DATABASE, DEBUG, app,\
                            connect_db, init_db, save_game, get_game, delete_game, create_user

from flask import Flask, render_template, request, session, redirect, url_for, g

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    g.db.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        try:
            if session['id']: # if a session is already running, try to load the user's previous game
                print "session", session['id'], "is already initialized"
                loaded = get_game(session['id'])
                if loaded: # if there is a game, load it
                    return render_template('form.html', room=loaded['location'], \
                                inventory=loaded['inv'], exits=loaded['location'].exits)
                else: # otherwise, just load a new game
                    return render_template('form.html', room=initial['location'], 
                                inventory=initial['inv'], exits=initial['location'].exits)
        except KeyError: # otherwise, load a new game
            return render_template('form.html', room=initial['location'], inventory=initial['inv'], exits=initial['location'].exits)
    elif request.method == 'POST':
        action = request.form['action']
        updated_game, msg = play_game(initial, action)
        return render_template('form.html', room=updated_game['location'], inventory=updated_game['inv'], \
                                exits=updated_game['location'].exits, message=msg)

@app.route('/newgame', methods=['GET'])
def newgame():
    old_id = session['id']
    delete_game(old_id)
    new_id = create_user()
    session['id'] = new_id
    print "new id is:", new_id
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='localhost')
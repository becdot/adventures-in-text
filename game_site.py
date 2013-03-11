# FLASK WEBSITE

# Runs the game online (currently only on localhost: 5000)
# Renders html, passes user_action to game.play(action), and calls database methods to get, save, and delete games

from game import Game
from db_methods import SECRET_KEY, DATABASE, COLLECTION, DEBUG, app, g, \
                            connect_db, init_db, save_game, get_game, new_game

from flask import Flask, render_template, request, session, redirect, url_for

@app.before_request
def before_request():
    g.connection = connect_db()
    g.db = g.connection[DATABASE][COLLECTION]

@app.teardown_request
def teardown_request(exception):
    g.connection.close()

def get_new_game(user_id=None):
    blank_game = Game()
    if user_id:
        print "deleting user", user_id
    session['id'] = new_game(blank_game, user_id)
    print "creating a new game for user", session['id']
    return redirect(url_for('index'))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        if 'id' in session and get_game(session['id']):
            loaded_game = get_game(session['id'])
            print "session", session['id'], "is already initialized"
            return render_template('form.html', room=loaded_game.game['location'],
                        inventory=loaded_game.game['inv'], exits=loaded_game.game['location'].exits)
        else:
            if 'id' in session:
                return get_new_game(session['id'])
            return get_new_game()
            
    elif request.method == 'POST':
        action = request.form['action']
        if 'id' not in session:
            return redirect(url_for('index'))
        loaded = get_game(session['id'])
        msg = loaded.play(action)
        save_game(session['id'], loaded)
        print "saving game for user", session['id']
        return render_template('form.html', room=loaded.game['location'], inventory=loaded.game['inv'], \
                                exits=loaded.game['location'].exits, message=msg)

@app.route('/newgame', methods=['GET'])
def newgame():
    return get_new_game(session['id'])

if __name__ == '__main__':
    app.run(host='localhost')
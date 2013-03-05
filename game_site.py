from game import Game
from adv_db_methods import SECRET_KEY, DATABASE, DEBUG, app, g, \
                            connect_db, init_db, save_game, get_game, new_game

from flask import Flask, render_template, request, session, redirect, url_for

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    g.db.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        if 'id' in session:
            loaded_game = get_game(session['id'])
            if loaded_game:
                print "session", session['id'], "is already initialized"
                return render_template('form.html', room=loaded_game.game['location'],
                            inventory=loaded_game.game['inv'], exits=loaded_game.game['location'].exits)
            else:
                print "creating a new game for user", session['id']
                game = Game()
                new_game(game, session['id'])
                return render_template('form.html', room=game.game['location'], inventory=game.game['inv'], 
                                    exits=game.game['location'].exits)
        else:
            print "loading a totally new game"
            game = Game()
            session['id'] = new_game(game)
            print "new session id created:", session['id']
            return render_template('form.html', room=game.game['location'], inventory=game.game['inv'], 
                                    exits=game.game['location'].exits)
            
    elif request.method == 'POST':
        action = request.form['action']
        if 'id' not in session:
            return redirect(url_for('index'))
        user_id = session['id']
        loaded = get_game(user_id)
        msg = loaded.play(action)
        save_game(session['id'], loaded)
        print "saving game for user", session['id']
        return render_template('form.html', room=loaded.game['location'], inventory=loaded.game['inv'], \
                                exits=loaded.game['location'].exits, message=msg)

@app.route('/newgame', methods=['GET'])
def newgame():
    old_id = session['id']
    game = Game()
    session['id'] = new_game(game, old_id)
    print "user", old_id, "deleted"
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='localhost')
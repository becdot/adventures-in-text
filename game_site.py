from game import Game
from adv_db_methods import SECRET_KEY, DATABASE, DEBUG, app,\
                            connect_db, init_db, save_game, get_game, delete_game, create_user, get_new_id

from flask import Flask, render_template, request, session, redirect, url_for, g

# @app.before_request
# def before_request():
#     g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    try:
        g.db.close()
    except AttributeError:
        pass

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
                new_game = Game()
                create_user(new_game, user_id=session['id'])
                return render_template('form.html', room=new_game.game['location'], inventory=new_game.game['inv'], 
                                    exits=new_game.game['location'].exits)
        else:
            print "loading a totally new game"
            new_game = Game()
            session['id'] = create_user(new_game)
            print "new session id created:", session['id']
            return render_template('form.html', room=new_game.game['location'], inventory=new_game.game['inv'], 
                                    exits=new_game.game['location'].exits)
            
    elif request.method == 'POST':
        action = request.form['action']
        if 'id' not in session:
            return redirect(url_for('index'))
        user_id = session['id']
        loaded = get_game(user_id)
        msg = loaded.play(action)
        print "loaded", loaded.serialise()
        save_game(session['id'], loaded)
        print "saving game for user", session['id']
        return render_template('form.html', room=loaded.game['location'], inventory=loaded.game['inv'], \
                                exits=loaded.game['location'].exits, message=msg)

@app.route('/newgame', methods=['GET'])
def newgame():
    old_id = session['id']
    delete_game(old_id)
    session['id'] = get_new_id()
    print "user", old_id, "deleted"
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='localhost')
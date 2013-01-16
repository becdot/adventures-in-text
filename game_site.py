from game import game as initial
from play_game import play_game

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('form.html', room=initial['location'], inventory=initial['inv'])
    elif request.method == 'POST':
        action = request.form['action']
        new_game, msg = play_game(initial, action)
        return render_template('form.html', room=new_game['location'], inventory=new_game['inv'], message=msg)

if __name__ == '__main__':
    app.run(host='localhost', debug=True)

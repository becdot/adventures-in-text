from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('form.html')

@app.route('/game', methods=['POST'])
def game():
    if request.method == 'POST':
        pass

if __name__ == '__main__':
    app.run(host='localhost', debug=True)

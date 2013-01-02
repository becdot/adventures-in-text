from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/')
@app.route('/user/<username>/')
def user(username=''):
    return render_template('user.html', name=username.title())

@app.route('/post/<int:post_id>/')
def post(post_id):
    return "Post {}".format(post_id)

if __name__ == "__main__":
    app.run(host='localhost', debug=True)
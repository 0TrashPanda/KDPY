from flask import Flask, abort, flash, redirect, render_template, render_template_string, request, url_for
import flask_login
from flask_socketio import SocketIO
from classes import Tile, TileType, Domino, Board, Player
from flask_login import LoginManager

app = Flask(__name__)
socketio = SocketIO(app)
login_manager = LoginManager()
login_manager.init_app(app)

app.secret_key = 'super secret key'

users = {}

@login_manager.user_loader
def load_user(id):
    return users.get(id)

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@app.route('/')
def index():
    if not flask_login.current_user.is_authenticated:
        return render_template('login.html')
    return render_template('index.html', users=users)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    user = users.get(username)
    if user is None:
        user = Player(username)
        users[user.id] = user
    else:
        user = Player(username)
    flask_login.login_user(user)
    # next = request.args.get('next')
    # if not url_has_allowed_host_and_scheme(next, request.host):
    #     return abort(400)
    return render_template('index.html', users=users), {'HX-Refresh': 'true'}

@app.route("/protected")
@flask_login.login_required
def protected():
    return render_template_string(
        "Logged in as: {{ user.id }}",
        user=flask_login.current_user
    )

@app.route("/logout", methods=['POST'])
def logout():
    flask_login.logout_user()
    return render_template('login.html'), {'HX-Refresh': 'true'}

if __name__ == '__main__':
    socketio.run(app, port=5000, debug=True)

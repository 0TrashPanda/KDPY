from flask import Flask, redirect, render_template, render_template_string, request, url_for
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
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    user = users.get(username)
    if user is None:
        user = Player(username)
        users[username] = user
    else:
        user = Player(username)
    flask_login.login_user(user)
    return redirect(url_for("protected"))

@app.route("/protected")
@flask_login.login_required
def protected():
    return render_template_string(
        "Logged in as: {{ user.id }}",
        user=flask_login.current_user
    )

@app.route("/logout")
def logout():
    flask_login.logout_user()
    return "Logged out"

if __name__ == '__main__':
    socketio.run(app, port=5000, debug=True)

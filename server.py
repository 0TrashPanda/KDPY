from flask_apscheduler import APScheduler
from flask import Flask, abort, flash, redirect, render_template, render_template_string, request, url_for
import flask_login
from flask_socketio import SocketIO
from classes import Tile, TileType, Domino, Board, Player
from flask_login import LoginManager
from web_classes import Game, User

app = Flask(__name__)
socketio = SocketIO(app)
login_manager = LoginManager()
login_manager.init_app(app)
scheduler = APScheduler()

app.secret_key = 'super secret key'

users = {}
games = {}

@login_manager.user_loader
def load_user(id):
    return users.get(id)

@socketio.on('connect')
def handle_connect():
    user = flask_login.current_user
    user.join()
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    user = flask_login.current_user
    user.leave()
    print('Client disconnected')

# Task to delete inactive user
def delete_inactive_users():
    for user in list(users.values()):
        if user.is_gone():
            users.pop(user.id)
            print(f"User {user} is gone")

@app.route('/')
def index():
    if not flask_login.current_user.is_authenticated:
        return render_template('login.html')
    return render_template('index.html', current_user=flask_login.current_user ,users=users)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    user = users.get(username)
    if user is None:
        user = User(username)
        users[user.id] = user
    else:
        user = User(username)
    flask_login.login_user(user)
    # next = request.args.get('next')
    # if not url_has_allowed_host_and_scheme(next, request.host):
    #     return abort(400)
    return render_template('index.html',current_user=flask_login.current_user , users=users), {'HX-Refresh': 'true'}

@app.route("/protected")
@flask_login.login_required
def protected():
    return render_template_string(
        "Logged in as: {{ user.id }}",
        user=flask_login.current_user
    )

@app.route("/logout", methods=['POST'])
def logout():
    user = flask_login.current_user
    user.remove(games)
    user_id = user.id
    flask_login.logout_user()
    del users[user_id]
    return render_template('login.html'), {'HX-Refresh': 'true'}

@app.route('/create', methods=['POST'])
def create():
    player = flask_login.current_user.player
    game = Game(host=player)
    game.players.append(player)
    return render_template('menu.html', game=game)

scheduler.add_job(id='cleanup_job', func=delete_inactive_users, trigger='interval', seconds=5)
scheduler.start()

if __name__ == '__main__':
    socketio.run(app, port=5000, debug=True)

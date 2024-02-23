from flask_apscheduler import APScheduler
from flask import Flask, abort, flash, redirect, render_template, render_template_string, request, url_for
import flask_login
from flask_socketio import SocketIO
from classes import Tile, TileType, Domino, Board, Player
from flask_login import LoginManager, login_required
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
    if not user.is_authenticated:
        user = "Anonymous"
        return
    print(f'{user} connected')
    user.join()
    # if user.game is not None:
        # socketio.emit('innerHTML', {'html': render_template('menu.html', game=user.game), 'div': 'main'})

@socketio.on('disconnect')
def handle_disconnect():
    user = flask_login.current_user
    if not user.is_authenticated:
        return
    user.leave()
    print('Client disconnected')

def delete_inactive_users():
    for user in list(users.values()):
        if user.is_gone():
            users.pop(user.id)
            print(f"User {user} is gone")

@app.route('/', methods=['GET'])
def index():
    if not flask_login.current_user.is_authenticated:
        return render_template('index.html')
    return redirect(url_for('main'))

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
    return redirect(url_for('main'))

@app.route('/main', methods=['GET'])
@login_required
def main():
    user = flask_login.current_user
    return render_template('main.html', user=user)

@app.route("/logout")
@login_required
def logout():
    user = flask_login.current_user
    print(f'User {user} logged out')
    user.leave_game()
    user_id = user.id
    flask_login.logout_user()
    del users[user_id]
    return redirect(url_for('index'))

@app.route('/create', methods=['POST'])
@login_required
def create():
    user = flask_login.current_user
    if user.game is not None:
        return render_template('menu.html', game=user.game)
    passwd = request.form.get('passwd')
    player = flask_login.current_user.player
    game = Game(host=player, passwd=passwd)
    game.players.append(player)
    user.game = game
    games[game.id] = game
    return render_template('menu.html', game=game)

@app.route('/passwd', methods=['POST'])
@login_required
def passwd():
    user = flask_login.current_user
    if user.game is not None:
        return render_template('menu.html', game=user.game)
    return render_template('passwd.html', user=user)

@app.route('/stop', methods=['POST'])
@login_required
def stop():
    user = flask_login.current_user
    if user.game is not None:
        try:
            del games[user.game.id]
        except KeyError:
            pass
        user.game = None
    return render_template('index.html', current_user=flask_login.current_user ,users=users), {'HX-Refresh': 'true'}

@app.route('/find_game', methods=['POST'])
@login_required
def find_game():
    user = flask_login.current_user
    if user.game is not None:
        return render_template('menu.html', game=user.game)
    return render_template('find_game.html', games=games.values())

@app.route('/passwd_join', methods=['POST'])
@login_required
def passwd_join():
    user = flask_login.current_user
    if user.game is not None:
        return render_template('menu.html', game=user.game)
    game_id = request.form.get('game_id')
    return render_template('passwd_join.html', game_id=game_id)

@app.route('/join', methods=['POST'])
@login_required
def join():
    user = flask_login.current_user
    if user.game is not None:
        return render_template('menu.html', game=user.game)
    game_id = request.form.get('game_id')
    game = games.get(int(game_id))
    if game is None:
        flash('Game does not exist')
        return render_template('index.html', current_user=flask_login.current_user ,users=users), {'HX-Refresh': 'true'}
    if game.passwd != request.form.get('passwd'):
        print('Invalid password')
        return render_template('index.html', current_user=flask_login.current_user ,users=users), {'HX-Refresh': 'true'}
    player = flask_login.current_user.player
    game.players.append(player)
    user.game = game
    return render_template('menu.html', game=game)

scheduler.add_job(id='cleanup_job', func=delete_inactive_users, trigger='interval', seconds=5)
scheduler.start()

if __name__ == '__main__':
    socketio.run(app, port=5000, debug=True)

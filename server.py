from flask_apscheduler import APScheduler
from flask import Flask, abort, flash, redirect, render_template, render_template_string, request, url_for
import flask_login
from flask_socketio import SocketIO
from classes import Tile, TileType, Domino, Board, Player
from flask_login import LoginManager, login_required
from web_classes import Game, User, Games

app = Flask(__name__)
socketio = SocketIO(app)
login_manager = LoginManager()
login_manager.init_app(app)
scheduler = APScheduler()

login_manager.login_view = 'index'

app.secret_key = 'super secret key'

users = {}
games = Games()

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

@app.route('/eval', methods=['GET', 'POST'])
def evaluate():
    user = flask_login.current_user
    if request.method == 'GET':
        return render_template('eval.html')
    code = request.form.get('code')
    try:
        result = str(eval(code))
    except Exception as e:
        result = str(e)
    return result

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    user = User(username)
    users[user.id] = user
    flask_login.login_user(user)
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
    global games
    user.leave_game()
    user_id = user.id
    flask_login.logout_user()
    del users[user_id]
    return redirect(url_for('index'))

@app.route('/create-game')
@login_required
def create_game():
    user = flask_login.current_user
    game = games.user_game(user.id)
    if game is not None:
        return render_template('menu.html', game=game, is_host=game.is_host(user.id))
    return render_template('create_game.html')

@app.route('/create', methods=['POST'])
@login_required
def create():
    user = flask_login.current_user
    game = games.user_game(user)
    if game is not None:
        return render_template('menu.html', game=game, is_host=game.is_host(user.id))
    passwd = request.form.get('passwd')
    game = Game(host=user.id, passwd=passwd)
    games.add(game)
    return render_template('menu.html', game=game, is_host=True)

@app.route('/stop')
@login_required
def stop():
    user = flask_login.current_user
    game = games.user_game(user.id)
    if game is not None:
        game.evacuate()
        games.remove(game)
    return redirect(url_for('main'))

@app.route('/find-games')
@login_required
def find_game():
    user = flask_login.current_user
    game = games.user_game(user.id)
    if game is not None:
        print(f'User {user} is already in game {game}')
        return render_template('menu.html', game=game, is_host=game.is_host(user.id))
    return render_template('find_game.html', games=games.get_all())

@app.route('/join-passwd/<game_id>')
@login_required
def passwd_join(game_id):
    user = flask_login.current_user
    game = games.user_game(user.id)
    if game is not None:
        return render_template('menu.html', game=game, is_host=game.is_host(user.id))
    return render_template('passwd_join.html', game_id=game_id)

@app.route('/join', methods=['POST'])
@login_required
def join():
    user = flask_login.current_user
    game = games.user_game(user.id)
    if game is not None:
        print(f'User {user} is already in game {game}')
        return render_template('menu.html', game=game, is_host=game.is_host(user.id))
    game_id = request.form.get('game_id')
    if game_id is None:
        return redirect(url_for('main'))
    game = games.get_game(game_id)
    if game is None:
        return redirect(url_for('main'))
    if game.passwd != request.form.get('passwd'):
        print('Invalid password')
        return redirect(url_for(f'join-passwd/{game_id}'))
    game.add_user(user)
    return render_template('menu.html', game=game, is_host=game.is_host(user.id))

scheduler.add_job(id='cleanup_job', func=delete_inactive_users, trigger='interval', seconds=5)
scheduler.start()

if __name__ == '__main__':
    socketio.run(app, port=5000, debug=True)

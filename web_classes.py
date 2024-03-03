from itertools import count
import time
from classes import Player
from dataclasses import dataclass, field
import random
from classes import Tile, TileType, Domino, Board, Player, StackPeace

users = {}
@dataclass
class Game():
    host: Player
    passwd: str
    is_anonymous: bool = field(default=False, init=False)
    users: list = field(default_factory=list)
    id: int = field(init=False)
    total_kings: int = field(init=False)
    cards: int = field(init=False)

    def __post_init__(self):
        from server import games
        self.id = games.gen_id()
        self.users = [self.host]

    def add_user(self, user):
        self.users.append(user)

    def leave(self, user):
        from server import games
        self.users.remove(user)
        if self.user_count() == 0:
            games.remove(self)
            return
        if self.host == user:
            self.host = self.users[0]

    def user_count(self):
        return len(self.users)

    def evacuate(self):
        for user in self.users:
            user.game = None
        self.users = []
        self.host = None

    def is_host(self, user):
        return self.host == user

    def usersnames(self):
        return [users.get(user_id) for user_id in self.users]

    def start(self):
        match len(self.users):
            case 2:
                self.total_kings = 4
                self.cards = 24
            case 3:
                self.total_kings = 3
                self.cards = 36
            case 4:
                self.total_kings = 4
                self.cards = 48
            case _:
                raise ValueError("Invalid number of players")
        from server import socketio
        for user in self.users:
            socketio.emit('start_game', {}, room=users.get(user).sid)
        time.sleep(1)
        random.shuffle(self.users)
        if len(self.users) == 2:
            self.users += self.users
        old_stack = self.get_new_stack()
        for player in self.users:
            self.choose_tile(player, old_stack)

    def get_new_stack(self):
        stack = []
        for _ in range(self.total_kings):
            stack.append(StackPeace(Domino()))
        stack.sort(key=lambda x: x.domino.number)
        self.cards -= self.total_kings
        return stack

    def choose_tile(self, player, stack):
        from server import socketio
        socketio.emit('choose_tile', {'stack': stack, 'player': player}, room=users.get(player).sid)


@dataclass
class User():
    username: str
    id: int = field(default_factory=count().__next__)
    player: Player = field(init=False)
    sid: str = field(default=None)
    last_seen: float = field(default_factory=time.time)

    def __str__(self):
        return self.username

    def join(self):
        self.last_seen = 0

    def leave(self):
        self.last_seen = time.time()

    def is_gone(self):
        if self.last_seen == 0:
            return False
        return time.time() - self.last_seen > 10 # 30 seconds

    def __post_init__(self):
        self.player = Player(name=self.username)

    def is_active(self):
        return True

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def leave_game(self):
        from server import games
        game = games.user_game(self)
        if game is not None:
            game.leave(self, games)


@dataclass
class Games():
    games: list = field(default_factory=list)

    def __str__(self):
        from server import users
        string = ""
        for game in self.games:
            string += f"id: {game.id} host: {users.get(game.host).username} passwd:{game.passwd} users: {[users.get(user).username for user in game.users]}\n"
        return string

    def add(self, game):
        self.games.append(game)

    def get_game(self, id):
        try:
            id = int(id)
        except ValueError:
            return None
        for game in self.games:
            if game.id == id:
                return game
        return None

    def user_game(self, user):
        for game in self.games:
            if user in game.users:
                return game
        return None

    def remove(self, game):
        self.games.remove(game)

    def gen_id(self):
        id = random.randint(1000, 9999)
        while self.get_game(id) is not None:
            id = random.randint(1000, 9999)
        return id

    def get_all(self):
        return self.games

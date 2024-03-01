from itertools import count
import time
from classes import Player
from dataclasses import dataclass, field
import random

@dataclass
class Game():
    host: Player
    passwd: str
    is_anonymous: bool = field(default=False, init=False)
    users: list = field(default_factory=list)
    id: int = field(init=False)

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
        from server import users
        return [users.get(user_id) for user_id in self.users]


@dataclass
class User():
    username: str
    id: int = field(default_factory=count().__next__)
    player: Player = field(init=False)
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
        print(f'Looking for game {id}')
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

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
    players: list = field(default_factory=list)
    id: int = field(init=False)

    def __post_init__(self):
        self.id = self.gen_id()

    def add_player(self, player):
        self.players.append(player)

    def leave(self, user, games):
        self.players.remove(user.player)
        if self.host == user.player:
            self.host = self.players[0]
        if len(self.players) == 0:
            games.pop(self.id)

    def get_player_count(self):
        return len(self.players)

    def gen_id(self):
        id = random.randint(1000, 9999)
        from server import games
        if id in games:
            return self.gen_id()
        return id

@dataclass
class User():
    username: str
    id: int = field(default_factory=count().__next__)
    player: Player = field(init=False)
    last_seen: float = field(default_factory=time.time)
    game: Game = None

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
        self.game.leave(self)


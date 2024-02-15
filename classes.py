from dataclasses import dataclass, field
from enum import Enum
import random
import numpy as np

class TileType(Enum):
    KING = "👑"
    FORREST = "🌲"
    DESERT = "🏜️"
    WHEAT = "🌾"
    WATER = "🌊"
    PLAINS = "🌿"
    MINES = "⛏️"

@dataclass
class Tile:
    type: TileType = field(default_factory=lambda: list(TileType)[np.random.randint(1, 7)])
    crowns: int = None
    number: int = 0

    def __post_init__(self):
        if self.crowns is None:
            self.crowns = np.random.binomial(2, float(self.number) / 200)

@dataclass
class Board:
    tiles: list[list[Tile]] = field(default_factory=[[Tile(type=TileType.KING)]])

    def up(self, x, y):
        return self.tiles[x - 1][y]

    def down(self, x, y):
        return self.tiles[x + 1][y]

    def left(self, x, y):
        return self.tiles[x][y - 1]

    def right(self, x, y):
        return self.tiles[x][y + 1]

@dataclass
class Player:
    name: str
    id: int
    score: int
    board: Board

@dataclass
class Domino:
    tile0: Tile
    tile1: Tile
    number: int

    def __init__(self):
        self.number = random.randint(0, 100)
        self.tile0 = Tile(self.number)
        self.tile1 = Tile(self.number)

@dataclass
class StackPeace:
    domino: Domino
    player_id: int = None
    player_name: str = None

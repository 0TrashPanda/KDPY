from dataclasses import dataclass, field
from enum import Enum
import random
import numpy as np

class TileType(Enum):
    EMPTY = " "
    KING = "👑"
    FORREST = "🌲"
    DESERT = "🏜️"
    WHEAT = "🌾"
    WATER = "🌊"
    PLAINS = "🌿"
    MINES = "⛏️"

@dataclass
class Tile:
    type: TileType = field(default_factory=lambda: list(TileType)[np.random.randint(2, 8)])
    crowns: int = None
    number: int = 0

    def __post_init__(self):
        if self.crowns is None:
            self.crowns = np.random.binomial(2, float(self.number) / 200)

@dataclass
class Board:
    tiles: list[list[Tile]] = field(default_factory=lambda: [[Tile(type=TileType.KING) if (x, y) == (2, 2) else Tile(type=TileType.EMPTY) for x in range(5)] for y in range(5)])

    def __str__(self):
        return "\n".join(" ".join(tile.type.value for tile in row) for row in self.tiles)

    def place(self, x0, y0, x1, y1, tile0, tile1):
        if self.tiles[y0][x0].type != TileType.EMPTY or self.tiles[y1][x1].type != TileType.EMPTY:
            return False
        if not self.naibour(x0, y0, tile0) and not self.naibour(x1, y1, tile1):
            return False
        self.tiles[y0][x0] = tile0
        self.tiles[y1][x1] = tile1

    def up(self, x0, y0, x1, y1):
        if y0 == 0 or y1 == 0:
            self.shift_down()
            return (x0, y0 + 1, x1, y1 + 1)
        return (x0, y0 - 1, x1, y1 - 1)

    def down(self, x0, y0, x1, y1):
        if y0 == 4 or y1 == 4:
            self.shift_up()
            return (x0, y0 - 1, x1, y1 - 1)
        return (x0, y0 + 1, x1, y1 + 1)

    def left(self, x0, y0, x1, y1):
        if x0 == 0 or x1 == 0:
            self.shift_right()
            return (x0 + 1, y0, x1 + 1, y1)
        return (x0 - 1, y0, x1 - 1, y1)

    def right(self, x0, y0, x1, y1):
        if x0 == 4 or x1 == 4:
            self.shift_left()
            return (x0 - 1, y0, x1 - 1, y1)
        return (x0 + 1, y0, x1 + 1, y1)

    def rotate(self, x0, y0, x1, y1):
        # 90° rotation
        if y0 == y1 + 1: # left to right
            y1 = y0
            x1 = x0 + 1
        elif y0 == y1 - 1: # right to left
            y1 = y0
            x1 = x0 - 1
        elif x0 == x1 + 1: # up to down
            x1 = x0
            y1 = y0 - 1
        elif x0 == x1 - 1: # down to up
            x1 = x0
            y1 = y0 + 1
        return (x0, y0, x1, y1)

    def shift_down(self):
        # if bottom row is empty, shift all rows down
        if all(tile.type == TileType.EMPTY for tile in self.tiles[-1]):
            self.tiles = [[Tile(type=TileType.EMPTY) for x in range(5)]] + self.tiles[:-1]

    def shift_up(self):
        # if top row is empty, shift all rows up
        if all(tile.type == TileType.EMPTY for tile in self.tiles[0]):
            self.tiles = self.tiles[1:] + [[Tile(type=TileType.EMPTY) for x in range(5)]]

    def shift_left(self):
        # if left column is empty, shift all columns left
        if all(row[0].type == TileType.EMPTY for row in self.tiles):
            self.tiles = [[Tile(type=TileType.EMPTY)] for y in range(5)] + self.tiles[:-1]

    def shift_right(self):
        # if right column is empty, shift all columns right
        if all(row[-1].type == TileType.EMPTY for row in self.tiles):
            self.tiles = self.tiles[1:] + [[Tile(type=TileType.EMPTY)] for y in range(5)]

    def naibour(self, x, y, tile):
        for i in range(-1, 1, 2):
            for j in range(-1, 1, 2):
                if self.tiles[y + i][x + j].type == tile.type or self.tiles[y + i][x + j].type == TileType.KING:
                    return True

@dataclass
class Player:
    name: str
    id: int
    score: int
    board: Board

    def __str__(self):
        return self.name

@dataclass
class Domino:
    tile0: Tile
    tile1: Tile
    number: int

    def __init__(self):
        self.number = random.randint(0, 100)
        self.tile0 = Tile(number=self.number)
        self.tile1 = Tile(number=self.number)

@dataclass
class StackPeace:
    domino: Domino
    player_id: int = None
    player_name: str = None

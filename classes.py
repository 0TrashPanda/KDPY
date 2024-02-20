from dataclasses import dataclass, field
from itertools import count
from enum import Enum
import random
import flask_login
import numpy as np
import copy

class TileType(Enum):
    EMPTY = [" "]
    KING = ["K"] # ["👑"]
    FOREST = ["A", "Ȧ", "Ä"] # ["🌴", "🌲", "🎄"]
    DESERT = ["O", "Ȯ", "Ö"] # ["🏜️", "⛱️", "🏖️"]
    WHEAT = ["W", "Ẇ", "Ẅ"] # ["🌾", "🍞", "🥪"]
    WATER = ["U", "Ȗ", "Ü"] # ["💧", "🌊", "🏊"]
    PLAINS = ["Y", "Ẏ", "Ÿ"] # ["🌿", "☘️", "🍀"]
    MINES = ["X", "Ẋ", "Ẍ"] # ["⛏️", "🛠️", "⚒️"]

@dataclass()
class Tile():
    type: TileType = field(default_factory=lambda: list(TileType)[np.random.randint(2, 8)])
    crowns: int = None
    number: int = 0

    def __post_init__(self):
        if self.type is TileType.KING or self.type is TileType.EMPTY:
            self.crowns = 0
            return
            # self.__setattr__("crowns", 0)
        if self.crowns is None:
            self.crowns = np.random.binomial(2, float(self.number) / 200)
            # self.__setattr__("crowns", np.random.binomial(2, float(self.number) / 200))

        if self.type is TileType.EMPTY and self.crowns != 0:
            raise ValueError("Empty tiles cannot have crowns")

    def __str__(self):
        return self.type.value[self.crowns]

@dataclass
class Board:
    tiles: list[list[Tile]] = field(default_factory=lambda: [[Tile(type=TileType.KING) if (x, y) == (2, 2) else Tile(type=TileType.EMPTY) for x in range(5)] for y in range(5)])

    def __str__(self):
        bordered_tiles = [["╔"] + ["═"] * len(self.tiles[0]) + ["╗"]]  # Top border
        bordered_tiles += [["║"] + [str(tile) for tile in row] + ["║"] for row in self.tiles]  # Tiles with side borders
        bordered_tiles.append(["╚"] + ["═"] * len(self.tiles[0]) + ["╝"])  # Bottom border
        return "\n".join("".join(row) for row in bordered_tiles)


    def place(self, y0, x0, y1, x1, tile0, tile1):
        print(self)
        if self.tiles[y0][x0].type != TileType.EMPTY or self.tiles[y1][x1].type != TileType.EMPTY:
            return False
        if not self.naibour(y0, x0, tile0) and not self.naibour(y1, x1, tile1):
            return False
        self.tiles[y0][x0] = tile0
        self.tiles[y1][x1] = tile1
        print(self)
        return True

    def up(self, y0, x0, y1, x1):
        if y0 == 0 or y1 == 0:
            self.shift_up()
            return (y0, x0, y1, x1)
        return (y0 - 1, x0, y1 - 1, x1)

    def down(self, y0, x0, y1, x1):
        if y0 == 4 or y1 == 4:
            self.shift_down()
            return (y0, x0, y1, x1)
        return (y0 + 1, x0, y1 + 1, x1)

    def left(self, y0, x0, y1, x1):
        if x0 == 0 or x1 == 0:
            self.shift_right()
            return (y0, x0, y1, x1)
        return (y0, x0 - 1, y1, x1 - 1)

    def right(self, y0, x0, y1, x1):
        if x0 == 4 or x1 == 4:
            self.shift_left()
            return (y0, x0, y1, x1)
        return (y0, x0 + 1, y1, x1 + 1)

    def rotate(self, y0, x0, y1, x1):
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
        # edging cases
        if y1 == -1:
            y0 += 1
            y1  += 1
            self.shift_down()
        elif y1 == 5:
            y0 -= 1
            y1 -= 1
            self.shift_up()
        elif x1 == -1:
            x0 += 1
            x1 += 1
            self.shift_right()
        elif x1 == 5:
            x0 -= 1
            x1 -= 1
            self.shift_left()
        return (y0, x0, y1, x1)

    def shift_down(self):
        # if bottom row is empty, shift all rows down
        if all(tile.type == TileType.EMPTY for tile in self.tiles[0]):
            self.tiles = self.tiles[1:] + [[Tile(type=TileType.EMPTY) for x in range(5)]]

    def shift_up(self):
        # if top row is empty, shift all rows up
        if all(tile.type == TileType.EMPTY for tile in self.tiles[-1]):
            self.tiles = [[Tile(type=TileType.EMPTY) for _ in range(5)]] + self.tiles[:-1]

    def shift_left(self):
        # if left column is empty, shift all columns left
        if all(row[0].type == TileType.EMPTY for row in self.tiles):
            # self.tiles = [[Tile(type=TileType.EMPTY)] for y in range(5)] + self.tiles[:-1]
            for index, row in enumerate(self.tiles):
                self.tiles[index] = row[1:] + [Tile(type=TileType.EMPTY)]

    def shift_right(self):
        # if right column is empty, shift all columns right
        if all(row[-1].type == TileType.EMPTY for row in self.tiles):
            # self.tiles = self.tiles[1:] + [[Tile(type=TileType.EMPTY)] for y in range(5)]
            for index, row in enumerate(self.tiles):
                self.tiles[index] = [Tile(type=TileType.EMPTY)] + row[:-1]

    def naibour(self, y, x, tile):
        cords = [(-1, 0),(0, -1),(1, 0),(0, 1)]
        for cord in cords:
            _y, _x = y + cord[0], x + cord[1]
            if _y < 0 or _y > 4 or _x < 0 or _x > 4:
                continue
            if self.tiles[_y][_x].type == tile.type or self.tiles[_y][_x].type == TileType.KING:
                return True

    def get_score(self):
        tiles = copy.deepcopy(self.tiles)
        score = 0
        for y, row in enumerate(tiles):
            for x, tile in enumerate(row):
                if tile.type is not TileType.EMPTY and tile.type is not TileType.KING:
                    # print(f"y: {y}, x: {x}, tile: {tile.type.name}")
                    score += self.calc_score_nabor(tiles, y, x)
        return score

    def calc_score_nabor(self, tiles, y, x, crowns=0, size=0):
        tile = tiles[y][x]
        crowns += tile.crowns
        size += 1
        _tile = copy.deepcopy(tile)
        tile.type = TileType.EMPTY
        # print(f"y: {y}, x: {x}, tile: {tile.type}, _tile: {_tile.type}, crowns: {crowns}, size: {size}")
        cords = [(-1, 0),(0, -1),(1, 0),(0, 1)]
        for cord in cords:
            _y, _x = y + cord[0], x + cord[1]
            if _y < 0 or _y > 4 or _x < 0 or _x > 4:
                continue
            if tiles[_y][_x].type == _tile.type:
                return self.calc_score_nabor(tiles, _y, _x, crowns, size)
        return crowns * size

@dataclass
class Player(flask_login.UserMixin):
    name: str
    id: int = field(default_factory=count().__next__)
    score: int = 0
    board: Board = field(default_factory=Board)

    def __str__(self):
        return self.name

    __tablename__ = 'user'

    def is_active(self):
        return True

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

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

class Keybinds(Enum):
    UP = ord("z")
    DOWN = ord("s")
    LEFT = ord("q")
    RIGHT = ord("d")
    PLACE = 10 # ENTER
    ROTATE = ord("r")
    ROTATE_SECOND = ord(" ")
    DISCARD = ord("x")

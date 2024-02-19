from classes import TileType, Tile, Board

def starting_board(y=0, x=0):
    board = [[Tile(type=TileType.EMPTY) for _ in range(5)] for _ in range(5)]
    board[y][x].type = TileType.KING
    return board

board = Board(starting_board(1, 1))

print(board.get_score(), 0)

board.place(0, 1, 0, 2, Tile(type=TileType.FOREST, crowns=1), Tile(type=TileType.DESERT, crowns=0))
print(board.get_score(), 1)
board.place(0, 0, 1, 0, Tile(type=TileType.FOREST, crowns=1), Tile(type=TileType.WATER, crowns=0))
print(board.get_score(), 4)
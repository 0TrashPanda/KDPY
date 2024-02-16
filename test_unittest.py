from classes import TileType, Tile, Board
import unittest   # The test framework

def starting_board(y=0, x=0):
    board = [[Tile(type=TileType.EMPTY) for _ in range(5)] for _ in range(5)]
    board[y][x].type = TileType.KING
    return board

class Test_Board(unittest.TestCase):
    def test_place(self):

        # Test placing on empty positions
        self.assertTrue(Board(starting_board()).place(0, 1, 0, 2, Tile(type=TileType.FOREST), Tile(type=TileType.DESERT)))

        # Test placing on non-empty positions
        self.assertFalse(Board(starting_board()).place(0, 0, 0, 1, Tile(type=TileType.DESERT), Tile(type=TileType.WATER)))

        # Test placing on non-neighbouring positions
        self.assertFalse(Board(starting_board()).place(0, 2, 0, 3, Tile(type=TileType.WATER), Tile(type=TileType.WATER)))

        board = Board(starting_board())
        board.place(0, 1, 0, 2, Tile(type=TileType.FOREST), Tile(type=TileType.DESERT))
        # Test placing on wrong type
        self.assertFalse(board.place(0, 3, 0, 4, Tile(type=TileType.WATER), Tile(type=TileType.WATER)))
        # Test placing on right type
        self.assertTrue(board.place(0, 3, 0, 4, Tile(type=TileType.DESERT), Tile(type=TileType.WATER)))

        # all directions
        board = Board(starting_board(2, 2))
        self.assertTrue(board.place(2, 1, 2, 0, Tile(type=TileType.FOREST), Tile(type=TileType.DESERT)))
        self.assertTrue(board.place(2, 3, 2, 4, Tile(type=TileType.FOREST), Tile(type=TileType.DESERT)))
        self.assertTrue(board.place(1, 2, 0, 2, Tile(type=TileType.FOREST), Tile(type=TileType.DESERT)))
        self.assertTrue(board.place(3, 2, 4, 2, Tile(type=TileType.FOREST), Tile(type=TileType.DESERT)))
        self.assertFalse(board.place(2, 0, 2, 1, Tile(type=TileType.FOREST), Tile(type=TileType.DESERT)))
        self.assertFalse(board.place(2, 4, 2, 3, Tile(type=TileType.FOREST), Tile(type=TileType.DESERT)))
        self.assertFalse(board.place(0, 2, 1, 2, Tile(type=TileType.FOREST), Tile(type=TileType.DESERT)))
        self.assertFalse(board.place(4, 2, 3, 2, Tile(type=TileType.FOREST), Tile(type=TileType.DESERT)))

    def test_movement(self):
        board = Board(starting_board())

        # Test moving up
        self.assertEqual(Board.up(board, 1, 2, 1, 3), (0, 2, 0, 3))
        self.assertEqual(Board.up(board, 0, 2, 0, 3), (0, 2, 0, 3))

        # Test moving down
        self.assertEqual(Board.down(board, 3, 2, 3, 3), (4, 2, 4, 3))
        self.assertEqual(Board.down(board, 4, 2, 4, 3), (4, 2, 4, 3))

        # Test moving left
        self.assertEqual(Board.left(board, 2, 1, 2, 2), (2, 0, 2, 1))
        self.assertEqual(Board.left(board, 2, 0, 2, 1), (2, 0, 2, 1))

        # Test moving right
        self.assertEqual(Board.right(board, 2, 2, 2, 3), (2, 3, 2, 4))
        self.assertEqual(Board.right(board, 2, 3, 2, 4), (2, 3, 2, 4))

    def test_rotate(self):
        # Define test board
        board = Board(starting_board())

        # Test rotating from 3 o'clock to 6 o'clock
        self.assertEqual(Board.rotate(board, 0, 1, 0, 2), (0, 1, 1, 1))

        # Test rotating from 6 o'clock to 9 o'clock
        self.assertEqual(Board.rotate(board, 0, 2, 1, 2), (0, 2, 0, 1))

        # Test rotating from 9 o'clock to 12 o'clock
        self.assertEqual(Board.rotate(board, 1, 2, 1, 1), (1, 2, 0, 2))

        # Test rotating from 12 o'clock to 3 o'clock
        self.assertEqual(Board.rotate(board, 1, 2, 0, 2), (1, 2, 1, 3))

        # edging cases
        # Test rotating from 3 o'clock to 6 o'clock
        self.assertEqual(Board.rotate(board, 4, 2, 4, 3), (3, 2, 4, 2))

        # Test rotating from 6 o'clock to 9 o'clock
        self.assertEqual(Board.rotate(board, 2, 0, 3, 0), (2, 1, 2, 0))

        # Test rotating from 9 o'clock to 12 o'clock
        self.assertEqual(Board.rotate(board, 0, 2, 0, 1), (1, 2, 0, 2))

        # Test rotating from 12 o'clock to 3 o'clock
        self.assertEqual(Board.rotate(board, 2, 4, 1, 4), (2, 3, 2, 4))

    def test_shift_down(self):
        # Define test board
        board = Board(starting_board(1, 1))

        # Test shifting up
        Board.shift_down(board)
        self.assertEqual(board.tiles[0][1].type, TileType.KING)
        self.assertEqual(board.tiles[1][1].type, TileType.EMPTY)

        Board.shift_down(board)
        self.assertEqual(board.tiles[0][1].type, TileType.KING)

    def test_shift_up(self):
        # Define test board
        board = Board(starting_board(3, 1))

        # Test shifting down
        Board.shift_up(board)
        self.assertEqual(board.tiles[4][1].type, TileType.KING)
        self.assertEqual(board.tiles[3][1].type, TileType.EMPTY)

        Board.shift_up(board)
        self.assertEqual(board.tiles[4][1].type, TileType.KING)

    def test_shift_left(self):
        # Define test board
        board = Board(starting_board(1, 1))

        # Test shifting left
        Board.shift_left(board)
        self.assertEqual(board.tiles[1][0].type, TileType.KING)
        self.assertEqual(board.tiles[1][1].type, TileType.EMPTY)

        # Board.shift_left(board)
        # self.assertEqual(board.tiles[1][0].type, TileType.KING)

    def test_shift_right(self):
        # Define test board
        board = Board(starting_board(1, 3))

        # Test shifting right
        Board.shift_right(board)
        self.assertEqual(board.tiles[1][4].type, TileType.KING)
        self.assertEqual(board.tiles[1][3].type, TileType.EMPTY)

        Board.shift_right(board)
        self.assertEqual(board.tiles[1][4].type, TileType.KING)

if __name__ == '__main__':
    unittest.main()

import unittest
from classes import TileType, Tile, Board

class TestBoard(unittest.TestCase):
    def test_place(self):
        # Define test board
        test_board = [
            [Tile(type=TileType.EMPTY) for _ in range(5)] for _ in range(5)
        ]
        test_board[0][0].type = TileType.KING

        # Test placing on empty positions
        self.assertTrue(Board.place(test_board, 1, 1, 2, 2, Tile(type=TileType.FOREST), Tile(type=TileType.DESERT)))

        # Test placing on non-empty positions
        self.assertFalse(Board.place(test_board, 1, 1, 2, 2, Tile(type=TileType.KING), Tile(type=TileType.WATER)))

    def test_movement(self):
        # Define test board
        test_board = [
            [Tile(type=TileType.EMPTY) for _ in range(5)] for _ in range(5)
        ]
        test_board[0][1].type = TileType.KING

        # Test moving up
        self.assertEqual(Board.up(test_board, 0, 1, 1, 2), (0, 0, 1, 1))

        # Test moving down
        self.assertEqual(Board.down(test_board, 1, 1, 2, 2), (1, 2, 2, 3))

        # Test moving left
        self.assertEqual(Board.left(test_board, 1, 1, 2, 2), (0, 1, 1, 2))

        # Test moving right
        self.assertEqual(Board.right(test_board, 1, 1, 2, 2), (2, 1, 3, 2))

    def test_rotate(self):
        # Define test board
        test_board = [
            [Tile(type=TileType.EMPTY) for _ in range(5)] for _ in range(5)
        ]
        test_board[0][1].type = TileType.KING
        test_board[0][2].type = TileType.WATER

        # Test rotating from left to right
        self.assertEqual(Board.rotate(test_board, 0, 1, 0, 2), (0, 1, 1, 1))

        # Test rotating from right to left
        self.assertEqual(Board.rotate(test_board, 0, 2, 0, 1), (0, 2, -1, 2))

        # Test rotating from up to down
        self.assertEqual(Board.rotate(test_board, 0, 1, 1, 1), (0, 1, 0, 0))

        # Test rotating from down to up
        self.assertEqual(Board.rotate(test_board, 1, 1, 0, 1), (1, 1, 1, 2))

    def test_shift_down(self):
        # Define test board
        test_board = [
            [Tile(type=TileType.EMPTY) for _ in range(5)] for _ in range(5)
        ]
        test_board[0][1].type = TileType.KING

        # Test shifting down
        Board.shift_down(test_board)
        self.assertEqual(test_board[1][1].type, TileType.KING)
        self.assertEqual(test_board[0][1].type, TileType.EMPTY)

    def test_shift_up(self):
        # Define test board
        test_board = [
            [Tile(type=TileType.EMPTY) for _ in range(5)] for _ in range(5)
        ]
        test_board[4][1].type = TileType.KING

        # Test shifting up
        Board.shift_up(test_board)
        self.assertEqual(test_board[3][1].type, TileType.KING)
        self.assertEqual(test_board[4][1].type, TileType.EMPTY)

    def test_shift_left(self):
        # Define test board
        test_board = [
            [Tile(type=TileType.EMPTY) for _ in range(5)] for _ in range(5)
        ]
        test_board[1][4].type = TileType.KING

        # Test shifting left
        Board.shift_left(test_board)
        self.assertEqual(test_board[1][3].type, TileType.KING)
        self.assertEqual(test_board[1][4].type, TileType.EMPTY)

    def test_shift_right(self):
        # Define test board
        test_board = [
            [Tile(type=TileType.EMPTY) for _ in range(5)] for _ in range(5)
        ]
        test_board[1][0].type = TileType.KING

        #

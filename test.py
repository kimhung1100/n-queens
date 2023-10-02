import unittest
from nqueens_board import NQueens_board  # Replace 'your_module' with the actual module name where NQueens is defined

class TestNQueens(unittest.TestCase):
    def test_initialization(self):
        n = 8  # Change the size as needed
        board = NQueens_board(n)

        # Check if the board is correctly initialized
        self.assertEqual(board.size, n)
        self.assertEqual(board.queens, [-1] * n)
        self.assertEqual(board.row_conflicts, [0] * n)
        self.assertEqual(board.column_conflicts, [0] * n)
        self.assertEqual(board.left_diagonal_conflicts, [0] * (2 * n - 1))
        self.assertEqual(board.right_diagonal_conflicts, [0] * (2 * n - 1))
        self.assertEqual(board.total_conflicts, 0)
        self.assertEqual(board.queen_count, 0)
        self.assertEqual(board.order_queens, [])

    def test_place_queen_and_remove_queen(self):
        n = 8  # Change the size as needed
        board = NQueens_board(n)

        # Place a queen and check if the board is updated correctly
        board.place_queen(0, 3)
        self.assertEqual(board.queens, [3, -1, -1, -1, -1, -1, -1, -1])
        self.assertEqual(board.row_conflicts, [1, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(board.column_conflicts, [0, 0, 0, 1, 0, 0, 0, 0])
        # Continue with similar checks for other attributes

        # Remove the queen and check if the board is updated correctly
        board.remove_queen(0, 3)
        self.assertEqual(board.queens, [-1, -1, -1, -1, -1, -1, -1, -1])
        self.assertEqual(board.row_conflicts, [0, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(board.column_conflicts, [0, 0, 0, 0, 0, 0, 0, 0])
        # Continue with similar checks for other attributes

    def test_is_safe(self):
        n = 8  # Change the size as needed
        board = NQueens_board(n)

        # Place queens in safe positions and check if is_safe returns True
        self.assertTrue(board.is_safe(0, 0))
        self.assertTrue(board.is_safe(2, 3))
        # Continue with similar checks for other positions

        # Place queens in positions with conflicts and check if is_safe returns False
        board.place_queen(0, 3)
        self.assertFalse(board.is_safe(1, 3))
        # Continue with similar checks for other positions

    def test_calculate_conflicts(self):
        n = 8  # Change the size as needed
        board = NQueens_board(n)

        # Place queens in various positions and check if calculate_conflicts returns the expected count
        self.assertEqual(board.calculate_conflicts(), 0)
        board.place_queen(0, 3)
        self.assertEqual(board.calculate_conflicts(), 0)
        board.place_queen(1, 5)
        self.assertEqual(board.calculate_conflicts(), 0)
        # Continue with similar checks for other positions

    def test_is_goal(self):
        n = 8  # Change the size as needed
        board = NQueens_board(n)

        # Place queens to create a goal state and check if is_goal returns True
        board.place_queen(0, 3)
        board.place_queen(1, 1)
        board.place_queen(2, 6)
        # Continue with similar checks for other positions

        self.assertFalse(board.is_goal())

        # Place queens in a way that doesn't form a goal state and check if is_goal returns False
        board.clear_board()
        board.place_queen(0, 3)
        board.place_queen(1, 3)
        board.place_queen(2, 6)
        # Continue with similar checks for other positions

        self.assertFalse(board.is_goal())

    def test_full_board(self):
        n = 8  # Change the size as needed
        board = NQueens_board(n)

        # Place queens in a way that forms a goal state (no conflicts)
        board.place_queen(0, 0)
        board.place_queen(1, 2)
        board.place_queen(2, 4)
        board.place_queen(3, 7)
        board.place_queen(4, 5)
        board.place_queen(5, 3)
        board.place_queen(6, 6)
        board.place_queen(7, 1)
        self.assertFalse(board.is_goal())

    def test_goal_state(self):
        n = 8  # Change the size as needed
        queen_positions = [0, 4, 7, 5, 2, 6, 1, 3]
        board = NQueens_board(n)

        # Place queens in the specified positions
        for row, col in enumerate(queen_positions):
            board.place_queen(row, col)

        self.assertTrue(board.is_goal())

    def test_goal_state1(self):
        n = 12  # Change the size as needed
        queen_positions = [0, 2, 3, 10, 5, 9, 1, 3, 0, 6, 9, 2]
        board = NQueens_board(n)

        # Place queens in the specified positions
        for row, col in enumerate(queen_positions):
            board.place_queen(row, col)

        self.assertFalse(board.is_goal())

    def test_goal_state2(self):
        n = 4  # Set the size of the board
        test_board = NQueens_board(n)

        # Place queens at the specified positions
        test_board.place_queen(0, 1)
        test_board.place_queen(1, 3)
        test_board.place_queen(2, 2)
        test_board.place_queen(3, 0)

        self.assertFalse(test_board.is_goal())

if __name__ == '__main__':
    unittest.main()

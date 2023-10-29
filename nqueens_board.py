import copy
import random
class NQueens_board:
    def __init__(self, size):
        self.size = size
        self.queens = [-1] * size  # List to store the column index of queens in each row
        self.row_conflicts = [0] * size  # Count of queens in each row
        self.column_conflicts = [0] * size  # Count of queens in each column
        self.left_diagonal_conflicts = [0] * (2 * size - 1)  # Count of queens in left diagonals
        self.right_diagonal_conflicts = [0] * (2 * size - 1)  # Count of queens in right diagonals
        self.total_conflicts = 0
        self.queen_count = 0
        self.order_queens = []
    def place_queen(self, row, col):
        self.queens[row] = col
        self.row_conflicts[row] += 1
        self.column_conflicts[col] += 1
        self.left_diagonal_conflicts[row + col] += 1
        self.right_diagonal_conflicts[row - col + self.size - 1] += 1
        self.total_conflicts += (self.row_conflicts[row]
                                 + self.column_conflicts[col]
                                 + self.left_diagonal_conflicts[row + col]
                                 + self.right_diagonal_conflicts[row - col + self.size - 1]
                                 - 4)
        self.queen_count += 1
        self.order_queens.append((row, col))
    def remove_queen(self, row, col):
        self.total_conflicts -= (self.row_conflicts[row]
                                 + self.column_conflicts[col]
                                 + self.left_diagonal_conflicts[row + col]
                                 + self.right_diagonal_conflicts[row - col + self.size - 1]
                                 - 4)
        self.queens[row] = -1
        self.row_conflicts[row] -= 1
        self.column_conflicts[col] -= 1
        self.left_diagonal_conflicts[row + col] -= 1
        self.right_diagonal_conflicts[row - col + self.size - 1] -= 1

        self.queen_count -= 1
        self.order_queens.pop()
    def calculate_conflicts(self):
        # Calculate the total number of conflicts in the current state
        return self.total_conflicts

    def is_goal(self):
        return self.total_conflicts == 0 and self.queen_count == self.size

    def print_board(self):
        for row in range(self.size):
            line = ["Q" if col == self.queens[row] else "." for col in range(self.size)]
            print(" ".join(line))

    def expand(self, row = -1, col = -1):
        """
        Generates the next queen board states by considering all valid positions
        to place a queen in the next row.
        If the current row has no queens (initial state),
        consider all columns in the first row.

        :param row: The current row.
        :param col: The current column (queen's column) in the current row.
        :return: A list of next board states.
        """
        next_states = []
        # Iterate through each column in the next row
        for next_col in range(self.size):
            if self.is_safe(row + 1, next_col):
                # Create a copy of the current board
                next_board = copy.deepcopy(self)
                # Place a queen in the valid position in the next row
                next_board.place_queen(row + 1, next_col)
                next_states.append(next_board)

        return next_states
    def is_safe(self, row: int, col: int):
        """
        Checks if it's safe to place a queen in the specified cell (row, col) on the chessboard.

        :param row: The row in which to place the queen.
        :param col: The column in which to place the queen.
        :return: True if it's safe to place a queen in the cell, False otherwise.
        """
        # Check if there's a queen in the same column
        if col in self.queens:
            return False

        # Check if there's a queen in the left diagonal
        if self.left_diagonal_conflicts[row + col] != 0:
            return False

        # Check if there's a queen in the right diagonal
        if self.right_diagonal_conflicts[row - col + self.size - 1] != 0:
            return False

        # If none of the above conditions are met, it's safe to place a queen in this cell
        return True

    def generate_random(self):
        # Clear the board and conflicts
        self.clear_board()

        # Place queens randomly in each row
        for row in range(self.size):
            col = random.randint(0, self.size - 1)
            self.place_queen(row, col)
    def generate_random_distinct(self):
        # Clear the board and conflicts
        self.clear_board()

        # Create a list of column indices, shuffle it
        columns = list(range(self.size))
        random.shuffle(columns)

        # Place queens in distinct columns
        for row in range(self.size):
            col = columns.pop()
            self.place_queen(row, col)

    def clear_board(self):
        # Clear the board and reset conflicts
        self.queens = [-1] * self.size
        self.row_conflicts = [0] * self.size
        self.column_conflicts = [0] * self.size
        self.left_diagonal_conflicts = [0] * (2 * self.size - 1)
        self.right_diagonal_conflicts = [0] * (2 * self.size - 1)
        self.total_conflicts = 0
        self.queen_count = 0
        self.order_queens = []
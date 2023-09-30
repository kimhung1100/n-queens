import copy


class Chessboard:
    def __init__(self, size: int):
        self.size = size
        self.row = -1
        self.col = -1
        self.board = [["." for _ in range(size)] for _ in range(size)]
        self.queens_in_row = set()
        self.queens_in_col = set()
        self.queens_in_main_diag = set()
        self.queens_in_anti_diag = set()

    def copy_board(self, board):
        self.size = board.size
        self.row = board.row
        self.col = board.col
        self.board = board.board
        self.queens_in_row = board.queens_in_row
        self.queens_in_col = board.queens_in_col
        self.queens_in_main_diag = board.queens_in_main_diag
        self.queens_in_anti_diag = board.queens_in_anti_diag

    def place_queen(self, row: int, col: int):
        if self.is_valid_position(row, col):
            self.board[row][col] = "Q"
            self.queens_in_row.add(row)
            self.queens_in_col.add(col)
            self.queens_in_main_diag.add(row - col)
            self.queens_in_anti_diag.add(row + col)
            self.row = row
            self.col = col
            return True
        return False

    def remove_queen(self, row: int, col: int):
        if self.is_valid_position(row, col) and self.board[row][col] == "Q":
            self.board[row][col] = "."
            self.queens_in_row.remove(row)
            self.queens_in_col.remove(col)
            self.queens_in_main_diag.remove(row - col)
            self.queens_in_anti_diag.remove(row + col)
            return True
        return False

    def is_valid_position(self, row: int, col: int):
        return (
            row not in self.queens_in_row
            and col not in self.queens_in_col
            and (row - col) not in self.queens_in_main_diag
            and (row + col) not in self.queens_in_anti_diag
        )

    def __str__(self):
        return "\n".join([" ".join(row) for row in self.board])

    def get_board(self):
        return self.board

    def print_board(self):
        """
        Prints the current board configuration.
        """
        for row in self.board:
            print(" ".join(row))

    def is_goal(self):
        # Check if the current board configuration is a valid solution
        return len(self.queens_in_row) == self.size

    def is_safe(self, row: int, col: int):
        # Helper method to check if a queen at (row, col) is safe
        # from other queens (no conflicts)
        for i in range(col):
            if self.board[row][i] == "Q":
                return False

            for j in range(row, self.size):
                if self.board[j][i] == "Q":
                    return False

            # check diagonal from top-left to bottom-right
            for j in range(1, min(row, col) + 1):
                if self.board[row - j][col - j] == "Q":
                    return False
            # check diagonal from bottom-left to top-right
            for j in range(1, min(self.size - row - 1, col) + 1):
                if self.board[row + j][col - j] == "Q":
                    return False

        return True

    def expand(self, row: int, col: int):
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

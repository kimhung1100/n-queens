from collections import deque
#from board import Chessboard
import random
import math
from nqueens_board import NQueens_board

def breadth_first_search(n: int):
    """
    Implemented based on pseudo-code textbook in page 95

    Time and space complexity: O(b^d)

    Return a solution node or a failure

        :rtype: board
    """
    board = NQueens_board(n)

    if board.is_goal():
        return board
    frontier = deque()
    frontier.append(board)
    reached = [board.queens]
    while frontier:
        node = frontier.popleft()  # Dequeue the first node from the frontier

        # Expand the current node and generate next board states
        if node.order_queens:
            # If the order_queens list is not empty, get the position of the last queen.
            next_states = node.expand(node.order_queens[-1][0], node.order_queens[-1][1])
        else:
            # If the order_queens list is empty, pass (-1, -1) as parameters.
            next_states = node.expand(-1, -1)

        for next_state in next_states:
            # Check if the next state is a goal state
            if next_state.is_goal():
                return next_state  # Return the goal state

            # Check if the next state has not been reached before
            if next_state.queens not in reached:
                reached.append(next_state.queens)  # Add the next state to reached
                frontier.append(
                    next_state
                )  # Enqueue the next state for further exploration

            # If the BFS doesn't find a solution, return None or handle it as needed
    return None


def initialize_board(n: int):
    # Create a list of integers from 0 to N-1 representing column positions.
    initial_board = list(range(n))

    # Shuffle the list to randomize the queen placements.
    random.shuffle(initial_board)

    return initial_board


def calculate_fitness(board):
    n = len(board)
    conflicts = 0

    for i in range(n):
        for j in range(i + 1, n):
            # Check for conflicts in the same column
            if board[i] == board[j]:
                conflicts += 1
            # Check for conflicts in diagonals
            if abs(board[i] - board[j]) == abs(i - j):
                conflicts += 1

    return conflicts


def generate_neighbor(board):
    n = len(board)

    # Choose a random row and a random column to move the queen in that row.
    random_row = random.randint(0, n - 1)
    random_col = random.randint(0, n - 1)

    # Ensure that the randomly chosen column is different from the current column.
    while board[random_row] == random_col:
        random_col = random.randint(0, n - 1)

    # Create a copy of the current board to represent the neighbor.
    neighbor_board = list(board)

    # Move the queen in the randomly chosen row to the new column.
    neighbor_board[random_row] = random_col

    return neighbor_board


def simulated_annealing(n: int):
    """
    present board in array int
    :param n:
    :return:
    """
    current_state = initialize_board(n)

    # Set the initial temperature and cooling rate for annealing.
    temperature = 1000
    cooling_rate = 0.95

    # Initialize the best state and best fitness (number of conflicts).
    best_state = current_state
    best_fitness = calculate_fitness(current_state)

    # Iterate until a solution is found or the temperature is too low.
    while temperature > 0:
        # Generate a neighboring state by making a random move or perturbation.
        neighbor_state = generate_neighbor(current_state)

        # Calculate fitness (number of conflicts) for both current and neighbor states.
        current_fitness = calculate_fitness(current_state)
        neighbor_fitness = calculate_fitness(neighbor_state)

        # Calculate the change in fitness (delta E).
        delta_fitness = neighbor_fitness - current_fitness

        # If the neighbor state has fewer conflicts or is better, accept it.
        if delta_fitness < 0 or random.random() < math.exp(
            -delta_fitness / temperature
        ):
            current_state = neighbor_state
            current_fitness = neighbor_fitness

            # If this is a new best state, update it.
            if current_fitness < best_fitness:
                best_state = current_state
                best_fitness = current_fitness

        # Reduce the temperature according to the cooling rate.
        temperature *= cooling_rate

    # Return the best state found.
    return best_state

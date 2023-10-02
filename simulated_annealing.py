from nqueens_board import NQueens_board
import random
import math
import copy
def simulated_annealing(n, max_iterations, initial_temperature, cooling_rate):
    current_state = NQueens_board(n)
    current_state.generate_random()
    best_state = current_state
    best_conflicts = current_state.total_conflicts
    temperature = initial_temperature

    for _ in range(max_iterations):
        if best_conflicts == 0:
            return best_state

        # Randomly select a queen and a new position for it
        row = random.randint(0, n - 1)
        new_col = random.randint(0, n - 1)
        old_col = current_state.queens[row]
        current_conflicts = current_state.total_conflicts
        current_state.remove_queen(row, old_col)
        current_state.place_queen(row, new_col)
        new_conflicts = current_state.total_conflicts

        # Calculate change in conflicts
        delta_conflicts = new_conflicts - current_conflicts

        # If the move is better or accepted by probability, keep it
        if delta_conflicts <= 0 or random.random() < math.exp(-delta_conflicts / temperature):
            current_conflicts = new_conflicts
            if current_conflicts < best_conflicts:
                best_state = current_state
                best_conflicts = current_conflicts
        else:
            # Revert the move if not accepted
            current_state.remove_queen(row, current_state.queens[row])
            current_state.place_queen(row, old_col)

        # Reduce temperature
        temperature *= cooling_rate

    return best_state

def nQueens_heuristics(state: NQueens_board, n: int):
    position1 = random.randint(0, n - 1)
    position2 = random.randint(0, n - 1)
    new_state = copy.deepcopy(state)
    new_state.remove_queen(position1, new_state.queens[position1])
    new_state.place_queen(position1, state.queens[position2])

    new_state.remove_queen(position2, new_state.queens[position2])
    new_state.place_queen(position2, state.queens[position1])
    return new_state

def sa_nqueens(cooling_rate, temperature, n):
    # heuristics
    queen_positions = list(range(n))
    current_state = NQueens_board(n)

    # Place queens in the specified positions
    for row, col in enumerate(queen_positions):
        current_state.place_queen(row, col)

    current_conflicts = current_state.total_conflicts

    while current_conflicts > 0:
        next_state = nQueens_heuristics(current_state, n)
        if next_state.total_conflicts < current_conflicts:
            current_state = copy.deepcopy(next_state)
            current_conflicts = next_state.total_conflicts
        else:

            delta_fitness = next_state.total_conflicts - current_conflicts
            if random.random() < math.exp(-delta_fitness / temperature):
                current_state = copy.deepcopy(next_state)
                current_conflicts = next_state.total_conflicts
        temperature = temperature*cooling_rate

    return current_state
# Example usage:
if __name__ == '__main__':
    n = 30  # Number of queens
    initial_temperature = 1000.0
    cooling_rate = 0.99

    solution = sa_nqueens(cooling_rate, initial_temperature, n)
    solution.print_board()
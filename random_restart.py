import random
import main


def is_goal(state):
    # Check if the current state is a goal state.
    # A goal state has no conflicts between queens.
    n = len(state)
    for i in range(n):
        for j in range(i + 1, n):
            if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                return False
    return True


def calculate_conflicts(state):
    # Calculate the number of conflicts (attacks) in the current state.
    # Return the count of conflicts.
    n = len(state)
    conflicts = 0
    for i in range(n):
        for j in range(i + 1, n):
            if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                conflicts += 1
    return conflicts


def random_restart_hill_climbing(n, max_iterations):
    best_solution = None
    best_conflicts = float("inf")  # Initialize to positive infinity.

    for _ in range(max_iterations):
        # Initialize a random or semi-random state as the current state.
        current_state = [random.randint(0, n - 1) for _ in range(n)]

        while True:
            # Calculate the number of conflicts in the current state.
            current_conflicts = calculate_conflicts(current_state)

            if current_conflicts == 0:
                # If no conflicts are found, it's a goal state.
                # Return the current state as the solution.
                return current_state

            # Generate neighboring states by moving one queen at a time.
            neighbors = []

            for queen in range(n):
                for new_col in range(n):
                    if current_state[queen] != new_col:
                        neighbor = list(current_state)
                        neighbor[queen] = new_col
                        neighbors.append(neighbor)

            # Find the neighbor with the fewest conflicts.
            min_neighbor = min(neighbors, key=lambda state: calculate_conflicts(state))

            if calculate_conflicts(min_neighbor) >= current_conflicts:
                # If no neighbor has fewer conflicts, we're at a local optimum.
                # Break out of the inner loop.
                break

            # Move to the neighbor with fewer conflicts.
            current_state = min_neighbor

        # Check if the current local optimum is better than the best solution found so far.
        if current_conflicts < best_conflicts:
            best_solution = current_state
            best_conflicts = current_conflicts

    # Return the best solution found across all restarts.
    return best_solution


if __name__ == "__main__":
    # Example usage:
    n = 25  # Number of queens
    max_iterations = 1000  # Maximum iterations for random restarts
    solution = random_restart_hill_climbing(n, max_iterations)
    print("Best Solution:", solution)
    main.print_queens_board(solution)

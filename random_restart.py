import random
import main
from nqueens_board import NQueens_board
import copy
import multiprocessing
import asyncio
import concurrent.futures
import  time

# def is_goal(state):
#     # Check if the current state is a goal state.
#     # A goal state has no conflicts between queens.
#     n = len(state)
#     for i in range(n):
#         for j in range(i + 1, n):
#             if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
#                 return False
#     return True


# def calculate_conflicts(state):
#     # Calculate the number of conflicts (attacks) in the current state.
#     # Return the count of conflicts.
#     n = len(state)
#     conflicts = 0
#     for i in range(n):
#         for j in range(i + 1, n):
#             if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
#                 conflicts += 1
#     return conflicts
def get_min_conflicts_successor(current_state):
    n = current_state.size
    min_conflicts = float("inf")
    best_successor = None

    # Generate neighboring states by moving one queen at a time.
    neighbors = []
    for row in range(n):
        for new_col in range(n):
            if current_state.queens[row] != new_col:
                neighbor = copy.deepcopy(current_state)
                neighbor.remove_queen(row, current_state.queens[row])
                neighbor.place_queen(row, new_col)
                if(neighbor.total_conflicts < current_state.total_conflicts):
                    neighbors.append(neighbor)
    # pick best neighbors
    if(len(neighbors) > 0):
        current_state = min(neighbors, key=lambda state: state.total_conflicts)

    return current_state

def nQueens_heuristics(state: NQueens_board):
    n = state.size
    position1 = random.randint(0, n - 1)
    position2 = random.randint(0, n - 1)
    new_state = copy.deepcopy(state)
    new_state.remove_queen(position1, new_state.queens[position1])
    new_state.place_queen(position1, state.queens[position2])

    new_state.remove_queen(position2, new_state.queens[position2])
    new_state.place_queen(position2, state.queens[position1])
    return new_state

def hill_climbing(n):
    current = NQueens_board(n)
    current.generate_random_distinct()
    iterate = 0
    while True:
        min_conflict_neighbor = get_min_conflicts_successor(current)
        with open("hill_climb.txt", "a") as f:
            f.write(f"{min_conflict_neighbor.total_conflicts}\n")

        if min_conflict_neighbor.total_conflicts >= current.total_conflicts or iterate == n:
            return min_conflict_neighbor
        current = min_conflict_neighbor
        iterate += 1



def random_restart_hill_climbing(n):
    best_solution = None
    best_conflicts = float("inf")  # Initialize to positive infinity.

    iteration = 0
    while best_conflicts:
        iteration += 1

        result = hill_climbing(n)

        if result.total_conflicts < best_conflicts:
            best_solution = result
            best_conflicts = result.total_conflicts
        print(best_conflicts)
        print(result.total_conflicts)

    return best_solution

async def run_hill_climbing(n, consecutive_iterations_to_terminate=50):
    return hill_climbing(n, consecutive_iterations_to_terminate)

async def parallel_random_restart_hill_climbing(n, num_processes, consecutive_iterations_to_terminate=50):
    best_solution = None
    best_conflicts = float("inf")
    restarts = 0
    with concurrent.futures.ProcessPoolExecutor(max_workers=num_processes) as executor:
        while best_conflicts > 0:
            tasks = [run_hill_climbing(n, consecutive_iterations_to_terminate) for _ in range(num_processes)]
            results = await asyncio.gather(*tasks)
            for result in results:
                if result.total_conflicts < best_conflicts:
                    best_solution = result
                    best_conflicts = result.total_conflicts
            restarts += 1
            print(best_conflicts)

    return best_solution, restarts

def random_restart_hill_climbing_annealing(n, max_iterations, restarts = 100):
    """
    Solves the N-Queens problem using random restart hill climbing.

    Args:
        n: The number of queens.
        max_iterations: The maximum number of iterations for each restart.
        restarts: The number of restarts.

    Returns:
        A solution to the N-Queens problem, or None if no solution is found.
    """

    for _ in range(restarts):
        # Initialize a random or semi-random state as the current state.
        current_state = NQueens_board(n)
        current_state.generate_random()

        # Calculate the initial number of conflicts.
        current_conflicts = current_state.total_conflicts

        # Set the initial temperature for simulated annealing.
        temperature = 1.0

        for _ in range(max_iterations):
            # Calculate the cooling factor for simulated annealing.
            cooling_factor = temperature / (temperature + 1.0)

            # Generate neighboring states by moving one queen at a time.
            neighbors = []

            for row in range(n):
                for new_col in range(n):
                    if current_state.queens[row] != new_col:
                        neighbor = copy.deepcopy(current_state)
                        neighbor.remove_queen(row, current_state.queens[row])
                        neighbor.place_queen(row, new_col)
                        neighbors.append(neighbor)

            # Find the neighbor with the fewest conflicts.
            min_neighbor = min(neighbors, key=lambda state: state.total_conflicts)

            # If the neighbor has fewer conflicts, accept it.
            if min_neighbor.total_conflicts < current_conflicts:
                current_state = min_neighbor
                current_conflicts = min_neighbor.total_conflicts

            # Otherwise, accept the neighbor with a probability that is proportional to the cooling factor.
            else:
                delta_conflicts = min_neighbor.total_conflicts - current_conflicts
                acceptance_probability = random.random() ** (delta_conflicts / temperature)

                if acceptance_probability > 0.5:
                    current_state = min_neighbor
                    current_conflicts = min_neighbor.total_conflicts

            # Update the temperature for simulated annealing.
            temperature *= cooling_factor

            # If no conflicts are found, it's a goal state.
            # Return the current state as the solution.
            if current_conflicts == 0:
                return current_state

    # If we reach this point, no solution was found.
    return None

def run_test_parallel_hill(n):
    loop = asyncio.get_event_loop()
    best_solution = loop.run_until_complete(parallel_random_restart_hill_climbing(n, num_processes=8))
    print("Best solution found:", best_solution[0].queens, best_solution[1])
    # best_solution.print_board()

def run_test_rr_hc(n):
    best_solution = random_restart_hill_climbing(n)
    print(best_solution.queens)
    best_solution.print_board()

if __name__ == "__main__":
    n = int(input("Input n: "))
    start = time.time()
    print("start: ", start)
    run_test_rr_hc(n)
    print(time.time() - start)




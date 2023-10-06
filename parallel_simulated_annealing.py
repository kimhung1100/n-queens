import multiprocessing
import random
import math
import copy
from multiprocessing import Pool
from simulated_annealing import nQueens_heuristics
from nqueens_board import NQueens_board

def sa_nqueens_worker(args):
    cooling_rate, temperature, n, seed = args

    # Set random seed for reproducibility
    random.seed(seed)

    queen_positions = list(range(n))
    current_state = NQueens_board(n)

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
        temperature = temperature * cooling_rate

    return current_state


def parallel_sa_nqueens(cooling_rate, temperature, n, num_processes):
    # Generate random seeds for parallel runs
    seeds = [random.randint(1, 10000) for _ in range(num_processes)]

    # Create a pool of worker processes
    pool = Pool(processes=num_processes)

    # Define arguments for parallel execution
    args = [(cooling_rate, temperature, n, seed) for seed in seeds]

    # Execute parallel simulations
    results = pool.map(sa_nqueens_worker, args)

    # Find the best solution among the results
    best_solution = min(results, key=lambda x: x.total_conflicts)

    return best_solution

if __name__ == "__main__":
    # Example usage:
    print(multiprocessing.cpu_count())
    n = 25 # Number of queens
    cooling_rate = 0.99  # Cooling rate
    temperature = 1000.0  # Initial temperature
    num_processes = 6  # Number of parallel processes

    best_solution = parallel_sa_nqueens(cooling_rate, temperature, n, num_processes)

    print("Best Solution:")
    best_solution.print_board()





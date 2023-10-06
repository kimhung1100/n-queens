from solver_algorithm import *
from board import *
import time
from random_restart import *
from simulated_annealing import *
from parallel_simulated_annealing import *
from divide_conquer import *
def print_queens_board(solution):
    n = solution.size
    for row in range(n):
        row_string = ""
        for col in range(n):
            if solution.queens[row] == col:
                row_string += "Q "
            else:
                row_string += ". "
        print(row_string.strip())  # Remove trailing space and print the row


def log_statistics(choice: int, solutions: [int], execution_time, max_iterations=-1):
    stats_files = [
        "dfs_stats.txt",
        "brfs_stats.txt",
        "sa_stats.txt",
        "rrhc_stats.txt",
        "p_sa_stats.txt",
        "dev_sa_stats.txt",
    ]
    with open(stats_files[choice - 1], "a") as f:
        f.write(f"{solutions.size},")
        if max_iterations != -1:
            f.write(f"{max_iterations},")
        f.write(f"{execution_time},")
        f.write(f"{solutions.queens}\n")

def solve_nqueens(n, choice, max_iterations=0):
    if choice == 1:
        pass
    elif choice == 2:
        sol = breadth_first_search(n)
    elif choice == 3:
        initial_temperature = 1000.0
        cooling_rate = 0.99
        sol = sa_nqueens(cooling_rate, initial_temperature, n)
    elif choice == 4:
        if max_iterations == 0:
            max_iterations = int(input("Enter the max iterations: "))
        sol = random_restart_hill_climbing(n, max_iterations)
    elif choice == 5:
        initial_temperature = 1000.0
        cooling_rate = 0.99
        num_processes = multiprocessing.cpu_count()  # Number of parallel processes
        sol = parallel_sa_nqueens(cooling_rate, initial_temperature, n, num_processes)
    elif choice == 6:
        initial_temperature = 1000.0
        cooling_rate = 0.99
        sol = divide_conquer(cooling_rate, initial_temperature, n)
    else:
        print("Invalid choice")
        return None

    return sol

if __name__ == "__main__":
    print("N-queens solver")
    n = int(input("Enter the size of the chessboard (N): "))
    if n == 2 or n == 3:
        print("No solution")
    else:
        print("Choice of algorithm: ")
        print("1. Depth first search (not implemented)")
        print("2. Breadth first search")
        print("3. Stimulated annealing")
        print("4. Random-restart hill climbing")
        print("5. Parallel stimulated annealing")
        print("6. Divide and conquer stimulate annealing")
        choice = int(input("Enter the choice of the algorithm: "))
        start = time.time()
        max_iterations = 0
        sol = solve_nqueens(n, choice)

        if sol is None:
            print("No solution found")
        else:
            print("A solution: ")
            if choice == 2:
                sol.print_board()
            if choice == 3 or choice == 4:
                print(sol.queens)
                print_queens_board(sol)

        print("Runtime in seconds:", time.time() - start)
        log_statistics(choice, sol, time.time() - start, max_iterations)
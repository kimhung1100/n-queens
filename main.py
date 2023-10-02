from solver_algorithm import *
from board import *
import time
from random_restart import *
from simulated_annealing import *

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


def log_statistics(choice: int, solutions: [int], execution_times, max_iterations=-1):
    stas_file = [
        "dfs_stats.txt",
        "brfs_stats.txt",
        "sa_stats.txt",
        "rrhc_stats.txt",
    ]
    with open(stas_file[choice - 1], "a") as f:
        f.write(str(solutions.size))
        f.write(",")
        if max_iterations != -1:
            f.write(str(max_iterations))
            f.write(",")
        f.write(str(execution_times))
        f.write(",")
        f.write(str(solutions.queens))
        f.write("\n")
    f.close()


if __name__ == "__main__":
    print("N-queens solver")
    n = int(input("Enter the size of the chessboard (N): "))
    if n == 2 or n == 3:
        print("No solution")
    print("Choice of algorithm: ")
    print("1. Depth first search (not implemented)")
    print("2. Breadth first search")
    print("3. Stimulated annealing")
    print("4. Random-restart hill climbing")
    choice = int(input("Enter the choice of the algorithm: "))
    start = time.time()
    max_iterations = 0
    if choice == 1:
        pass
    elif choice == 2:
        sol = breadth_first_search(n)
    elif choice == 3:
        initial_temperature = 1000.0
        cooling_rate = 0.99

        sol = sa_nqueens(cooling_rate, initial_temperature, n)
    elif choice == 4:
        print(
            "Max iterations\n"
            "This increases the chances of finding a better solution, \n"
            "especially when dealing with complex problems or large search spaces\n"
            "This can lead to quicker runs but may result in the algorithm \n"
            "getting stuck in local optima, especially for challenging problem instances.\n"
        )
        max_iterations = int(input("Enter the max iterations: "))

        sol = random_restart_hill_climbing(n, max_iterations)
    if sol == None:
        print("No solution found")
    else:
        print("A solution: ")
        if choice == 2:
            sol.print_board()
        if choice == 3 or choice == 4:
            print(sol.queens)
            print_queens_board(sol)
    print("Runtime in second:", time.time() - start)

    log_statistics(choice, sol, time.time() - start, max_iterations)

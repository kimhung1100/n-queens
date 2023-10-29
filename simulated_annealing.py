from nqueens_board import NQueens_board
import random
import math
import copy
import time

def nQueens_heuristics(state: NQueens_board, n: int):
    position1 = random.randint(0, n - 1)
    position2 = random.randint(0, n - 1)
    new_state = copy.deepcopy(state)
    new_state.remove_queen(position1, new_state.queens[position1])
    new_state.place_queen(position1, state.queens[position2])

    new_state.remove_queen(position2, new_state.queens[position2])
    new_state.place_queen(position2, state.queens[position1])
    return new_state
def gradient_heuristics_nQueens(state: NQueens_board, n: int):
    swaps_performed = 0

    while True:
        swaps_performed = 0

        for i in range(n):
            for j in range(i + 1, n):
                queen_i = i
                queen_j = j

                if not state.is_safe(queen_i, state.queens[i] or not state.is_safe(queen_j, state.queens[j])):
                    # Calculate the number of collisions with the current queens
                    current_collisions = state.calculate_conflicts()

                    # Swap queens
                    state.remove_queen(queen_i, state.queens[queen_i])
                    state.place_queen(queen_i, state.queens[queen_j])
                    state.remove_queen(queen_j, state.queens[queen_j])
                    state.place_queen(queen_j, state.queens[queen_i])

                    # Calculate the number of collisions after the swap
                    new_collisions = state.calculate_conflicts()

                    if new_collisions < current_collisions:
                        # Swap reduces collisions, accept the swap
                        swaps_performed += 1
                    else:
                        # Swap increases or maintains collisions, undo the swap
                        state.remove_queen(queen_i, state.queens[queen_i])
                        state.place_queen(queen_i, state.queens[queen_j])
                        state.remove_queen(queen_j, state.queens[queen_j])
                        state.place_queen(queen_j, state.queens[queen_i])

        if swaps_performed == 0:
            # No more swaps can be performed to reduce collisions, exit the loop
            nQueens_heuristics(state, n)
            break

    return state
def sa_nqueens(start, cooling_rate, temperature, n, current_state = None):
    # heuristics
    if not current_state:
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
        delta_fitness = next_state.total_conflicts - current_conflicts

        print(current_conflicts)
        with open("sa_step_print.txt", "a") as f:
            f.write(f"{current_conflicts} ")
            f.write(f"{temperature}\n")

    return current_state

def sa_stop(start, cooling_rate, temperature, n, current_state = None):
    # heuristics
    if not current_state:
        queen_positions = list(range(n))
        current_state = NQueens_board(n)

        # Place queens in the specified positions
        for row, col in enumerate(queen_positions):
            current_state.place_queen(row, col)

    max_iter = n * 5000
    iter = 0
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
        delta_fitness = next_state.total_conflicts - current_conflicts

        print(current_conflicts)
        with open("sa_step.txt", "w") as f:
            f.write(f"{time.time() - start},")
            f.write(f"{current_conflicts},")
            f.write(f"{current_state.queens},")
            f.write(f"{math.exp(-delta_fitness / temperature)}\n")
        iter += 1
        if (iter >= max_iter):
            break

    return current_state

def simulate_anealing_restart(n):
    cooling_rate = .99
    initial_temperature = 1000.0
    temp_range = 100

    iteration = 0
    start = time.time()
    queen_positions = list(range(n))
    current_state = NQueens_board(n)

    # Place queens in the specified positions
    for row, col in enumerate(queen_positions):
        current_state.place_queen(row, col)
    best_conflicts = current_state.total_conflicts
    best_solution = current_state
    while best_conflicts:
        iteration += 1
        result = sa_stop(start, cooling_rate, initial_temperature, n,  current_state)

        if result.total_conflicts < best_conflicts:
            best_solution = result
            best_conflicts = result.total_conflicts
        print(best_conflicts)
        print(result.total_conflicts)

    return best_solution

def very_fast_sa(start, cooling_rate, initial_temperature, n, current_state = None):
    if not current_state:
        queen_positions = list(range(n))
        current_state = NQueens_board(n)

        # Place queens in the specified positions
        for row, col in enumerate(queen_positions):
            current_state.place_queen(row, col)


    current_conflicts = current_state.total_conflicts
    iteration = 0
    reanneal_interval = 10000
    temperature = initial_temperature
    while(current_conflicts > 0):
        next_state = nQueens_heuristics(current_state, n)
        if next_state.total_conflicts < current_conflicts:
            current_state = copy.deepcopy(next_state)
            current_conflicts = next_state.total_conflicts
        else:

            delta_fitness = next_state.total_conflicts - current_conflicts
            if random.random() < math.exp(-delta_fitness / temperature):
                current_state = copy.deepcopy(next_state)
                current_conflicts = next_state.total_conflicts

        if iteration % reanneal_interval == 0:
            temperature = current_conflicts*1/(iteration + 1)

        temperature *= cooling_rate
        iteration += 1
        print(current_conflicts)
        with open("vf_sa_step.txt", "w") as f:
            f.write(f"{time.time() - start},")
            f.write(f"{current_conflicts},")
            f.write(f"{current_state.queens},")
            f.write(f"{temperature}\n")

    return current_state


# Example usage:
if __name__ == '__main__':
    n = int(input("Inpute N: "))
    initial_temperature = 1000.0
    cooling_rate = 0.99
    start = time.time()
    solution = simulate_anealing_restart(n)
    solution.print_board()
    print("Runtime in second:", time.time() - start)
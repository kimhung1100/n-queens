from nqueens_board import NQueens_board
import math
from simulated_annealing import *

def calculate_A_and_B(N):
    # Helper function to check if a number is divisible by 2 or 3
    def is_divisible_by_2_or_3(num):
        return num % 2 == 0 or num % 3 == 0

    B = 1
    A = N

    # Find B and A such that B is the smallest possible value
    while A >= B:
        B += 1
        A = N // B
        if N == A * B and not is_divisible_by_2_or_3(A) and (B % 6 == 0 or B % 6 == 4 or B % 6 == 2):
            return A, B

    # If no suitable A and B are found, return None
    return None, None
def cal_A_and_B(n: int):
    sqrt_n = int(math.sqrt(n))

    # Initialize A and B to the starting point (sqrt(n))
    A = sqrt_n
    B = sqrt_n

    while A * B != n:
        if A * B < n:
            B += 1
        else:
            A -= 1

    return A, B

def select_yagolm_sol(b: int):
    if b % 6 == 0 or b % 6 == 4:
        return 1
    elif b % 6 == 2:
        return 2
    return -1
def divide_conquer(cooling_rate: float, initial_temperature: float, n: int):

    nA, nB = cal_A_and_B(n)
    # pattern_A = sa_nqueens(cooling_rate, initial_temperature, nA).queens
    # nA = 7
    # nB = 5
    # if nA % 6 == 0 or nA % 6 == 4:
    #     board_pattern_A = NQueens_board(nA)
    #     for i in range(0, nA // 2):
    #         board_pattern_A.place_queen(i, i* 2 + 1)
    #     for i in range(nA // 2, nA):
    #         board_pattern_A.place_queen(i, (i - nA// 2)* 2)
    #     pattern_A = board_pattern_A.queens
    # elif nA % 6 == 2:
    #     pass
    pattern_A = sa_nqueens(cooling_rate, initial_temperature, nA)
    pattern_B = sa_nqueens(cooling_rate, initial_temperature, nB)
    combined_board = NQueens_board(n)

    ## Place pattern B solutions into each position of pattern A
    for i in range(n):
        position_in_pattern_A = pattern_A.queens[i//nB]
        position_in_pattern_B = pattern_B.queens[i%nB]
        combined_position = position_in_pattern_A*nA + position_in_pattern_B
        combined_board.place_queen(i, combined_position)

    sol = sa_nqueens(cooling_rate, initial_temperature, n, combined_board)
    return sol


if __name__ == '__main__':
    sol = divide_conquer(.99, 1000.0, 100)
    print(sol.queens)
    sol.print_board()
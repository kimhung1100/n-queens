from solver_algorithm import *
from board import *

if __name__ == "__main__":
    print("N-queens solver")
    n = int(input("Enter the size of the chessboard (N): "))
    print("Choice of algorithm: ")
    print("1. Breadth first search")
    choice = int(input("Enter the choice of the algorithm: "))
    if choice == 1:
        print("A solution: ")
        sol = breadth_first_search(n)
    if sol == None:
        print("No solution found")
    else:
        sol.print_board()

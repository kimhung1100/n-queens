from collections import deque
from board import Chessboard


# return a solution node or a failure
def breadth_first_search(n: int):
    """

    :rtype: board
    """
    board = Chessboard(n)

    if board.is_goal():
        return board
    frontier = deque()
    frontier.append(board)
    reached = {tuple(tuple(row) for row in board.board)}
    while frontier:
        node = frontier.popleft()  # Dequeue the first node from the frontier

        # Expand the current node and generate next board states
        next_states = node.expand(
            node.row, node.col
        )  # Assuming your Chessboard class has row and col attributes

        for next_state in next_states:
            # Check if the next state is a goal state
            if next_state.is_goal():
                return next_state  # Return the goal state

            # Convert the next state to a tuple for set comparison
            next_state_tuple = tuple(tuple(row) for row in next_state.board)

            # Check if the next state has not been reached before
            if next_state_tuple not in reached:
                reached.add(next_state_tuple)  # Add the next state to reached
                frontier.append(
                    next_state
                )  # Enqueue the next state for further exploration

            # If the BFS doesn't find a solution, return None or handle it as needed
    return None

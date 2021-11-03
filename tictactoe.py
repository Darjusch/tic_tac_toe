"""
Tic Tac Toe Player
"""

import math, copy, util
from util import Node, StackFrontier

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # The player function should take a board state as input, and return which player’s turn it is (either X or O).
    # In the initial game state, X gets the first move. Subsequently, the player alternates with each additional move.
    # Any return value is acceptable if a terminal board is provided as input (i.e., the game is already over).
    x_count = 0
    o_count = 0
    for i in board:
        for j in i:
            if X == j:
                x_count += 1
            elif O == j:
                o_count += 1
    if x_count > o_count:
        return O
    else:
        return X

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # Each action should be represented as a tuple (i, j) 
    # where i corresponds to the row of the move (0, 1, or 2)
    # and j corresponds to which cell in the row corresponds to the move (also 0, 1, or 2).
    # Possible moves are any cells on the board that do not already have an X or an O in them.
    # Any return value is acceptable if a terminal board is provided as input.
   
    possible_moves = set()
    for count_i, i in enumerate(board):
        for count_j, j in enumerate(i):
            if EMPTY == j:
                possible_moves.add((count_i, count_j))
    return possible_moves

def result(board, action: tuple):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # The result function takes a board and an action as input, and should return a new board state, 
    # without modifying the original board.
    # If action is not a valid action for the board, your program should raise an exception.
    # The returned board state should be the board that would result from taking the original input board,
    #  and letting the player whose turn it is make their move at the cell indicated by the input action.
    # Importantly, the original board should be left unmodified: 
    # since Minimax will ultimately require considering many different board states during its computation. 
    # This means that simply updating a cell in board itself is not a correct implementation of the result function. 
    # You’ll likely want to make a deep copy of the board first before making any changes.
    board_copy = copy.deepcopy(board)
    move = player(board_copy)
    board_copy[action[0]][action[1]] = move
    return board_copy

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # The winner function should accept a board as input, and return the winner of the board if there is one.
    # If the X player has won the game, your function should return X. If the O player has won the game, your function should return O.
    # One can win the game with three of their moves in a row horizontally, vertically, or diagonally.
    # You may assume that there will be at most one winner (that is, no board will ever have both players with three-in-a-row, since that would be an invalid board state).
    # If there is no winner of the game (either because the game is in progress, or because it ended in a tie), the function should return None.
    
    win_conditions = [
        [X, X ,X], 
        [O, O, O]
        ]
    diagonal_win = [
        [board[0][0], board[1][1], board[2][2]],
        [board[0][2], board[1][1], board[2][0]]
         ]
    # 3 in a row
    for item in board:
        if item in win_conditions:
            return item[0]
    # 3 in a column
    for item in zip(board[0], board[1], board[2]):
        if list(item) in win_conditions:
            return item[0]
    # 3 diagonal
    for win in diagonal_win:
        if win in win_conditions:
            return win[0]
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    winner_determined = winner(board)
    # Winner
    if winner_determined:
        return True
    # There are still moves
    for i in board:
        for j in i:
            if EMPTY == j:
                print(j)
                return False
    # Draw OR no moves
    return True

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # The utility function should accept a terminal board as input and output the utility of the board.
    # If X has won the game, the utility is 1. If O has won the game, the utility is -1. If the game has ended in a tie, the utility is 0.
    # You may assume utility will only be called on a board if terminal(board) is True.
    
    utility_winner = winner(board)
    if utility_winner == X:
        return 1
    elif utility_winner == O:
        return -1
    else:
        return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # The minimax function should take a board as input, and return the optimal move for the player to move on that board.
    # The move returned should be the optimal action (i, j) that is one of the allowable actions on the board. If multiple moves are equally optimal, any of those moves is acceptable.
    # If the board is a terminal board, the minimax function should return None.
    
    # Store the actions as nodes in a Stack
    # DFS
    # Go one "branch of the tree" down and check if the game is over or winning
    # till the end
    # If it is winning or over check if that is the best result already 
    # If we check for player X we want X to win and can stop here
    # Same for player O
    # If that is not the case we need to somehow save it so we can later on check if that was move better than other 
    # For example draw is worse then winning but still better than losing
    # Maybe for now we can drop that saving and add it later even though we should not be losing when we play perfect
    # If the games is not over
    # Copy the board again and create new moves with the result function
    # Save that in the Stack and continue.
    stack = StackFrontier()
    current_player = player(board)
    possible_actions = actions(board)
    node = Node(state=board, parent=None, action=list(possible_actions))
    stack.add(node)
    for current_action in possible_actions:
        board_after_move = result(board, current_action)
        actions_after_move = actions(board_after_move)
        node = Node(state=board_after_move, parent=board, action=list(actions_after_move))
        stack.add(node)    
    while len(stack.frontier) > 0:
        for node in stack.frontier:
            for action in node.action:
                board_after_move = result(board, action)
                # Check for win
                if terminal(board_after_move):
                    #check if winner
                    if winner(board_after_move):
                        print("WINNER")
                        # Return the optimal move
                        return "WINNER"
                    else:
                        # Return the optimal move
                        return "DRAW"
                actions_after_move = actions(board_after_move)
                if len(stack.frontier) == 0:
                    break
                removed_node = stack.remove()
                new_node = Node(state=board_after_move, parent=removed_node.state, action=list(actions_after_move))
                stack.add(new_node)
                print("Node removed")
        print("Again")

        



board = initial_state()
# player(board)
# w = winner([[X, EMPTY, O],
#             [O, X, EMPTY],
#             [O, EMPTY, X]])
# print(w)
m = minimax([[X, O, EMPTY],
             [O, EMPTY, X],
             [O, X, X]])
print(m)
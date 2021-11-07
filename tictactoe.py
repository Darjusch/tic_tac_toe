"""
Tic Tac Toe Player
"""

import copy
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

	possible_moves = []
	for count_i, i in enumerate(board):
		for count_j, j in enumerate(i):
			if EMPTY == j:
				possible_moves.append((count_i, count_j))
	return possible_moves

def result(board, action: tuple):
	"""
	Returns the board that results from making move (i, j) on the board.
	"""
	board_copy = copy.deepcopy(board)
	move = player(board_copy)
	try:
		board_copy[action[0]][action[1]] = move
		return board_copy
	except: 
		raise ValueError

def winner(board):
	"""
	Returns the winner of the game, if there is one.
	"""
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
				return False
	# Draw OR no moves
	return True

def utility(board):
	"""
	Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
	"""  
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


	# Initializing
	stack = StackFrontier()
	node = Node(
		state=board,
		parent=None, 
		action=None,
		score=None)
	stack.add(node)

	current_player = player(board)
	game_not_over = True
	while game_not_over:
		for node in stack.frontier:
				# create new possible actions
				possible_actions = actions(node.state)
				if not possible_actions:
					game_not_over = False
				for action in possible_actions:
					# copy and get board after action
					board = result(node.state, action)
					score = None
					# check if game is over
					if terminal(board):
						# return score of move
						score = utility(board)
					new_node = Node(
						state=board, 
						parent=node,
						action=action, 
						score=score
						)
					stack.add(new_node)
					if score:
						break

	# then i want to see which of them has the highest score
	# this we can check by there children when one of them has -1 its over
	# and then we pick the highest and we are done

	terminal_nodes = list(filter(lambda x: x.score , stack.frontier))
	highest_node = None
	higher = True
	list_of_root_nodes = []
	for y in terminal_nodes:
		try:
			print(y.score)
			print(y.state)
			print(y.action)
		except:
			print("root")
		while higher:
			try:
				# not working because not all notes have scores
				# so we have to filter first by the ones that have scores
				# and only loop through them and then assign the parent
				y.parent.score = y.score
				highest_node = y.parent
				print(highest_node)
				y.parent = highest_node.parent
			except:
				higher = False
		list_of_root_nodes.append(highest_node)
		# return x.action
	print(list_of_root_nodes)

	# print(nodes_of_current_player)
	print("Okay")



b = initial_state()
board = [[O, X, EMPTY],
		[EMPTY, EMPTY, X],
		[O, EMPTY, EMPTY]]
m = minimax(board)
print(m)

### Pytest doesn't work right now so improvising

# def test_correct_player_X():
#     board = initial_state()
#     if player(board) == X:
#         return True
#     else:
#         return False
# print(f"test_correct_player_X: {test_correct_player_X()}")

# def test_correct_player_O():
#     board = [[EMPTY, X, EMPTY],
#             [EMPTY, EMPTY, EMPTY],
#             [EMPTY, EMPTY, EMPTY]]
#     if player(board) == O:
#         return True
#     else:
#         return False
# print(f"test_correct_player_O: {test_correct_player_O()}")

# def test_possible_actions():
#     board = [[EMPTY, X, EMPTY],
#             [X, O, X],
#             [O, O, X]]
#     possible_moves = [(0, 0), (0, 2)]
#     if actions(board) == possible_moves:
#         return True
#     else:
#         return False
# print(f"test_possible_actions: {test_possible_actions()}")

# def test_other_possible_actions():
#     board = [[EMPTY, X, EMPTY],
#             [X, EMPTY, X],
#             [O, O, EMPTY]]
#     possible_moves = [(0, 0), (0, 2), (1, 1), (2, 2)]
#     if actions(board) == possible_moves:
#         return True
#     else:
#         return False
# print(f"test_other_possible_actions: {test_other_possible_actions()}")

# def test_result_after_move():
#     board = initial_state()
#     if result(board, (0, 0)) == [
#         [X, EMPTY, EMPTY],
#         [EMPTY, EMPTY, EMPTY],
#         [EMPTY, EMPTY, EMPTY]]:
#         return True
#     else:
#         False
# print(f"test_result_after_move: {test_result_after_move()}")


# def test_result_after_multiple_moves():
#     board = initial_state()
#     board_after_move = result(board, (0, 0))
#     board_after_move = result(board_after_move, (0, 1))
#     board_after_move = result(board_after_move, (1, 1))
#     board_after_move = result(board_after_move, (2, 1))
#     if board_after_move == [
#         [X, O, EMPTY],
#         [EMPTY, X, EMPTY],
#         [EMPTY, O, EMPTY]]:
#         return True
#     else:
#         return False
# print(f"test_result_after_multiple_moves {test_result_after_multiple_moves()}")

# def test_winner_diagonal_x():
#     board =  [
#         [X, O, EMPTY],
#         [EMPTY, X, EMPTY],
#         [EMPTY, O, X]]
#     if winner(board) == X:
#         return True
#     else:
#         return False
# print(test_winner_diagonal_x())

# def test_winner_row_o():
#     board =  [
#         [O, O, O],
#         [X, X, EMPTY],
#         [X, EMPTY, X]]
#     if winner(board) == O:
#         return True
#     else:
#         return False
# print(f"test_winner_row_o: {test_winner_row_o()}")

# def test_winner_column_x():
#     board =  [
#         [X, O, O],
#         [X, EMPTY, EMPTY],
#         [X, EMPTY, X]]
#     if winner(board) == X:
#         return True
#     else:
#         return False
# print(f"test_winner_column_x: {test_winner_column_x()}")

# def test_draw():
#     board =  [
#         [O, X, O],
#         [X, X, O],
#         [X, O, X]]
#     if winner(board) == None:
#         return True
#     else:
#         return False
# print(test_draw())

# def test_game_ongoing():
#     board = initial_state()
#     if winner(board) == None:
#         return True
#     else:
#         return False
# print(test_game_ongoing())
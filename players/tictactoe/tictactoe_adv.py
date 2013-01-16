import collections
import sys
import math

import game_state
import game_player
import tictactoe


# A less-stupid TicTacToePlayer agent.
#
# Treats X as maximizing player and O as minimizing player.
class TicTacToePlayer(game_player.GamePlayer):

	# Make a note of our name and player ID
	# see comments on GamePlayer for more details
	def __init__(self, name, game_id):
		game_player.GamePlayer.__init__(self, name, game_id)
	
	# Returns the number of 3-in-a-rows available to the OPPOSITE player of
	# the one indicated.
	#
	# i.e., if we give it X's ID, we'll get the number of 3-in-a-rows available
	# to O.
	#
	# state is a TicTacToeState, otherPlayer is a valid game ID.
	def open3(self, state, otherPlayer):
		s = 0
		if state.board_value(0) != otherPlayer \
				and state.board_value(4) != otherPlayer \
				and state.board_value(8) != otherPlayer:
			s += 1
		if state.board_value(6) != otherPlayer \
				and state.board_value(4) != otherPlayer \
				and state.board_value(2) != otherPlayer:
			s += 1
		for i in range(3):
			if state.board_value(3*i) != otherPlayer and \
					state.board_value((3*i)+1) != otherPlayer and \
					state.board_value((3*i)+2) != otherPlayer:
				s += 1
			if state.board_value(i) != otherPlayer and \
					state.board_value(i+3) != otherPlayer and \
					state.board_value(i+6) != otherPlayer:
				s += 1
		return s
	
	# A simple evaluation function for tic-tac-toe
	#
	# Returns the number of 3-in-a-rows available to player X, minus the
	# number of 3-in-a-rows available to player O.
	#
	# "state" is a TicTacToeState object
	def evaluate(self, state):
		players = state.get_players()
		f = self.open3(state, players[1]) - self.open3(state, players[0])
		return f
	
	# Does most of the terminal checks for a single step in the search
	#
	# state is a TicTacToeState
	# h is steps to the ply horizon
	# players is the list of valid player IDs
	#
	# Returns None if no termination
	# (value, move) otherwise
	def terminal_checks(self, state, h, players):
		# If first player wins, that's a positive
		if state.is_win(players[0]):
			return (sys.maxint, None)
		# If second player wins, that's a negative
		elif state.is_win(players[1]):
			return (-sys.maxint-1, None)
		
		# If there are no more expansions allowed, or if
		# we hit the horizon, evaluate
		if state.expansions_count() <= 0 or h <= 0:
			return (self.evaluate(state), None)
		
		# if no termination, return None
		return None
		
	
	# A helper function for minimax_move().  This one returns a
	# (value, move) tuple that lets us back values up the tree and still
	# return a move at the top.
	#
	# state is a TicTacToeState
	# h is an integer representing the distance to the ply horizon
	def minimax_search(self, state, h):
		# Get player IDs
		players = state.get_players()
		
		# Do most of our terminal checks
		term = self.terminal_checks(state, h, players)
		if term != None:
			return term
		
		# Get successor states
		# We should check to see if this is None, but since we just
		#  checked to see if expansion_count was <= 0, we're safe
		successors = state.successors()
		# If there are no successors and nobody's won, it's a draw
		if len(successors) == 0:
			return (0, None)
		
		# Recur on each of the successor states (note we take the state out
		# of the successor tuple with x[1] and decrease the horizon)
		values = [self.minimax_search(s.state, h-1) for s in successors]
		# We're not interested in the moves made, just the minimax values
		values = [x[0] for x in values]
		# Look for the best among the returned values
		# Max if we're player 1
		# Min if we're player 2
		if state.get_next_player() == players[0]:
			max_idx = max(enumerate(values), key=lambda x: x[1])[0]
		else:
			max_idx = min(enumerate(values), key=lambda x: x[1])[0]
		# Return the minimax value and corresponding move
		return (values[max_idx], successors[max_idx].move)
	
	
	# A helper function for alpha_beta_move().  See minimax_search().
	#
	# a,b are alpha, beta values.
	def alpha_beta_search(self, state, h, a, b):
		# Get player IDs
		players = state.get_players()
		player = state.get_next_player()
		
		# Do most of our terminal checks
		term = self.terminal_checks(state, h, players)
		if term != None:
			return term
		
		# Get successor states
		# We should check to see if this is None, but since we just
		#  checked to see if expansion_count was <= 0, we're safe
		successors = state.successors()
		# If there are no successors and nobody's won, it's a draw
		if len(successors) == 0:
			return (0, None)
		
		# We start out with a low best-value and no move
		v = -sys.maxint-1 if player == players[0] else sys.maxint
		m = None
		for s in successors:
			# Recur on the successor state
			s_val = self.alpha_beta_search(s.state, h-1, a, b)
			# If our new value is better than our best value, update the best
			#  value and the best move
			if (player == players[0] and s_val[0] > v) \
					or (player == players[1] and s_val[0] < v):
				v = s_val[0]
				m = s.move
			# If we're maxing and exceeding the min above, just return
			# Likewise if we're minning and exceeding the max above
			if (player == players[0] and v >= b) \
					or (player == players[1] and v <= a):
				return (v, m)
			# Update a,b for the next successor
			a = a if player == players[1] else max(a,v)
			b = b if player == players[0] else min(b,v)
		# return the best value, move we found
		return (v,m)
		
	
	# Get a move for the indicated state, using a minimax search.
	#
	# "state" is still a TicTacToeState object
	def minimax_move(self, state, visited):
		# Adjust our ply horizon to the expansion count,
		# based on a maximum branching factor of 8.
		# NB: This may not be the best way to do this.
		exp = state.expansions_count()
		h = int(math.floor(float(exp) ** (1.0 / 8.0)))
		print h
		return self.minimax_search(state,h)[1]
	
	# Get a move for the indicated state, using an alpha-beta search.
	#
	# state is a TicTacToeState
	def alpha_beta_move(self, state, visited):
		# Adjust our ply horizon to the expansion count,
		# based on an average branching factor of 4.
		exp = state.expansions_count()
		h = int(math.floor(float(exp) ** (1.0 / 4.0)))
		return self.alpha_beta_search(state, h, -sys.maxint-1, sys.maxint)[1]
	
	# Just call alpha-beta
	def tournament_move(self, state, visited):
		return self.alpha_beta_move(state, visited)

def make_player(name, gameID):
	return TicTacToePlayer(name, gameID)

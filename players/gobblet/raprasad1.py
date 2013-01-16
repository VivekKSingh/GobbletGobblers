import collections
import sys
import math

import game_state
import game_player
import gobblet


class GobbletPlayer(game_player.GamePlayer):
	def __init__(self, name, gameID):
		game_player.GamePlayer.__init__(self, name, gameID)
		
	# EXAMPLE: Loads a file from the same directory this module is stored in
	#  and returns its contents.  Pattern any file operations you do in your
	#  player on this model.
	#
	# NB: Make a note of the working directory before you cd to the module
	#  directory, and restore it afterward!  The rest of the program may break
	#  otherwise.
	def load_file(self, fname):
		wd = os.getcwd()
		os.chdir("players/gobblet")
		fin = open(fname)
		contents = fin.read()
		fin.close()
		os.chdir(wd)
		return contents
	
	def open3(self, state, otherPlayer):
		s=0
		if state.board_value([0,0]) != otherPlayer\
			and state.board_value([1,1]) != otherPlayer \
			and state.board_value([2,2]) != otherPlayer:
			s += 1
		if state.board_value([0,2]) != otherPlayer \
			and state.board_value([1,1]) != otherPlayer \
			and state.board_value([2,0]) != otherPlayer:
			s += 1
		for i in range(2):
			if state.board_value([i,0]) != otherPlayer and \
					state.board_value([(1),i]) != otherPlayer and \
					state.board_value([(2),i]) != otherPlayer:
				s += 1
			if state.board_value([i,2]) != otherPlayer and \
					state.board_value([i,1]) != otherPlayer and \
					state.board_value([i,0]) != otherPlayer:
				s += 1
		return s

	def evaluate(self, state):
		
		players=state.get_players()
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


	def alpha_beta_move(self, state, visited):
		pass
		
	def tournament_move(self, state, visited):
		pass
		
		
def make_player(name, gameID):
	return GobbletPlayer(name, gameID)

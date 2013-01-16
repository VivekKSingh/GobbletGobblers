import game_state
import game_player
import gobblet
import math
import sys


# An advanced GobbletPlayer agent.
class GobbletPlayer(game_player.GamePlayer):

	# Make a note of our name and player ID
	# see comments on GamePlayer for more details
	def __init__(self, name, game_id):
		game_player.GamePlayer.__init__(self, name, game_id)
		self.rejectedList = []

	# This function checks for Three in a rows for the player 
	def open3(self, state, otherPlayer):
		s = 0
		if self.ifOpen(state,[0,0]) and self.ifOpen(state,[1,1]) and self.ifOpen(state,[2,2]):
			s += 1
		if self.ifOpen(state,[2,0]) and self.ifOpen(state,[1,1]) and self.ifOpen(state,[0,2]):
			s += 1
		for i in range(2):
			if self.ifOpen(state,[0,i]) and self.ifOpen(state,[1,i]) and self.ifOpen(state,[2,i]):
				s += 1
			if self.ifOpen(state,[i,2]) and self.ifOpen(state,[i,1]) and self.ifOpen(state,[i,0]):
				s += 1
		return s
	# This function calculates the state of a position on the board whether it is empty, has a small piece or a medium piece.
	#It basically checks if the current player is at advantage based on the piece on the position and the kind of pieces in the players kitty
	def ifOpen(self,state, location):
		if (state.board_value(location) is None):
			return True
		if (state.board_value(location).size == 'S') and ((state.pieces_available(self, 'L') > 0) or 
														(state.pieces_available(self, 'M') > 0)):
			return True
		if ((state.board_value(location).size == 'M') and (state.pieces_available(self, 'L') > 0)):
			return True
		return False

        # This function helps in rejecting the mirror and rotating states to build a better horizon
	def filterSuccessors(self, successors):		
		mirrorObject = None
		rotations = []
		removedSuccessors = []
		print "Previous length :: " , len(successors)
		for successor in successors:
			mirrorObject = str(gobblet.mirror(successor.state))			
			if (mirrorObject in self.rejectedList) or (str(successor) in self.rejectedList):
				removedSuccessors.append(successor)
				successors.remove(successor)
			else:
				self.rejectedList.append(mirrorObject)
				rotations = gobblet.rotations(successor.state)
				self.rejectedList.append(str(rotated) for rotated in rotations)
		print removedSuccessors				 
		return successors
	
	# This agent doesn't evaluate states, so just return 0
	#
	# "state" is a GobbletState object
	def evaluate(self, state):
		players = state.get_players()
		f = self.open3(state, players[1]) - self.open3(state, players[0])
		return f
	
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
		successors = self.filterSuccessors(state.successors())
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
		successors = self.filterSuccessors(state.successors())
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
	
	# Don't perform any game-tree expansions, just pick the first move
	# that's available in the list of successors.
	#
	# "state" is still a TicTacToeState object
	def minimax_move(self, state, visited):
		# "successors" is a list of GameSuccessor objects
		exp = state.expansions_count()
		h = int(math.floor(float(exp) ** (1.0 / 8.0)))
		print h
		return self.minimax_search(state,h)[1]
	
	# Function calculating the next move based on alpha beta pruning
	def alpha_beta_move(self, state, visited):
		# Adjust our ply horizon to the expansion count,
		# based on an average branching factor of 4.
		exp = state.expansions_count()
		h = int(math.floor(float(exp) ** (1.0 / 4.0)))
		return self.alpha_beta_search(state, h, -sys.maxint-1, sys.maxint)[1]
	
	# Function for competing in the tournament using the alpha beta search
	def tournament_move(self, state, visited):
		return self.alpha_beta_move(state, visited)


def make_player(name, gameID):
	return GobbletPlayer(name, gameID)

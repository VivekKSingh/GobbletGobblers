import game_state

PLAYERS = ['B', 'O']
SIZES = ['S', 'M', 'L']
THREES = [[(0,0), (1,1), (2,2)], [(2,0), (1,1), (0,2)], [(0,0), (1,0), (2,0)],
			[(0,1), (1,1), (2,1)], [(0,2), (1,2), (2,2)], [(0,0), (0,1), (0,2)],
			[(1,0), (1,1), (1,2)], [(2,0), (2,1), (2,2)]]
DIAGONAL_PLACES = THREES[:2]

class GobbletPiece(object):
	"""A class representing a single piece in the game.  Has
	data members "player" and "size" corresponding to values used
	by the GobbletState class."""
	def __init__(self, player, size):
		self.player = player
		self.size = size
	
	def __str__(self):
		return PLAYERS[self.player] + SIZES[self.size]
	
	def repeated_rep(self):
		"""A representation suitable for hashing."""
		return (self.player, self.size)
	
	def copy_into(self, other):
		"""Copies this piece into another GobbletPiece object."""
		other.player = self.player
		other.size = self.size
	
	def make_copy(self):
		"""Returns a new copy of this GobbletPiece object."""
		other = GobbletPiece(self.player, self.size)
		return other

class GobbletMoveDetail(object):
	"""A class representing details about a move in a Gobblet
	Gobblers game.  Contains data members "source" (2-tuple giving
	location we're picking up from, if any, else None), "target"
	(2-tuple giving location we're landing on), and "piece" (a
	GobbletPiece object representing the piece we're using).
	
	If source is not None, the topmost piece on that location on the
	board should agree with the "piece" member of this object."""
	def __init__(self, source, target, piece):
		self.source = source
		self.target = target
		self.piece = piece

class GobbletMove(game_state.GameMove):
	"""A class representing a move in a Gobblt Gobblers game.  Subclass
	of the GameMove state."""
	def __init__(self, move, forfeit=False):
		""" "move" is a GobbletMoveDetail object, forfeit a boolean
		indicating whether the player is forfeiting the game."""
		self.move = move
		self.forfeit = forfeit
		
	def __str__(self):
		if self.move.source:
			return "Player %.1s moves %.1s from %s to %s" % \
				(PLAYERS[self.move.piece.player], SIZES[self.move.piece.size], \
					self.move.source, self.move.target)
		return "Player %.1s moves %.1s to %s" % \
			(PLAYERS[self.move.piece.player], SIZES[self.move.piece.size], \
				self.move.target)
	
	def get_player(self):
		"""Returns the player who's making this move, as represented
		in the GobbletState class."""
		return self.move.piece.player
	
	def get_move(self):
		"""Returns the GobbletMoveDetail object that details this move.
		(Weird naming is owing to the design of the GameMove superclass.)"""
		return self.move
	
	def is_forfeit(self):
		"""Returns True if move is a forfeit."""
		return self.forfeit

class GobbletState(game_state.GameState):
	"""Defines a complete game state in the Gobblet Gobblers game,
	as well as the logic of moving from that state.  Subclass of the 
	GameState class."""
	def __init__(self):
		game_state.GameState.__init__(self)
		self.clear()
	
	def __str__(self):
		return "%.2s | %.2s | %.2s\n" \
				"------------\n" \
				"%.2s | %.2s | %.2s\n" \
				"------------\n" \
				"%.2s | %.2s | %.2s" % \
				tuple([str(self.board[i][j][-1]) if self.board[i][j] \
							else '  ' \
							for i in range(3)
							for j in range(3)])
	
	def clear(self):
		"""Resets the game to opening state."""
		self.player = 0
		self.isDraw = False
		self.board = [[[] for j in range(3)] for i in range(3)]
		self.pieces = [[2 for j in range(3)] for i in range(2)]
	
	def repeats(self):
		"""Simply returns True, as a Gobblet Gobblers game
		can cycle."""
		return True
	
	def repeated_rep(self):
		"""Returns a hashable representation of the state."""
		return tuple([tuple([piece.repeated_rep() for piece in place]) \
						for row in self.board for place in row] \
					#+ [tuple(player) for player in self.pieces] \
					+ [self.player])
	
	def copy_into(self, other):
		"""Copies this state's values onto another GobbletState object."""
		game_state.GameState.copy_into(self, other)
		other.player = self.player
		other.pieces = [[v for v in player] for player in self.pieces]
		other.board = [[[piece.make_copy() for piece in place] for place in row] \
						for row in self.board]
	
	def make_copy(self):
		"""Returns a fresh copy of this state."""
		other = GobbletState()
		self.copy_into(other)
		return other
	
	def is_win(self, player):
		"""Returns True if this state is a win for the indicated player, False else.
		
		"player" is a valid player ID returned by get_players()"""
		for three in THREES:
			win = True
			for pos in three:
				p1, p2 = pos
				if not self.board[p1][p2] or self.board[p1][p2][-1].player != player:
					win = False
					break
			if win:
				return True
		return False
	
	def get_players(self):
		"""Returns a list of the representations used for the players,
		suitable for passing into any function that requires a player ID."""
		return [0,1]
	
	def get_next_player(self):
		"""Returns the internal representation of the current player in this state."""
		return self.player
	
	def board_stack(self, location):
		"""Returns the complete stack of game pieces on a given location.
		
		The location is a 2-tuple (x,y)"""
		t1,t2 = location
		return [piece.make_copy() for piece in self.board[t1][t2]]
		
	def board_value(self, location):
		"""Returns the last (top-most) game piece on a given location, or None
		if the location is empty
		
		The location is a 2-tuple (x,y)"""
		t1,t2 = location
		if not self.board[t1][t2]:
			return None
		return self.board[t1][t2][-1].make_copy()
	
	def pieces_available(self, player, size):
		"""Returns the number of pieces available for the given size (0-2) and
		the given player.
		
		Player is a valid player ID returned by get_players()"""
		return self.pieces[player][size]
	
	def get_player_state(self, player):
		"""Returns a player's view of the state (just a copy of this object,
		as Gobblet games are fully observable).  Called by GameController."""
		return self.make_copy()
	
	def is_valid_move(self, move):
		"""Returns True if the move (a GobbletMove object) is legal in this state."""
		if move.get_player() != self.player:
			return False
		detail = move.get_move()
		t1,t2 = detail.target
		size = detail.piece.size
		if detail.source:
			s1,s2 = detail.source
			if detail.target == detail.source:
				return False
		if not detail.source and self.pieces[self.player][size] <= 0:
			return False
		if detail.source and not self.board[s1][s2]:
			return False
		if detail.source and \
				(self.board[s1][s2][-1].player != self.player \
					or self.board[s1][s2][-1].size != size):
			return False
		if self.board[t1][t2] and self.board[t1][t2][-1].size >= size:
			return False
		return True
	
	def move(self, move, clearRepeats=False):
		"""Destructively modifies this state by making the indicated move
		(a GobbletMove object).  Returns a 2-tuple (newplayer, clear) with
		clear being true if clearRepeats argument is True and it is safe
		for the GameController to forget visited states up to this point."""
		if not self.is_valid_move(move):
			return (None, False)
		detail = move.get_move()
		t1,t2 = detail.target
		size = detail.piece.size
		if detail.source:
			s1,s2 = detail.source
			self.board[s1][s2] = self.board[s1][s2][:-1]
		else:
			self.pieces[self.player][size] -= 1
		self.board[t1][t2].append(detail.piece.make_copy())
		self.player = (self.player + 1) % 2
		return self.player, (detail.source is None)
		
	def handle_cycle(self):
		"""Handles a cycle in the game (by declaring it a draw, in Gobblet
		Gobblers).  Called by GameController when a cycle is detected."""
		self.isDraw = True
		
	def successor_moves(self):
		"""Returns a list of GobbletMoves which are legal moves to
		make in this state."""
		if self.isDraw:
			return []
		successors = game_state.GameState.successor_moves(self)
		if successors is None:
			return None
		for size in range(3):
			if self.pieces[self.player][size] <= 0:
				continue
			for t1 in range(3):
				for t2 in range(3):
					if not self.board[t1][t2] or self.board[t1][t2][-1].size <= size:
						move = GobbletMove(GobbletMoveDetail(None, 
														(t1,t2), 
														GobbletPiece(self.player, size)))
						if self.is_valid_move(move):
							successors.append(move)
		for s1 in range(3):
			for s2 in range(3):
				if self.board[s1][s2] and self.board[s1][s2][-1].player == self.player:
					size = self.board[s1][s2][-1].size
					for t1 in range(3):
						for t2 in range(3):
							if s1 == t1 and s2 == t2:
								continue
							if not self.board[t1][t2] or self.board[t1][t2][-1].size <= size:
								move = GobbletMove(GobbletMoveDetail((s1,s2), 
														(t1,t2), 
														GobbletPiece(self.player, size)))
								if self.is_valid_move(move):
									successors.append(move)
		return successors

def mirror(state):
	"""Returns the mirror-image of the provided state."""
	r = state.make_copy()
	for i in range(3):
		t = r.board[i][0]
		r.board[i][0] = r.board[i][2]
		r.board[i][2] = t
	return r

def rotate(state):
	"""Destructively rotates the provided state."""
	r = state.make_copy()
	newboard = [[[] for j in range(3)] for i in range(3)]
	newboard[0][0] = r.board[2][0]
	newboard[0][1] = r.board[1][0]
	newboard[0][2] = r.board[0][0]
	newboard[1][0] = r.board[2][1]
	newboard[1][1] = r.board[1][1]
	newboard[1][2] = r.board[0][1]
	newboard[2][0] = r.board[2][2]
	newboard[2][1] = r.board[1][2]
	newboard[2][2] = r.board[0][2]
	r.board = newboard
	return r

def rotations(state):
	"""Returns the three rotated versions of the provided state."""
	rots = [rotate(state)]
	for i in range(2):
		rots.append(rotate(rots[-1]))
	return rots
	
def make_state():
	return GobbletState()
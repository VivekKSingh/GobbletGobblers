import game_state
import game_player

class TicTacToeMove(game_state.GameMove):
	"""Subclass of GameMove representing one move by one player in a
	tic-tac-toe class"""
	def __init__(self, player, move, forfeit=False):
		"""player: a TicTacToePlayer object representing the player making the
		 move.
		move: a number representing the square being moved to.
		forfeit: a boolean which is True only if the player wishes to give up."""
		self.move = move
		self.player = player
		self.forfeit = forfeit
	
	def __str__(self):
		"""Returns an informal string representation for printing"""
		# Tell us which player moves where
		return "Player %.1s moves to square %s" \
			% (TicTacToeState.val_to_char(self.player), \
				str(self.move+1) if self.move != None else "(None)")
	
	def get_player(self):
		"""Returns the TicTacToePlayer object who's moving"""
		return self.player
	
	def get_move(self):
		"""Returns the number indicating the square being moved to"""
		return self.move
	
	def is_forfeit(self):
		"""Returns True if the player gives up,
		False else"""
		return self.forfeit

class TicTacToeState(game_state.GameState):
	"""Subclass of GameState representing a state in
	 a game of tic-tac-toe"""
	 
	X = 1
	O = 2
	EMPTY = -1
	
	@classmethod
	def val_to_char(cls, x):
		"""A class method that gives you a character value for a player ID
		(useful for building a string representation of a player or a board)"""
		if x == TicTacToeState.X:
			return 'X'
		elif x == TicTacToeState.O:
			return 'O'
		else:
			return ' '
	
	def __init__(self):
		"""Player X goes first"""
		self.clear()
	
	# Returns an informal string representation of the board
	# useful for printing the board before every move
	def __str__(self):
		s = "%.1s | %.1s | %.1s\n"\
				"---------\n"\
				 "%.1s | %.1s | %.1s\n"\
				 "---------\n"\
				 "%.1s | %.1s | %.1s\n" % \
				 tuple(map(TicTacToeState.val_to_char, self.board))
		return s
		
	def clear(self):
		"""Clears the board and sets X as the next player"""
		self.board = [TicTacToeState.EMPTY for x in range(9)]
		self.player = TicTacToeState.X;
	
	def board_positions(self):
		"""returns a list of valid positions on the board"""
		return range(9)
	
	def board_value(self, pos):
		"""returns the value at the indicated board position
		
		"pos" should be one of the values returned by board_positions()
		(i.e., 0-8)"""
		return self.board[pos]
	
	def copy_into(self, other):
		"""copies relevant information into another state object
		
		"other" is the TicTacToeState object to be copied into
		Warning: destroys data in "other" """
		game_state.GameState.copy_into(self, other)
		other.player = self.player
		other.board = [x for x in self.board]
	
	def make_copy(self):
		"""Returns a TicTacToeState object, functionally identical to this one,
		which may be modified without modifying this state object's internals"""
		r = TicTacToeState()
		self.copy_into(r)
		return r
	
	def get_players(self):
		"""Returns a list of valid player IDs"""
		return [TicTacToeState.X, TicTacToeState.O]
	
	def get_next_player(self):
		"""Returns the player who should play next"""
		return self.player
	
	def get_player_state(self, player):
		"""Returns a state representation specific to the indicated player
		For tic-tac-toe that's just a copy of this state obtained with
		make_copy().
		
		"player" is a valid player ID returned by get_players()
		(i.e., 1 or 2)"""
		return self.make_copy()
	
	def is_win(self, player):
		"""Returns True if this state represents a win for the indicated player
		False else
		
		"player" is a valid player ID returned by get_players()"""
		if self.board[0] == self.board[4] == self.board[8] == player:
			return True
		if self.board[6] == self.board[4] == self.board[2] == player:
			return True
		for i in range(3):
			if self.board[3*i] == self.board[(3*i)+1] == self.board[(3*i)+2] \
					== player:
				return True
			if self.board[i] == self.board[i+3] == self.board[i+6] == player:
				return True
		return False
	
	def is_valid_move(self, move):
		"""Returns true if the indicated move is valid on this state
		
		"move" is a TicTacToeMove object"""
		return move.get_player() == self.player and \
					self.board[move.get_move()] == TicTacToeState.EMPTY
	
	def move(self, move, clearRepeats=False):
		"""Destructively modifies this state object by performing the indicated
		move (if valid).
		
		Returns the player ID of the player who should play next, or None
		if the move was invalid.
		
		"move" is a TicTacToeMove object"""
		if not self.is_valid_move(move):
			return (None, False)
		self.board[move.get_move()] = move.get_player()
		self.player = (self.player % 2) + 1
		return (self.player, False)
	
	def successor_moves(self):
		"""Returns a list of the valid moves which may be performed on this state,
		or None if the game controller refuses to allow any more expansions
		this turn.
		
		If the return value is an empty list, there are no valid moves to be
		made on this state.
		
		Each move in the list is a TicTacToeMove object."""
		moves = game_state.GameState.successor_moves(self)
		if(moves == None):
			return None
		for i in range(9):
			move = TicTacToeMove(self.player, i)
			if(self.is_valid_move(move)):
				moves.append(move)
		return moves

def make_state():
	return TicTacToeState()
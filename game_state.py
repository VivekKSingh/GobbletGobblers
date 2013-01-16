import copy
import weakref

class GameSuccessor(object):
	"""A class to represent a successor -- just contains members
	"move" and "state".
	Not intended to be subclassed."""
	def __init__(self, move, state):
		self.move = move
		self.state = state

class GameMove(object):
	"""A class to represent one move to be made in the game.
	Has to represent both what the move is and and the player making it.
	Allows the player to give up by setting is_forfeit() True.
	
	Intended to be subclassed for a specific game type.
	Override all methods in subclass."""
	def __str__(self):
		"""Returns an informal string representation (used to print out the move
		 during gameplay)"""
		return "Base GameMove object"
		
	def get_player(self):
		"""Returns the player whose move this is.
		 return val is an object whose type is a game-specific subclass of
		 GamePlayer."""
		return None
		
	def get_move(self):
		"""Returns the move made.
		 return val is an object whose type is a game-specific subclass of
		 GameMove"""
		return None
		
	def is_forfeit(self):
		"""Returns a boolean indicating whether this move is a forfeiture
		 (useful for human players who want to quit)"""
		return False

class GameState(object):
	"""A class to represent a state in the game.
	
	Intended to be subclassed for a specific game type.
	Override the following methods in a subclass:
	  __str__(),
	  repeats(),
	  repeated_rep(),
	  copy_into(),
	  make_copy(),
	  clear(),
	  is_win(),
	  get_players(),
	  get_next_player(),
	  get_player_state(),
	  is_valid_move(),
	  move(),
	  handle_cycle(),
	  successor_moves()"""
	def __init__(self):
		self.moveCounter = None
	
	def set_counter(self, moveCounter):
		"""Sets a move counter to be shared between this state and its successors.
		This allows us to check how many times per turn the player is allowed to
		ask about successor states."""
		self.moveCounter = moveCounter
		
	def __str__(self):
		"""Override in subclass
		
		Must return a printable representation of the game in the state
		represented by this object, so we can show the game state as it progresses"""
		return "Base game state object"
		
	def repeats(self):
		"""Override in subclass ONLY if game has cycles
		
		Returns True if the game can cycle infinitely, False else"""
		return False
	
	def repeated_rep(self):
		"""Override in subclass ONLY if game has cycles.
		
		Returns a representation of the state which is suitable for hashing"""
		pass
	
	def copy_into(self, other):
		"""Override in subclass
		Be sure to call this super method to get the move counter!
		
		"other" is another GameState object
		
		Intent is to populate a copy the player can perform game moves on
		without modifying the original game state held by the controller."""
		other.moveCounter = self.moveCounter
	
	def make_copy(self):
		"""Override in subclass
		
		Creates a copy for player experiments without modifying original
		game state
		
		See copy_into() above"""
		pass
	
	def clear(self):
		"""Override in subclass
		
		Reset to a starting game"""
		pass
	
	def is_win(self, player):
		"""Override in subclass.
		
		returns True if indicated player has won, False else
		
		"player" parameter is a player's game ID"""
		pass
	
	def get_players(self):
		"""Override in subclass.
			
		Returns a list of legal player game IDs in nominal order of play."""
		pass
		
	def get_next_player(self):
		"""Override in subclass
		
		Returns the game ID of the player who should move next"""
		pass
	
	def get_player_state(self, player):
		"""Override in subclass.
		
		Returns a representation of the game state particular to a player,
		which may be a partial or probabilistic picture of the entire game state.
		
		player is an object whose type is a game-specific subclass of GamePlayer"""
		return None
	
	def is_valid_move(self, move):
		"""Override in subclass.
		
		Returns True if the indicated move is valid on the current state,
		False otherwise.
		
		move is an object whose type is a game-specific subclass of GameMove
		return False"""
		pass
		
	def move(self, move, clearRepeats=False):
		"""Override in subclass.
		
		Make the indicated move and modify the state accordingly.
		Should modify self, return a 2-tuple (nextplayer, clear) -- clear should
		be True if clearRepeats is True, the game has cycles, and it is safe
		for the GameController to forget visited states up to this point.
		
		Returns (None, False) if the move is invalid.
		
		move is an object whose type is a game-specific subclass of GameMove"""
		pass
	
	def handle_cycle(self):
		"""Override in subclass ONLY if the game can cycle.
		
		Responsible for handling a cycle situation (e.g., by declaring a draw,
		 awarding pieces to players, etc.)"""
		pass
	
	def expansions_count(self):
		"""Returns number of expansions the controller will allow for the remainder
		of the turn"""
		if not self.moveCounter:
			return None
		else:
			return self.moveCounter.count
		
	def successor_moves(self):
		"""Override in subclass.
		
		Be sure to call this super function and return None if it returns None!
		Override should return empty list if no moves are possible.
		
		Generates a list of valid moves to make on the current state.
		Each move is an object whose type is a game-specific subclass of GameMove.
		
		Returns None if the GameController indicates that we are not allowed to
		generate any more successors"""
		if self.moveCounter == None:
			return []
		elif self.moveCounter.count > 0:
			self.moveCounter.count -= 1
			return []
		else:
			return None
	
	def move_copy(self, move):
		"""Like move(), above, but returns a copy of the game state after the
		indicated move instead of modifying the current state (useful for looking
		ahead in a minimax tree without destroying the original state).
		
		Returns None if the move is invalid.
		
		move is an object whose type is a game-specific subclass of GameMove"""
		if not self.is_valid_move(move):
			return None
		r = self.make_copy()
		player, clear = r.move(move)
		return (player, r)
	
	def successors(self):
		"""Returns a valid list of GameSuccessor objects.  Each one contains
		a valid move on the current state (obtained with successor_moves() above) and
		a GameState resulting from applying that move (obtained with move_copy()
		above).
		
		Returns None if the GameController indicates that we are not allowed to
		generate any more successors, empty list if no moves are possible"""
		moves = self.successor_moves()
		if moves == None:
			return None
		s = [self.move_copy(m) for m in moves]
		s = [GameSuccessor(moves[i], s[i][1]) for i in range(len(moves))]
		#s = zip([x[0] for x in s], [x[1] for x in s], moves)
		return s
	
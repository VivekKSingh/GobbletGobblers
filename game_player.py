
class GamePlayer(object):
	"""Represents/contains the logic for an individual player in a game
	
	Intended to be subclassed for a particular game type
	Override the following methods in a subclass:
	  evaluate()
	  minimax_move()
	  alpha_beta_move()
	  tournament_move()"""
	  
	def __init__(self, name, game_id):
		""""name" is a string identifier for the player (the default game framework
		value is the module name)
		
		"game_id" is a game-type-specific identifier for the player (e.g., 1 for
		player 1)"""
		self.name = name
		self.game_id = game_id
		
	def get_name(self):
		return self.name
	
	def get_game_id(self):
		return self.game_id
	
	def evaluate(self, state):
		"""Override in subclass!
		
		Gives an evaluation value for a game state.
		
		"state" is an object whose type is a game-specific subclass of GameState"""
		pass
	
	def minimax_move(self, state, visited):
		"""Override in subclass!
		
		Returns a move object of a game-type-specific GameMove subclass
		representing the move the player will make from the indicated
		state.
		
		"state" is an object whose type is a game-specific subclass of GameState.
		"visited" is a set of states' repeated representations, giving the states
		 the controller is tracking as visited so far in the game."""
		pass
	
	def alpha_beta_move(self, state, visited):
		"""Override in subclass!
		
		Does the same thing as minimax_move() but with alpha-beta pruning."""
		pass
		
	def tournament_move(self, state, visited):
		"""Override in subclass!
		
		Calls minimax_move() or alpha_beta_move().  Or, performs special behavior 
		if you like."""
		pass
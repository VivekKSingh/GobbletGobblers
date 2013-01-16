import game_state
import game_player
import tictactoe


# A TicTacToePlayer class for asking a human player for input.
class TicTacToePlayer(game_player.GamePlayer):

	# Make a note of our name and player ID (see GamePlayer for comments)
	def __init__(self, name, game_id):
		game_player.GamePlayer.__init__(self, name, game_id)
	
	# Since we're asking the human, we don't need to evaluate states.
	#
	# "state" is a TicTacToeState object
	def evaluate(self, state):
		return 0
	
	# Don't do game-tree expansion, just ask the human.
	#
	# "state" is a TicTacToeState object
	def minimax_move(self, state, visited):
		# see what the valid moves are so we can check the human's answer
		successors = state.successor_moves()
		successors = [x.get_move() for x in successors]
		
		# Keep looping until the human gives us valid input
		while True:
			# Ask
			s = raw_input("What square would you like to move to (1-9, q to quit)? ")
			# Human wants to quit
			if s == 'q':
				# so return a forfeit move
				return tictactoe.TicTacToeMove(self.game_id, None, True)
			
			# Human may not have input an integer
			try:
				s = int(s)
			except:
				print "Please input an integer 1-9, or q to quit "
				continue
			
			# Human may not have input a value on the board
			if s >= 1 and s <= 9:
				s -= 1
			else:
				print "Please input an integer 1-9, or q to quit "
				continue
			
			# Human may not have input a valid move
			if s not in successors:
				print "That is not a valid move.  Please choose an unoccupied "\
					"square."
				continue
			
			# Return the valid move
			return tictactoe.TicTacToeMove(self.game_id, s)
	
	# We're just asking the human, so call minimax
	def alpha_beta_move(self, state, visited):
		return self.minimax_move(state, visited)
	
	# We're just asking the human, so call minimax
	def tournament_move(self, state, visited):
		return self.minimax_move(state, visited)
		
		
def make_player(name, gameID):
	return TicTacToePlayer(name, gameID)
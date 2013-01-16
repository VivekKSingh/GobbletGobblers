import game_state
import game_player
import gobblet


# A human-interactive GobbletPlayer agent.
class GobbletPlayer(game_player.GamePlayer):

	# Make a note of our name and player ID
	# see comments on GamePlayer for more details
	def __init__(self, name, game_id):
		game_player.GamePlayer.__init__(self, name, game_id)
	
	# This agent doesn't evaluate states, so just return 0
	#
	# "state" is a GobbletState object
	def evaluate(self, state):
		return 0
	
	def minimax_move(self, state, visited):
		# see what the valid moves are so we can check the human's answer
		successors = state.successor_moves()
		successors = [x.get_move() for x in successors]
		size = None
		
		# Keep looping until the human gives us valid input
		while True:
			src = raw_input("What square would you like to pick up from (1-9, q to quit, "\
							"0 to place a new piece)? ")
			if src == 'q':
				# Quit by forfeiting
				return gobblet.GobbletMove(None, True)
			try:
				src = int(src)
			except:
				print "Please input an integer 0-9, or q to quit. "
				continue
			
			if src >= 0 and src <= 9:
				src -= 1
			else:
				print "Please input an integer 0-9, or q to quit. "
				continue
				
			if src >= 0:
				src = (src / 3, src % 3)
				for successor in successors:
					if successor.source == src:
						size = state.board_value(src).size
						break
				if size is None:
					print "You do not have a topmost piece at that location. "
					continue
			else:
				src = None
				size = raw_input("What size piece would you like to use (0-2)? ")
				try:
					size = int(size)
				except:
					print "Please input an integer 0-2. "
					continue
				if size < 0 or size > 2:
					print "Please input an integer 0-2. "
					continue
				
				if state.pieces_available(state.get_next_player(), size) <= 0:
					print "You do not have any pieces of that size available. "
					continue
		
			# Ask
			target = raw_input("What square would you like to move to (1-9)? ")
			
			# Human may not have input an integer
			try:
				target = int(target)
			except:
				print "Please input an integer 1-9. "
				continue
			
			if target >= 1 and target <= 9:
				target -= 1
				target = (target / 3, target % 3)
			else:
				print "Please input an integer 1-9. "
				continue
			
			move = gobblet.GobbletMove(gobblet.GobbletMoveDetail(src, target, 
						gobblet.GobbletPiece(state.get_next_player(), size)))
						
			# Human may not have input a valid move
			if not state.is_valid_move(move):
				print "That is not a valid move.  Please choose a target square that "\
					"is occupied only by smaller pieces or no pieces. "
				continue
			
			# Return the valid move
			return move
			
def make_player(name, gameID):
	return GobbletPlayer(name, gameID)
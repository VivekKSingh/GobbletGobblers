#!/usr/bin/env python

import imp
import getopt
import optparse
import os
import sys
import traceback

import game_state
import game_player
import game_controller

MAX_EXPAND = 15
USAGE_STRING = \
"\nUsage 1: %prog [-m | -a] [-e MAX_EXPAND] GAME PLAYER1 PLAYER2\n"\
"Usage 2: %prog -t [-v] [-e MAX_EXPAND] [-x PLAYER] GAME\n\n"\
"GAME specifies the game to be played (see README)\n"\
"PLAYER1, PLAYER2 specify player modules to use for first and second player\n"\
	"\trespectively"
PLAYER_PATH = './players'
GAME_SUFFIX = "State"
PLAYER_SUFFIX = "Player"

def load_module(mName, path, wd):
	"""Loads a module with the indicated name from the indicated path.
	Appends the path to sys.path so any imports from that module will be correctly
	handled.
	wd is the working directory that should be restored after the module loads.
	
	Returns the module object, or None if an exception occurs."""
	f = p = d = mod = None
	if path != '' and path != None and path not in sys.path:
		sys.path.append(path)
	try:
		f,p,d = imp.find_module(mName, None)
		mod = imp.load_module(mName, f, p, d)
	except ImportError as e:
		print "Could not import module", mName
		print e
		return None
	except:
		print "Could not import module", mName, "(unknown error)"
		traceback.print_exc()
		return None
	finally:
		if f != None:
			f.close()
		os.chdir(wd)
	return mod

# TODO: Should throw exceptions
def call_name(mod, name, *args):
	"""Calls the indicated name from the indicated module.  Optional args
	are passed with the call.
	
	Can be used to create a class instance by calling the constructor.
	
	Returns the return value of the the call, or None if an exception occurs."""
	try:
		cl = getattr(mod, name)
		r = cl(*args)
	except AttributeError, e:
		print "Could not get callable object named", name
		print e
		return None
	except:
		print "Could not get callable object named", name, "(unknown error)"
		traceback.print_exc()
		return None
	return r
	

def play_game(gameName, p1Name, p2Name, maxExpansions, p1alphabeta, \
		p2alphabeta):
	"""Plays a game.
	
	"gameName" is the name of the Python module, in the working directory or
	on the path, containing the GameState subclass we want and a make_state() function
	that returns an opening state object.
	
	"p1Name" is the name of the first player's module, which is in
	the "players/[gameName]" subdirectory.  This module must contain a player class
	derived from GamePlayer and a make_player() function that returns
	an instance of this class.
	
	e.g., the simple TicTacToe agent lives in the players/tictactoe/tictactoe_simple.py
	file, which contains the TicTacToePlayer class defining the agent.
	The value of this argument is "tictactoe_simple".
	
	"p2Name" is the name of the second player's module, which works exactly
	the same as the first player's (and can in fact be the same module)
	
	"maxExpansions" is the maximum number of game-tree expansions to allow each
	player as they search during one turn.
	
	"p*alphabeta" is a boolean indicating whether alpha-beta is used or not for
	player1 and player 2, respectively."""
	wd = os.getcwd()
	# Load game, player modules
	gameMod = load_module(gameName.lower(), None, wd)
	p1Mod = load_module(p1Name, os.path.join(PLAYER_PATH, gameName.lower()), wd)
	p2Mod = load_module(p2Name, os.path.join(PLAYER_PATH, gameName.lower()), wd)
	if gameMod == None or p1Mod == None or p2Mod == None:
		sys.exit(2)
	
	# Load game, player classes
	state = call_name(gameMod, "make_state")
	if state == None:
		sys.exit(2)
	gameIDs = state.get_players()
	p1 = call_name(p1Mod, "make_player", p1Name, gameIDs[0])
	p2 = call_name(p2Mod, "make_player", p2Name, gameIDs[1])
	if p1 == None or p2 == None:
		sys.exit(2)
		
	fn1 = game_controller.GameController.ALPHA_BETA if p1alphabeta \
				else game_controller.GameController.MINIMAX
	fn2 = game_controller.GameController.ALPHA_BETA if p2alphabeta \
				else game_controller.GameController.MINIMAX
	
	# Create a game controller
	try:
		gm = game_controller.GameController(state, [p1,p2], [fn1,fn2],
											maxExpansions, wd)
	except game_controller.PlayerException, e:
		print "Player ID not covered!"
		print e
		sys.exit(3)
		
	# keep playing til user wants to stop
	playOn = True	
	while playOn:
		# Reset the game
		gm.reset()
		# Play the game
		winner = gm.play_game()
		if winner == None:
			print "Game is a draw!"
		else:
			winnerName = None
			if p1.get_game_id() == winner:
				winnerName = p1.get_name()
			else:
				winnerName = p2.get_name()
			print winnerName, "wins!"
		
		# get valid input
		while True:
			p = raw_input("Play again (y/n)? ")
			if p == 'y':
				break
			elif p == 'n':
				playOn = False
				break
			else:
				print "Please input 'y' or 'n'"


def play_tournament(gameName, exclusions, maxExpansions, quiet):
	"""Runs a tournament between all the game players it can find for the indicated
	game.
	
	"gameName" is as for play_game() above.
	
	"exclusions" is a list of strings indicating player modules to leave out
	of the tournament (useful for excluding human-interaction modules).
	
	"maxExpansions" is as for play_game() above.
	
	"quiet" indicates that the program should refrain from outputting each and
	every game state as games are played, if True."""
	wd = os.getcwd()
	
	# Load game module
	gameMod = load_module(gameName.lower(), None, wd)
	if gameMod == None:
		sys.exit(2)
	
	# Instantiate game class & get player IDs
	state = call_name(gameMod, "make_state")
	if state == None:
		sys.exit(2)
	playerIDs = state.get_players()
	
	# Get a list of player modules and try to load them
	playerNames = os.listdir(os.path.join(PLAYER_PATH, gameName.lower()))
	playerNames = [x[:-3] for x in playerNames if x.endswith('.py')]
	playerNames = [x for x in playerNames if x not in exclusions]
	playerMods = [load_module(x, \
						os.path.join(PLAYER_PATH, gameName.lower()), wd) \
					for x in playerNames]
	if None in playerMods:
		sys.exit(2)
	
	# Instantiate a player-1 instance and a player-2 instance of every player
	players = [(call_name(x, "make_player", playerNames[i], \
					playerIDs[0]), \
				call_name(x, "make_player", playerNames[i], \
					playerIDs[1])) \
				for i,x in enumerate(playerMods)]
				
	# Cut down the name, module lists to successfully-instantiated players
	playerNames = [x for i,x in enumerate(playerNames) \
					if players[i][0] != None and players[i][1] != None]
	playerMods = [x for i,x in enumerate(playerMods) \
					if players[i][0] != None and players[i][1] != None]
	players = [x for x in players if x[0] != None and x[1] != None]
	
	# Need to know what function to use for each player
	playerFns = [game_controller.GameController.TOURN] * 2
	
	# Player scores are all 0 to begin
	playerScores = [0 for x in players]
	
	# Create a game controller
	try:
		gm = game_controller.GameController(state, \
					[players[0][0],players[1][1]], \
					playerFns, \
					maxExpansions, wd)
	except game_controller.PlayerException, e:
		print "Player ID not covered!"
		print e
		sys.exit(3)
	
	# Play every player as player 1
	for i, p1 in enumerate(players):
		# Against every other player as player 2
		for j, p2 in enumerate(players):
			if i == j:
				continue
			
			# Reset the game
			gm.reset()
			gm.setup_players([p1[0], p2[1]], playerFns)
			# Play the game using tournament functions
			winner = gm.play_game(quiet)
			
			# Output results
			if winner == None:
				print p1[0].get_name(), "vs.", p2[1].get_name(), "is a draw"
				continue
			winnerName = p1[0].get_name() if p1[0].get_game_id() == winner \
							else p2[1].get_name()
			print p1[0].get_name(), "vs.", p2[1].get_name(), "won by", \
							winnerName
			
			# Increment winner's score
			if winner == p1[0].get_game_id():
				playerScores[i] += 1
			else:
				playerScores[j] += 1
	
	# Output final scores of all players
	print
	print "-----------------------------------------"
	print "-----------------------------------------"
	print "Final scores:"
	for i,s in enumerate(playerScores):
		print "Player %s: %d" % (players[i][0].get_name(), s)
	


def main():
	parser = optparse.OptionParser()
	gameName = None
	gameMod = None
	p1Name = None
	p1Mod = None
	p2Name = None
	p2Mod = None
	alphabeta = False
	
	# Set up our option parser
	parser.set_usage(USAGE_STRING)
	parser.add_option("--m1", "--minimax1", action="store_true", dest="minimax1",
		help="Have player 1 use minimax tree search (default).")
	parser.add_option("--a1", "--alpha-beta1", action="store_true", dest="alphabeta1",
		help="Have player 1 use alpha-beta tree search.")
	parser.add_option("--m2", "--minimax2", action="store_true", dest="minimax2",
		help="Have player 2 use minimax tree search (default).")
	parser.add_option("--a2", "--alpha-beta2", action="store_true", dest="alphabeta2",
		help="Have player 2 use alpha-beta tree search.")
	parser.add_option("-t", "--tournament", action="store_true", dest="tournament",
		help="Run a tournament with all compatible players.")
	parser.add_option("-e", "--max-expand", type="int", dest="maxExpand",
		help="Set the maximum number of expansions per ply (default=%d)" \
			% MAX_EXPAND, metavar="MAX_EXPAND")
	parser.add_option("-x", "--exclude", action="append", dest="exclusions",
		help="Exclude a player from the tournament.  Use multiple --exclude " \
		"to exclude many players.", metavar="PLAYER")
	parser.add_option("-v", "--verbose", action="store_false", dest="quiet",
		help="Print out all the game states in tournament mode.")
	parser.set_defaults(alphabeta=False, minimax=False, tournament=False,
		maxExpand=MAX_EXPAND, exclusions=[], quiet=True)
	
	# Parse the arguments
	opts, args = parser.parse_args()
	
	# Using alpha-beta?
	p1alphabeta = False
	p2alphabeta = False
	# Why on earth doesn't optparse handle store_false and store_true to
	#  the same option as mutually exclusive?
	if opts.minimax1 and opts.alphabeta1:
		print "Error: --alpha-beta1 and --minimax1 are mutually exclusive."
		sys.exit(1)
	if opts.minimax2 and opts.alphabeta2:
		print "Error: --alpha-beta2 and --minimax2 are mutually exclusive."
		sys.exit(1)
	if opts.alphabeta1:
		p1alphabeta = True
	if opts.alphabeta2:
		p2alphabeta = True
	
	# Playing a tournament
	if opts.tournament:
		if len(args) != 1:
			print "Error: Tournament requires 1 argument.  "\
					"Use '-h' for more information."
			sys.exit(1)
		
		# Minimax, alpha-beta options meaningless to tournament play
		if opts.minimax1 or opts.alphabeta1 or opts.minimax2 or opts.alphabeta2:
			print "Error: Minimax and alpha-beta specifications are "\
					"compatible only with non-tournament play.  Use '-h' "\
					"for more information."
			sys.exit(1)
		
		# Get the game name
		gameName = args[0]
		
		# Run the tournament
		play_tournament(gameName, opts.exclusions, opts.maxExpand, opts.quiet)
		
	# Just playing one player against another
	else:
		# There shouldn't be exclusions
		if len(opts.exclusions) > 0:
			print "Error: Player exclusions are compatible only with "\
					"tournament play.  Use '-h' for more information."
			sys.exit(1)
		
		# There should be three args which are not options
		if len(args) != 3:
			print "Error: Game requires 3 arguments.  "\
					"Use '-h' for more information."
			sys.exit(1)
		
		# Get the game and player names (see comemnts for play_game())
		gameName = args[0]
		p1Name = args[1]
		p2Name = args[2]
		
		print "\nBeginning", gameName, "with players", p1Name, "and", p2Name, \
			"using", "alpha-beta" if p1alphabeta or p2alphabeta else "minimax", "planning.\n"
		
		# Go ahead and play
		play_game(gameName, p1Name, p2Name, opts.maxExpand, p1alphabeta, p2alphabeta)

if __name__ == "__main__":
	main()

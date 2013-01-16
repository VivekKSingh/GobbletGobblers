------------------------------------------------------------------
SHORT VERSION

There's a lot of information in this README.  You should read all of it.
However, here's the quick version so you can keep track of it all.

-Game framework is defined in files named game*.py in the top directory.
-Invoke the program with "./game.py" or "python game.py".  Use the -h switch for
	help.
-Game names you can give the program are "TicTacToe" and "Gobblet" (NB: case-
	sensitive!).  "TicTacToe" is an example game, "Gobblet" is what you're working on.
-Game logic definitions are in tictactoe.py and gobblet.py in the top directory.
-Game players are in players/GAME_NAME/ subdirectories.
-WHAT YOU HAVE TO DO:
	-Rename players/gobblet/username.py to have your username instead of
		"username" (e.g., Mark's is "mw54.py").
	-Implement the minimax_move() method in the GobbletPlayer class in the file
		with your username.  See "hw2.pdf" for details.
	-Implement the alpha_beta_move() method in the GobbletPlayer class in the
		file with your username.  See "hw2.pdf" for details.
	-Implement the tournament_move() method in the GobbletPlayer class in the
		file with your username.  See "hw2.pdf" for details.
	-Answer the written questions from "hw2.pdf" and type or write your answers.
	-Upload the Python file with your username to OnCourse and turn in the
		written answers in hard-copy.
-WHAT YOU MAY DO:
	-You may wish to define additional modules.  These files MUST go in the
		players/gobblet/ subdirectory and MUST have names starting with your
		username (e.g., "mw54_aux.py").  Make sure you upload these files to
		OnCourse.
	-Clever stuff in your tournament_move() might require external files
		(e.g., to contain databases of endgame moves).  These files MUST go
		in the players/gobblet/ subdirectory (see players/gobblet/username.py for
		an example of how to load a file in that location) and MUST have names
		starting with your username (e.g., "mw54_endgame_db.txt").  Do not
		give files which are not Python files the .py extension, please.  Make
		sure you upload these files to OnCourse.
-WHAT YOU MAY NOT DO:
	-Modify the game*.py framework files or the gobblet.py game definition file.
		When grading we will use the canonical versions of these files and any
		changes you make will not be in effect.

------------------------------------------------------------------
INVOKING THE GAME SYSTEM

On UNIX systems, the file "game.py" is executable, meaning you can do:
./game.py
at the command line.  I will use this convention for invocation as it is
shorter.

On Windows systems, this will likely need to be:
python game.py
at the command line.

At any time, you can do:
./game.py -h
for help.

There are two modes for the game system:  Regular play, and tournament.  In
regular-play mode, you provide the program with the name of a game module and two
player modules, and the system will run a single game between them, showing
each move, and at the end display the results and ask if you would like to play
again.  All modules are specified by the names of their files, without extensions.
See below in this README for information about invoking specific games included
in the package.
Regular play is invoked with:
./game.py [options] GAME PLAYER1 PLAYER2

In tournament mode, you provide the program with the name of a game, and the
system will find as many compatible player modules as it can.  Then it will
play every player against every other player, once as the first player in the
game and once as the second.  It will print the outcomes of each game as
the tournament progresses, and at the end it will display the number of games
won by each player.  Tournament play is invoked with:
./game.py -t [options] GAME

In regular-play mode, you have a number of options:
--m1 or --minimax1 calls Player 1's minimax search functions, which is the
	default behavior.  Likewise for --m2 and --minimax2.
--a1 or --alpha-beta1 calls Player 1's alpha-beta pruning search functions.
	--m1 and --a1 are incompatible, for obvious reasons.  Likewise for --a2
	and --alpha-beta2.
-e or --max-expand MAX_EXPAND allows each player MAX_EXPAND expansions of the
	game state during each turn's search.  MAX_EXPAND should be
	an integer value.

In tournament mode, you also have some options:
-e or --max-expand MAX EXPAND works exactly as for regular play.
-v or --verbose causes the system to output every game state as play progresses,
	just like it does in regular play.
-x or --exclude PLAYER excludes a specific player module from tournament play.
	This is useful if we wish to leave out a human-interactive player or a
	malfunctioning module from a computer tournament.

------------------------------------------------------------------
GENERIC REMARKS ABOUT THE FRAMEWORK AND ITS STRUCTURE

Students:  This section contains information which may be of interest to you
as well as to anyone who uses this framework to implement other games in the
future.  However, you should read the next section of this file for specific
instructions about this assignment, including where to write code and how to
name your files.

The Python files packaged with this README provide a generic game-playing
template program for two-player games, as well as the definitions for the
specific game for this semester.

The following four files define pieces of the basic game-playing framework.
STUDENTS SHOULD NOT MODIFY THESE FILES and this overview is presented merely
for your understanding of the framework.

-game_state.py -- This file defines three classes.  Two of these classes
	are intended to be subclassed for specific games, as we shall see shortly.
	Files containing subclasses for game_state.py should be kept in the same
	directory and follow strict naming conventions which will be described
	later.
	-GameSuccessor -- an object that contains two data members, move and state,
	representing a move and a subsequent state that comprise a successor in a game.
	-GameMove -- an object of this type represents one move to be made in a game.
		Should be subclassed for a specific game.
	-GameState -- an object of this type represents one state (i.e., board
		position) in a game.  The logic of game rules is also coded
		into this class via methods such as move(), is_valid_move(),
		successors(), etc.  Should be subclassed for a specific game.
		
-game_player.py -- This file defines one base class, GamePlayer.  An object of
	this type represents one player in a game and defines that player's logic
	for gameplay.  This class is intended to be subclassed for specific games.
	Files containing subclasses for game_player.py should be kept in the
	players/ subdirectory tree and follow naming conventions which will
	be described shortly.

-game_controller.py -- This file defines three classes:
	-GameExpansionCounter -- an object of this type is shared among states used
	to explore a minimax tree and keeps track of how many more expansions the player
	is allowed on the current move.
	-GameController -- handles the logic of playing ONE game between TWO SPECIFIC 
	player objects.  GameController is intended to operate generically on
	superclass instances (GameState, GameMove, GamePlayer) and should not need 
	to be subclassed.
	-PlayerException -- An exception thrown by the GameController in unusual
	circumstances.

-game.py -- This is the "main" file of the program.  It handles command-line
	options, imports and creates the relevant game and player classes, and runs
	games or tournaments using GameController.  This file contains no class
	definitions and should not need to be modified.
	
There are important rules for writing extensions to the framework for specific
games.  Some of these have to do with details of implementation, such as which
methods to override and what they do;  these are covered by the comments in the
above files.  Other rules capture how the extensions should be named and where
their module files should be placed.

RULE 1:  Pick a Python-compatible module name (for instance, tictactoe) for your game.
RULE 2:  You should create three subclasses for the GameMove, GameState, and 
	GamePlayer base classes.  For instance, TicTacToeMove, TicTacToeState,
	TicTacToePlayer.
RULE 3:  Your -Move and -State subclasses should reside in a file in the top-
	level directory of the package, along with game_state.py,
	game_controller.py, game_player.py, and game.py.  This file's name should
	be the name you picked in rule 1, with a .py extension.  The file should 
	also contain a function named make_state() that returns a new instance of
	the -State subclass.
RULE 4:  Your -Player subclasses should reside in a subdirectory of the
	players/ directory.  This subdirectory's name should be the name you picked
	in rule 1.  You may have as many -Player subclasses
	as you like, but each one should reside alone in a file with a
	different name (STUDENTS: see rules about naming your submissions at the
	end of this file!).  For instance, tictactoe_simple.py and tictactoe_adv.py
	are both located in the players/tictactoe/ directory.  Each file should also
	have a make_player() function that accepts name and game-ID arguments and returns
	a new instance of the -Player subclass in that file.
	
	
In addition to the framework, one simple but complete implementation of an
EXAMPLE game is presented so you can see a simple use of the framework and also
get an idea how to implement your own player agents.  NOTE:  Again, this game
(Tic-tac-toe) is presented as an EXAMPLE and is NOT the game you will be working
on for the assignment.

-tictactoe.py -- This file defines subclasses of GameMove and GameState
	to represent moves and states in a game of tic-tac-toe (aka noughts and
	crosses -- see http://en.wikipedia.org/wiki/Tic-tac-toe).  The complete
	logic of tic-tac-toe is encapsulated in TicTacToeState's methods.
	
-players/tictactoe/tictactoe_simple.py -- This file defines an incredibly simple
	Tic-tac-toe playing agent -- all it does is request a list of successor
	moves from the current state of the game and pick the first one.  Obviously,
	this is not a very good approach to the game.
	
-players/tictactoe/tictactoe_human.py -- This file defines a Tic-tac-toe playing
	agent which asks a human player for input.  This allows you, the human,
	to play against one of the computer opponents.
	
-players/tictactoe/tictactoe_adv.py -- This file defines a smarter computerized
	Tic-tac-toe agent.  It has an evaluation function which treats the player
	using X as MAX and the player using O as min, and it can perform minimax
	and alpha-beta pruning searches through the game tree using the game-logic
	methods of the game-state objects.  Your player agent for the assignment
	game (below) should be loosely modeled on these lines.

Tic-tac-toe is invoked on the command line by passing the game name "tictactoe"
to the game.py script, along with two of "tictactoe_simple", "tictactoe_adv",
and "tictactoe_human" for the player names.

e.g.:
./game.py tictactoe tictactoe_simple tictactoe_adv
./game.py -a -e 45 tictactoe tictactoe_adv tictactoe_human
./game.py -t -v -x tictactoe_human tictactoe


---------------------------------------------------------------------
ASSIGNMENT-SPECIFIC INSTRUCTIONS FOR STUDENTS

Finally, the package contains an implementation of the game you will be working
on for the assignment.  This semester we are using the Gobblet Gobblers game from
Blue Orange Games.  The definition of the game --
representation of its states, moves, and logic -- is contained in the file
gobblet.py, which provides Gobblers-specific subclasses of GameMove and GameState.
A list of the rules we are using is provided below.

A questionably-intelligent Gobblers agent, using the same "pick-the-first-
successor" strategy as the simple Tic-tac-toe agent above, is in
players/gobblet/gobblet_simple.py.  A human-interactive agent, which will ask a
human player for input, resides in players/gobblet/gobblet_human.py.

Finally, and importantly, an incomplete Gobblet agent resides in
players/gobblet/username.py.  RENAME THIS FILE TO HAVE YOUR IU USERNAME.  For
instance, Mark's username is "mw54", so his Gobblers agent would be in the file
players/gobblet/mw54.py.

Follow the instructions in hw2.pdf to complete the Gobblers agent and answer the
written questions.  When searching the game tree, you may call the GobbletState
object's successors() method to get a list of tuples.  Each tuple will consist
of (player, state, move) values, representing the next player in the game (for
Gobblet Gobblers, this is always the opposite player to the one who moved), the state the
game will be in after the move is made, and the move which will lead to that
state.  These will all be legal moves.  Of course, you may call the successors()
method of each of the resulting states to get more moves, but eventually the
game will bar you from expanding any more states (when you hit the maximum
number of expansions per turn, specified at the command line).

Writing external modules for your player is discouraged, but can be done.  The
module should be placed in the players/gobblet/ directory and given a name
which starts with your username (e.g., "mw54_aux.py").  When you are ready to
submit, simply submit the module file along with your agent file and your
written answers.

If you need to load data from an external data file, place the file in the
players/gobblet/ directory and give it a name starting with your username
(e.g., "mw54_endgame_db.txt").  There is an example in the incomplete Gobblet
agent of how to load an external file -- please note, particularly, the process
of saving the working directory, changing directory, using the file, and then
restoring the original working directory.  Remember to upload your data files 
along with your submission.  Your data files should never have .py extensions 
if they are not valid Python files.


RULES FOR GOBBLERS
- See an overview of Gobblers at http://www.blueorangegames.com/instructions.php
- Specific rules we are using:
	- Blue always moves first.
	- When a cycle in the game is detected, the game is declared a draw.
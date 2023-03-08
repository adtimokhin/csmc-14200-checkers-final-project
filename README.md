# Checkers

This repository contains a design and implementation
for Checkers game.
This is a project by

* [adtimokhin](https://github.com/adtimokhin) (TUI)
* [rahulgarge](https://github.com/rahulgarga) (Game Logic)
* [pborisova](https://github.com/pborisova-cs) (GUI)
* [nikitarodin](https://github.com/nikitarodin) (Bot)


# Setup
To install the required Python libraries run the following:

    pip3 install -r requirements.txt

# Running TUI
To run TUI with default parameters, run the following from the root of the repository:

    python3 src/tui.py

Default parameters include:
Two real players (given names `Player One` and `Player Two`) playing on a board size 8 x 6.

## Tailoring Parameters

The command has two flags for providing information about the players:

    python3 src/tui.py --player-1 <value_1> --player-2 <value_2>

The flags are optional.
Both flags have exactly the same behaviour. The following values can be passed as the values of the flags:

1. `random-bot` - will replace a player with a bot that follows a random strategy
2. `smart-bot` - will replace a player with a bot that follows a real strategy. The strategy the bot follows is described [here](https://hobbylark.com/board-games/Checkers-Strategy-Tactics-How-To-Win). 
3. `Any name` - if any other value than from points 1 and 2 is entered then the name of the real player will be altered to the value set in the flag

There are also two flags that can be set to tailor the size of the board on which checkers are played.

    python3 src/tui.py --width <int_value> --rows-with-pieces <int_value>

* `--width` - sets number of columns (aka width) of the board. Default is 8

* `--rows-with-pieces` - sets number of rows each will start with that will contain their game pieces. Default is 2

### Example of the command call:

    python3 src/tui.py --player-1 Walter --player-2 random-bot --width 10 --rows-with-pieces 3


___

# Running GUI
To run TUI with default parameters, run the following from the root of the repository:

     python3 src/gui.py

## Tailoring Parameters

The command has two flags for providing information about the players:

    python3 src/gui.py --player-1 <value_1> --player-2 <value_2>

The flags are optional.
Both flags have exactly the same behaviour. The following values can be passed as the values of the flags:

1. `random-bot` - will replace a player with a bot that follows a random strategy
2. `checkers-bot` - will replace a player with a bot that follows a real strategy. The strategy the bot follows is described [here](https://hobbylark.com/board-games/Checkers-Strategy-Tactics-How-To-Win). 
3. `human` - will make player to be a real human player! This is a default value for both the flags.

# Changes to design

## Board class
* We added extra attribute to the class: players. That is a list of players that will play on the board.
* Changed number_of_row to be an attibute n - number of lines of checkers pieces
* Made a method is_empty_cell() which checks if a cell is empty.
* Added a repr method for a printable representation of the board
* Added many new methods get_possible_moves, get_possible_moves_for_piece, get_possible_jumps which are very specific to various needs of the player
 -- for example, if a player decides he wants to move a specific piece, then get_possible_moves_for_piece returns the moves for that piece.
* Added a method place_piece which does the opposite of remove_piece
* Note: we received conflicting feedback about whether to move the methods from the board class to Class Game; however, we decided to keep them 
in the board class, meaning our board is not general, it is checkers-specific, and we did away with Class Game as it is now obsolete and its functionality has been moved elsewhere

## Bots:

### RandomBot

* added a bot which picks random moves to test efficency of a newly created bot 

### CheckersBot

* designed a bot which actually is capable to play a game of checkers more or less properly 
* researched a few heuristics on how to play checkers 

## TUI
* Added a class responsible for I/O interactions through text-based interface.
* Added methods for getting boolean and integer inputs from users.

## TUIGame
* Added a class to perform game logic stuff (that were previously part of Game class)

## GUI
* Added methods that will provide all necessary interaction between user and the game logic via GUI

## Game
* Moved functionality to play the actual game to the TUI- and GUI-related classes
* Extended the methods to allow selecting moves based on whether they are jumps or all moves allowed for a piece/player.
* Moved the methods that are responsible for the game logic back to this class (removed the functions from Board class, where they were after Milestone 2).


# Changes to implementation made since Milestone 2

## TUI
* Fixed a bug where a bot was asked if they want to offer/accept a draw. Bots do not give up!
* Added a winner screen after the game has finished
* Made code for the function that prints the board into the terminal more readable
* Added unit tests for TUIGame, located in test_tui.py
* Made it so that player must choose a jump move if one is available.


## Game
* Decided to move most of the functions related to the game logic back to this class from the Board class. Now Game acts as an interface, connecting Board, Players, GamePiences, TUI, and GUI.
* Made a recursive method to find all possible jumps of the piece.

## Board
* Made Board to be rectangular rather than square. Now you can set width and height separately.
* Game logic was moved to the Game class

## GUI

* Made implementation more in line with the design (mostly done by updating the design, however).
* Made changes to the is_jump method in Class Board to make it more comprehensive
* Initialized placing pieces on the board as part of the constructor in Class Board
* Removed is_valid_position method
* Updated get_possible_jumps method
* Updated get_possible_moves_for_piece method
* Removed the class for encapsulating the functions since it was unnecessary

## BOT

*Updated metrics and algorythms to choose the optimal move due to changes in design
*Spesifically changed the implementation of best_jump_method
*Fixed a bug, connected to avoiding danger, which didn't account for current position becoming empty after the move
*Added a small simulation in a main function in a file, which you can run by running bot.py file and get a win-ratio for the bot
*Added unit tests in a seperate file to check basic functionality of a bot
*tests are in test_for_bot, and can be run with pytest

# How we addressed feedback from TA

Most of the changes that we made were described above. One that we did not outline properly was that we made a move to be of this weired structure that is outlined below. We did it, as TA has recomended, to be able to track the whole path the piece makes when is moved.

`list[GamePiece, list[tuple(int,int)]]`

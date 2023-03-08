"""
This is a file that contains logic for TUI

Aleksnadr Timokhin
"""

from rich.console import Console
import click

from game import Game
from player import Player
from board import Board
from bot import CheckersBot, RandomBot

import math

class TUI:
    """
    This class is used to call methods for interacting with user via a console 
    (Text-Based User Interface).
    Both input and output functions are located here
    """
    def __init__(self):
        self.console = Console()
    
    def print_board(self, game, highlights=[]):
        """
        This function prints the board to the console

        Args:
            game (Game): The game to be printed

        """
        board = game.board
        player_colours = list(player.color for player in game.players) 
        board_colours = ["#eddad3", "#4a2112"]  # Colours of the game board pieces
        highlight_colour = "on blue"

        spaces_at_front = math.floor(math.log10(board.number_of_cols))

        # separator_line = " "+f"+-" * board.number_of_cols + "+"
        top_line = (" " * spaces_at_front) + " " # This space is for the top line of the board
        for i in range(1, board.number_of_cols+1):
            top_line += (" " * (spaces_at_front -
                                   math.floor(math.log10(i)))) + f" {i}"

        separator_line = (" " * spaces_at_front) + " " + ("+" + "-" *
                            (spaces_at_front + 1)) *board.number_of_cols + "+"
        self.console.print(top_line)
        self.console.print(separator_line)
        row_number = 0
        for row in board.grid:
            line_to_print = (" " * (spaces_at_front - math.floor(
                math.log10(row_number + 1)))) + f"{row_number + 1}|"
            col_number = 0
            for col in row:
                bg_colour = "on " + board_colours[(row_number + col_number) % 2]
                if (row_number, col_number) in highlights:
                    bg_colour = highlight_colour
                char_to_print = " "
                if col is not None:
                    player_index = game.players.index(col.player)
                    if col.is_king:
                        char_to_print = "K"
                    else:
                        char_to_print = "O"
                    # Adding color to the symbol
                    char_to_print = f"[{player_colours[player_index]}]{char_to_print}[/{player_colours[player_index]}]"
                line_to_print += f"[{bg_colour}]"+f" " * ((spaces_at_front)) +f"{char_to_print}[/{bg_colour}]|"
                col_number += 1
            # 1. Print the row content
            self.console.print(line_to_print)
            # 2. Print the separator line
            self.console.print(separator_line)
            row_number += 1

    def get_int_input(self, prompt, range=(-1, -1)):
        """
        This method will repeatedly ask user to select a user to enter an
        integer until a valid value is given.
        Inputs:
            prompt (str) - a message that explains what the input is for
            range (tuple(int, int)) - an inclusive range of accepted values, as
                                    follows: (min_val, max_val). If the tuple is
                                    given as (-1,-1) then the range is not
                                    applicable.
        Output:
            (int) - a value of type integer and in a certain range,
                    if was provided.
        """
        result = -1
        valid_input = False
        while not valid_input:
            self.console.print(f"[on red]{prompt}[/on red]")
            result = input()
            try:
                result = int(result)
                if range != (-1, -1):
                    if range[0] <= result <= range[1]:
                        valid_input = True
                    else:
                        self.console.print(f"The value should be in range from"+
                                        f"{range[0]} to {range[1]} inclusively")
                else:
                    valid_input = True
            except ValueError:
                self.console.print("This is not an integer!")
        return result

    def get_bool_input(self, prompt, true_ans=["y"], false_ans=["n"]):
        """
        This method will repeatedly ask user to select a user to enter an string
        until a valid value is given.
        Inputs:
            prompt (str) - a message that explains what the input is for
            true_ans (list[str]) - a list of inputs by user that would be
                            considered to be equivalent to an answer of True
            false_ans (list[str]) - a list of inputs by user that would be
                            considered to be equivalent to an answer of False
        Output:
            (bool) - a value of type integer and in a certain range,
                    if was provided.
        """

        result = False
        valid_answer = False
        while not valid_answer:
            self.console.print(f"[on red]{prompt}[/on red]")
            self.console.print(f"to answer [green]'yes'[/green] type one of"
                               f" these values: {true_ans}")
            self.console.print(f"to answer [red]'no'[/red] type one of"
                               f" these values: {false_ans}")
            user_input = input().lower()
            if user_input in true_ans:
                result = True
                valid_answer = True
            elif user_input in false_ans:
                result = False
                valid_answer = True
            else:
                self.console.print("This is an invalid answer")

        return result

    def print_winner_screen(self, winner=None) -> None:
        """
        Prints information which player won.

        Input:
            player (Player) - player that has won the game. 
                            If player is passed as None, then the game was 
                            terminated with a draw
        """
        self.console.print("-"*10 + " [yellow]THE GAME IS OVER[/yellow] " + "-"*10)
        if winner is None:
            self.console.print("[green]DRAW![/green] There is no winner")
        else:
            self.console.print(f"Winner: [on green]{winner.name}[/on green]")
        self.console.print("-"*10)  

    def get_valid_pos(self, valid_poisitions):
        row = -1
        col = -1

        while (row,col) not in valid_poisitions:
            self.console.print("Choose a piece to move")

            row = -1 + self.get_int_input("Select a row: ")
            col = -1 + self.get_int_input("Select a column: ")

            if (row, col) not in valid_poisitions:
                self.console.print("Invalid position")
        return (row, col)

    def get_player_move(self,player,game):
        possible_jumps = game.get_all_jumps(player)
       
        if possible_jumps == []:
            possible_moves = game.get_possible_moves(player)
            pieces_that_can_be_moved = []
            for move in possible_moves:
                pieces_that_can_be_moved.append(move[0])
            pieces_that_can_be_moved = list(set(pieces_that_can_be_moved)) # Remove duplicates

            pieces_that_can_be_moved_pos = list(piece.position for piece in pieces_that_can_be_moved)
            # Print the board with pieces that can be moved
            self.console.print(f"[on green]{player.name}[/on green] can move this pieces:")
            self.print_board(game, highlights=pieces_that_can_be_moved_pos)

            # Force user to chose valid game_piece position
            valid_piece_pos = self.get_valid_pos(pieces_that_can_be_moved_pos)
            piece_to_move = game.board.grid[valid_piece_pos[0]][valid_piece_pos[1]]

            # Print possible moves for that piece
            possible_piece_moves = game.get_possible_moves_for_piece(piece_to_move)
            arriving_positions = []
            for move in possible_piece_moves:
                arriving_positions.append(move[1][-1])
            self.console.print(f"[on green]{player.name}[/on green] This is where you can move your piece to:")
            self.print_board(game, highlights=arriving_positions)

            # Force user to chose valid game_piece position
            valid_final_piece_pos = self.get_valid_pos(arriving_positions)
            move_selected = []
            for move in possible_piece_moves:
                if move[1][-1] == valid_final_piece_pos:
                    move_selected = move
            return move_selected
        else:
            pieces_that_can_be_moved = []
            for move in possible_jumps:
                pieces_that_can_be_moved.append(move[0])
            pieces_that_can_be_moved = list(set(pieces_that_can_be_moved)) # Remove duplicates

            pieces_that_can_be_moved_pos = list(piece.position for piece in pieces_that_can_be_moved)
            # Print the board with pieces that can be moved
            self.console.print(f"[on green]{player.name}[/on green] can move this pieces:")
            self.print_board(game, highlights=pieces_that_can_be_moved_pos)
            # Force user to chose valid game_piece position
            valid_piece_pos = self.get_valid_pos(pieces_that_can_be_moved_pos)
            piece_to_move = game.board.grid[valid_piece_pos[0]][valid_piece_pos[1]]
            # Print possible moves for that piece
            possible_piece_moves = game.get_possible_jumps_for_piece(piece_to_move)
            moves_paths = list(move[1] for move in possible_piece_moves)

            self.console.print(f"There are {len(possible_piece_moves)} possible jumps for this piece:")
            for index, path in enumerate(moves_paths):
                self.console.print(f"{index + 1}: {path}")
            
            # Showing a move path if player wants to see it
            while self.get_bool_input("Do you want to see a path of a certain jump?"):
                jump_index = -1 + self.get_int_input("Select a jump number: " , (1,len(moves_paths)))
                self.print_board(game, highlights=moves_paths[jump_index])
            
            # Force user to chose valid game_piece position
            self.console.print(f"There are {len(possible_piece_moves)} possible jumps for this piece:")
            for index, path in enumerate(moves_paths):
                self.console.print(f"{index + 1}: {path}")
            jump_index = -1 + self.get_int_input("Select a jump number that you will make: " , (1,len(moves_paths)))
            return possible_piece_moves[jump_index]

  
def is_bot(player) -> bool:
    """
    This method checks if the user passed in parameters is a Bot.

    Input:
        player (Player) - player or an object that inherits from Player class

    Output:
        True - if the player is of class that inherits Player
        False - if the player is of class Player and not its children.
    """
    return type(player) is RandomBot or type(player) is CheckersBot
   

class TUIGame:
    
    def __init__(self, game):
        self.game = game
        self.tui = TUI()

    def play_game(self):
        """
        This function is called to play the game,
        using the board set as a class parameters
        """

        turn = 0
        player_count = len(self.game.players)
        is_draw = False

        current_player = self.game.players[0]
        next_player = self.game.players[1]

        # Flag that checks if the players should have a offer_draw option
        should_offer_draw = not(is_bot(current_player) or is_bot(next_player))


        # Game loop
        while not (self.check_player_lost(current_player) or is_draw):
             # Printing board
            self.tui.print_board(self.game)
            
            # A turns starts with asking if users want to declare a draw
            if should_offer_draw:
                is_draw = self.is_draw(current_player,
                                         next_player)
                if is_draw:
                    # Then the game finishes with a draw
                    continue   
                # When the game is over, a description of how the game ended should 
             
            # Asking for players move.
            if is_bot(current_player):
                move = current_player.choose_move(self.game.board, self.game.get_possible_moves(current_player))
            else:
                move = self.tui.get_player_move(current_player, self.game)

            # Performing the move
            self.game.make_move(move)

            # Updating some pointers
            turn += 1
            current_player = self.game.players[turn % player_count]
            next_player = self.game.players[(turn + 1) % player_count]

        # When the game is over, a description of how the game ended should 
        # be provided
        winner = None if is_draw else self.game.players[(turn + 1) % player_count]
        self.tui.print_winner_screen(winner)         

    def check_player_lost(self, current_player):
        """
        Checks if the player lost the game or not
        Input:
            current_player (Player) - a player whose turn it is
        Output:
            True - if the player has lost the game
            False - if the player has not lost the game
        """
        valid_moves = self.game.get_possible_moves(current_player)
        return valid_moves == []

    def is_draw(self, current_player, next_player):
        """
        Checks if draw is offered and accepted. Prompts users to
        enter their answer to see if the game should end with a draw.
        Input:
            current_player (Player) - Player that can offer a draw as 
                                      it is their turn.
            next_player (Player) - Player to whom offer can be offered, and they
                                    may accept it or not.
        Output:
            True - the game should be terminated with a draw
            False - the game continues
        """
        if self.tui.get_bool_input(prompt=f"Do you, {current_player.name}," + \
                                f" want to offer a draw to your opponent?",
                                true_ans=["y", "yes"], false_ans=["n", "no"]):
            return self.tui.get_bool_input(
                prompt=f"Do you, {next_player.name}, want to accept a draw" + \
                       f" offered by your opponent?",
                true_ans=["y", "yes"], false_ans=["n", "no"])

        return False

@click.command(name="checkers-tui")
@click.option('--player-1-type', default="Player One")
@click.option('--player-2-type', default="Player Two")
@click.option('--width', default=8)
@click.option('--rows-with-pieces', default=2)
def cmd(player_1_type, player_2_type, width, rows_with_pieces):

    if player_1_type == "random-bot":
        player_1 = RandomBot("random-bot-1","#5442f5")
    elif player_1_type == "smart-bot":
        player_1 = CheckersBot("smart-bot-1","#5442f5")
    else:
        player_1 = Player(player_1_type, "#5442f5")

    if player_2_type == "random-bot":
        player_2 = RandomBot("random-bot-2","#42f2f5")
    elif player_2_type == "smart-bot":
        player_2 = CheckersBot("smart-bot-2","#42f2f5")
    else:
        player_2 = Player(player_2_type, "#42f2f5")
    
    players = [player_1, player_2]
    game = Game(players, rows_with_pieces, width)

    tui_game = TUIGame(game)

    tui_game.play_game()


if __name__ == "__main__":
    cmd()

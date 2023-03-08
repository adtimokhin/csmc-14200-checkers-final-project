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

    REGULAR_GAME_PIECE_SYMBOL = "O"
    KING_GAME_PIECE_SYMBOL ="K"

    def __init__(self):
        self.console = Console()
    
    def print_board(self, game):
        """
        This function prints the board to the console

        Args:
            game (Game): The game to be printed

        """
        board = game.board
        player_colours = list(player.color for player in game.players) 
        board_colours = ["#eddad3", "#4a2112"]  # Colours of the game board pieces

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

            


class TUIGame:
    
    def __init__(self, game):
        self.game = game
        self.tui = TUI()


    def play_game(self) -> None:
        """
        This function is called to play the game,
        using the board set as a class parameters
        """

        # Printing board
        self.tui.print_board(self.game)


# @click.command(name="checkers-tui")
def cmd():
    player_1 = Player("Player 1", "#5442f5")
    player_2 = Player("Player 2", "#42f2f5")
    players = [player_1, player_2]

    game = Game(players, 2,6)
    tui_game = TUIGame(game)
    tui_game.play_game()


if __name__ == "__main__":
    cmd()

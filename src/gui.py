"""
GUI for checkers

Polina Borisova

This is an updated version of the GUI. 
It is possible for us to do the following:
    - Start the GUI and play against another human player (on the same computer)
    - Have two human players play a game of Checkers until one of them wins

The code relies on game logic implementation done by Aleksnadr with some minor 
updates:
    - get_captured_position function is implemented
    - the logic for moves/jumps is updated depending on the piece kind (king or 
    not)

To test the default mode of the game (2 human players, 8x8 board), run the 
following from the root of the repository:
python3 src/gui.py

NEED TO DO: update the code to play against the bot
"""

import pygame
from pygame.locals import *
import sys
import click

from player import Player
from board import Board
from game_piece import GamePiece
from bot import CheckersBot, RandomBot
from game import Game
from tui import is_bot

WIDTH = 600
HEIGHT = 600
RED = (161, 8, 8)
BLACK = (0, 0, 0)
WHITE = (255,255,255)
GOLD = (245, 217, 61)
GREEN = (25, 176, 95)
BLUE = (0, 120, 224)
YELLOW = (245, 245, 44)
BROWN = (166, 75, 0)
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))


def is_players_piece(surface, coordinates, player_color):
    '''
    Checks if the selected location stores the piece of a given player
    '''
    if player_color == "Red":
        if tuple(pygame.Surface.get_at(surface, coordinates)[:3]) == RED:
            return True
    if player_color == "Black":
        if tuple(pygame.Surface.get_at(surface, coordinates)[:3]) == BLACK:
            return True

def get_piece(board, coordinates):
    '''
    Finds and returns the piece (GamePiece) on the board given its coordinates
    '''
    x, y = coordinates
    piece = board.grid[x][y]
    return piece

def get_position(coordinates, game):
    '''
    Converts pixel coordinates into board position (row, column)
    '''
    x, y = coordinates
    square_width = WIDTH / game.board.number_of_cols
    square_height = HEIGHT /game.board.number_of_rows 
    column = x // square_width 
    row = y // square_height
    column = int(column)
    row = int(row)
    position = (row, column)
    return position

def draw_board(game, surface, game_piece = None) -> None:
    """ 
    Draws the current state of the board in the window
    Args:
        surface: Pygame surface to draw the board on
        board: The board to draw
    Returns: None
    """
    background = WHITE
    surface.fill(background)

    nrows = len(game.board.grid)
    ncols = len(game.board.grid[0])

    grid = game.board.grid

    
    # Compute the row height and column width
    row_height = HEIGHT // nrows + 1
    column_width = WIDTH // ncols + 1

    # Draw the board
    board_squares = []
    for row in range(nrows):
        for col in range(ncols):
            rect = (col * column_width, row * row_height, column_width, row_height)

            if row % 2 != 0 and col % 2 == 1: 
                pygame.draw.rect(surface, color=BROWN, rect = rect)
                rect = Rect(rect)
                board_squares.append(rect)

            if row % 2 == 0 and col % 2 != 1: 
                pygame.draw.rect(surface, color=BROWN, rect = rect)
                rect = Rect(rect)
                board_squares.append(rect)
            
    if game_piece is not None: 
        # Highlight game piece
        row, col = game_piece.position
        rect = (col * column_width, row * row_height, column_width, row_height)
        pygame.draw.rect(surface, color= YELLOW, rect = rect)

        # Highlight all valid moves (prioritize jumps)
        moves = game.get_possible_moves_for_piece(game_piece)
        jumps = game.get_possible_jumps_for_piece(game_piece)

        if jumps != []: 
            jumps = list(move[1][-1] for move in jumps)
            for jump in jumps:
                    row, col = jump
                    rect = (col * column_width, row * row_height, column_width, row_height)
                    pygame.draw.rect(surface, color= BLUE, rect = rect)
        else:
            if moves != []:
                moves = list(move[1][-1] for move in moves)
                for move in moves:
                    row, col = move
                    rect = (col * column_width, row * row_height, column_width, row_height)
                    pygame.draw.rect(surface, color= GREEN, rect = rect)
        
    # Draw the game pieces
    for i, row in enumerate(grid):
        for j, piece in enumerate(row):
            if piece is not None:
                if piece.player.color == "Red":
                    color = RED
                if piece.player.color == "Black":
                    color = BLACK
                center = (j * column_width + column_width // 2, i * row_height + row_height // 2)
                radius = row_height // 2 - 8
                if not piece.is_king:
                    pygame.draw.circle(surface, color=color,
                                    center=center, radius=radius)
                if piece.is_king:
                    pygame.draw.circle(surface, color=color,
                                    center=center, radius=radius)
                    color = GOLD
                    radius = radius - 16
                    pygame.draw.circle(surface, color=color,
                                    center=center, radius=radius)
                    
    pygame.display.flip()

def play_checkers(game):
    '''
    Plays a game of Checkers on a Pygame window
    Args:
        board: The board to play on
        players: A list of players (GUIPlayer objects)
    Returns: None
    '''
    # Initialize Pygame
    pygame.init()
    pygame.display.set_caption("Checkers")
    draw_board(game, SCREEN)

    # 
    current_player = game.players[0]
    next_player = game.players[1]

    selected = None
    # Game loop
    while not check_player_lost(game, current_player):
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if not is_bot(current_player):
            if event.type == pygame.MOUSEMOTION:
                    if is_players_piece(SCREEN, event.pos, current_player.color): 
                        board_color = get_position(event.pos, game)
                        for piece in game.pieces_dict[current_player]:
                            if piece.position == board_color:
                                selected = piece
                                break

                        draw_board(game, SCREEN, game_piece=selected)
                        pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                        should_be_jump = game.get_all_jumps(current_player) != []
                        board_coor = get_position(event.pos,game)
                        if is_piece_moved(game, selected, board_coor, should_be_jump):
                            temp = current_player
                            current_player = next_player
                            next_player = temp
                            draw_board(game, SCREEN)
        else:
            move = current_player.choose_move(game.board, game.get_possible_moves(current_player))
            game.make_move(move)
            temp = current_player
            current_player = next_player
            next_player = temp
            draw_board(game, SCREEN)
   
    print(f"{next_player} WON!")
    pygame.quit()

def is_piece_moved(game,piece_to_move, selected_final_position, should_be_jump):
    """
    Checks if the piece is moved or not
    Input:
        piece_to_move (GamePiece) - the piece to move
        selected_final_position (tuple) - the final position of the piece
    Output:
        True - if the piece is moved to a valid location
        False - if the piece is not moved to a valid location
    """
    all_possible_moves = game.get_possible_jumps_for_piece(piece_to_move)
    if all_possible_moves == []:
        if should_be_jump:
            return False
        all_possible_moves = game.get_possible_moves_for_piece(piece_to_move)
    final_positions = list(move[1][-1] for move in all_possible_moves)

    i = -1
    for index, final_position in enumerate(final_positions):
        if final_position == selected_final_position:
            i = index
            break
    if i == -1:
        return False
    
    game.make_move(all_possible_moves[i])
    return True

def check_player_lost(game, current_player):
    """
    Checks if the player lost the game or not
    Input:
        current_player (Player) - a player whose turn it is
    Output:
        True - if the player has lost the game
        False - if the player has not lost the game
    """
    valid_moves = game.get_possible_moves(current_player)
    return valid_moves == []
                    
@click.command(name="checkers-tui")
@click.option('--player-1-type', default="Player One")
@click.option('--player-2-type', default="Player Two")
@click.option('--width', default=8)
@click.option('--rows-with-pieces', default=2)
def cmd(player_1_type, player_2_type, width, rows_with_pieces):
    """
    This is the command line interface for the Checkers TUI.

    Input:
        player_1_type (str) - type of player 1
        player_2_type (str) - type of player 2
        width (int) - width of the board
        rows_with_pieces (int) - number of rows with pieces
    """
    if player_1_type == "random-bot":
        player_1 = RandomBot("random-bot-1","Red")
    elif player_1_type == "smart-bot":
        player_1 = CheckersBot("smart-bot-1","Red")
    else:
        player_1 = Player(player_1_type, "Red")

    if player_2_type == "random-bot":
        player_2 = RandomBot("random-bot-2","Black")
    elif player_2_type == "smart-bot":
        player_2 = CheckersBot("smart-bot-2","Black")
    else:
        player_2 = Player(player_2_type, "Black")

    players = [player_1, player_2]
    game = Game(players, rows_with_pieces, width)

    play_checkers(game)

if __name__ == "__main__":
    cmd()





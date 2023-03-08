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

class GUIPlayer(Player):
    """
    Simple class to store information about a GUI player
    """
    def __init__(self, n: int, player_type: str, board: Board, color):
        """ Constructor
        Args:
            n: The player's number (1 or 2)
            player_type: "human", "random-bot", or "checkers-bot"
            board: The Checkers board
            color: The player's color
        """
        if player_type == "human":
            self.name = f"Player {n}"
            self.bot = None
        if player_type == "random-bot":
            self.name = f"Random Bot {n}"
            self.bot = RandomBot(str(n), color)
        elif player_type == "checkers-bot":
            self.name = f"Checkers Bot {n}"
            self.bot = CheckersBot(str(n), color)
        self.board = board
        self.color = color


def is_players_piece(surface, coordinates, player_pieces_color):
    '''
    Checks if the selected location stores the piece of a given player
    '''
    if player_pieces_color == "Red":
        if tuple(pygame.Surface.get_at(surface, coordinates)[:3]) == RED:
            return True
    if player_pieces_color == "Black":
        if tuple(pygame.Surface.get_at(surface, coordinates)[:3]) == BLACK:
            return True

def get_piece(board, coordinates):
    '''
    Finds and returns the piece (GamePiece) on the board given its coordinates
    '''
    x, y = coordinates
    piece = board.grid[x][y]
    return piece

def get_position(coordinates):
    '''
    Converts pixel coordinates into board position (row, column)
    '''
    x, y = coordinates
    square_width = WIDTH / 8
    square_height = HEIGHT / 8
    column = x // square_width 
    row = y // square_height
    column = int(column)
    row = int(row)
    position = (row, column)
    return position

def draw_board(board: Board, surface, game_piece = None) -> None:
    """ 
    Draws the current state of the board in the window
    Args:
        surface: Pygame surface to draw the board on
        board: The board to draw
    Returns: None
    """
    background = WHITE
    surface.fill(background)

    grid = board.grid 
    nrows = len(grid)
    ncols = len(grid[0])
    
    
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
        moves = Board.get_possible_moves_for_piece(board, game_piece)
        jumps = Board.get_possible_jumps(board, game_piece)

        if jumps is not None: 
            for jump in jumps:
                    row, col = jump
                    rect = (col * column_width, row * row_height, column_width, row_height)
                    pygame.draw.rect(surface, color= BLUE, rect = rect)

        if jumps is None:
            if moves is not None:
                for move in moves:
                    row, col = move
                    rect = (col * column_width, row * row_height, column_width, row_height)
                    pygame.draw.rect(surface, color= GREEN, rect = rect)
        
    # Draw the game pieces
    for i, row in enumerate(grid):
        for j, piece in enumerate(row):
            if piece is not None:
                if piece.player == "Red":
                    color = RED
                if piece.player == "Black":
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


class GUIPiece():
    """
    Simple class to 
    - store information about current player and selected piece to 
    perform the move, 
    - perform a valid move (jumps are prioritized)
    - switch the turn 
    - update the grid
    """
    def __init__(self, board: Board):
        """ Constructor
        Args:
            board: The Checkers board
        """
        self.board = board
        self.grid = board.grid
        self.selected_piece = None
        self.current_player = self.board.current_player
        self.gui_player = None

    def selected_square(self, coordinates):
        '''
        Selects a piece to move or jump. When the user chooses the final 
        position by clicking on the available square, calls move_piece() to 
        move the selected piece
        '''        
        if self.selected_piece is not None:
            jumps = Board.get_possible_jumps(self.board, self.selected_piece)
            moves = Board.get_possible_moves_for_piece(self.board, self.selected_piece)
            if jumps is not None:
                for jump in jumps:
                    if coordinates == jump:
                        self.move_piece(coordinates)
            elif moves is not None:
                for move in moves:
                    if coordinates == move:
                        self.move_piece(coordinates)
            self.selected_piece = None

        elif self.selected_piece is None:
            piece = get_piece(self.board, coordinates)
            if piece is not None: 
                jumps = Board.get_all_jumps(self.board, self.current_player)
                if piece.player == self.current_player:
                    if jumps is not None:
                        for jump in jumps:
                            if piece.position == jump[0].position:
                                self.selected_piece = piece
                    elif jumps is None:
                        self.selected_piece = piece


    def move_piece(self, final_pos):
        '''
        Moves the piece on the board. Calls change_player() to switch the turn
        after the move is performed
        '''
        initial_pos = self.selected_piece.position
        Board.perform_move(self.board, initial_pos, final_pos)
        draw_board(self.board, SCREEN)
        pygame.display.update()
        self.selected_piece = None
        self.change_player()


    def change_player(self):
        '''
        Switches the turn
        '''
        if self.board.current_player == "Black":
            self.board.current_player = "Red"
        elif self.board.current_player == "Red": 
            self.board.current_player = "Black"
        self.current_player = self.board.current_player
        return None


    def is_end(self):
        '''
        Checkes if the game has ended (condition: the current player does not 
        have any moves to perform, for example, if they have no game pieces left
        on the board)
        '''
        if Board.get_all_jumps(self.board, self.current_player) is None and \
        Board.get_possible_moves(self.board, self.current_player) is None:
            return True
        return False
    

def play_checkers(board: Board, players):
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
    draw_board(board, SCREEN)

    # The starting player is black
    board.current_player = "Black"
    gui_piece = GUIPiece(board)

    while not GUIPiece.is_end(gui_piece): 
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            for player in players:
                if player.color == board.current_player:
                    current = player

            if current.bot is None:
                if event.type == pygame.MOUSEMOTION:
                    if is_players_piece(SCREEN, event.pos, board.current_player): 
                        board_coor = get_position(event.pos)
                    
                        for piece in board.pieces_dictionary[board.current_player]:
                            if piece.position == board_coor:
                                selected = piece
                        
                        draw_board(board, SCREEN, selected)
                        pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    board_coor = get_position(event.pos)
                    GUIPiece.selected_square(gui_piece, board_coor)
            
            if current.bot is not None:
                move = current.choose_move(board)
                gui_piece.selected_piece = move[0]
                move_coor = move[1]
                GUIPiece.move_piece(gui_piece, move_coor)

    
    lost = board.current_player
    if lost == "Red":
        winner = "Black"
    else: 
        winner = "Red"
    
    for player in players:
        if player.color == winner:
            winner = player.name

    if winner is not None:
        print(f"The winner is {winner}!")
    else:
        print("It's a tie!")

    pygame.quit()
                    
@click.command(name="checkers-gui")

@click.option('--size', required=True, type=int,
              default=3)

@click.option('--player1',
              type=click.Choice(['human', 'random-bot', 'checkers-bot'], case_sensitive=False),
              default="human")

@click.option('--player2',
              type=click.Choice(['human', 'random-bot', 'checkers-bot'], case_sensitive=False),
              default="human")


def cmd(size, player1, player2):

    board = Board(size)

    player1 = GUIPlayer(1, player1, board, "Black")
    player2 = GUIPlayer(2, player2, board, "Red")

    players = [player1, player2]

    play_checkers(board, players)

if __name__ == "__main__":
    cmd()





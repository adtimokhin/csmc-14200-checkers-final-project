from src.board import Board
from src.game_piece import GamePiece
class Game:
    """
    Public attributes of this class:
        board: Board
        players: list[Player]
    """

    def __init__(self, players, number_populated_rows, width=8):
        self.players = players
        self.number_populated_rows = number_populated_rows
        self.width = width
        self.board = Board(number_populated_rows*2 + 2, width)
        self.pieces_dict = {}

        # Setting up the pieces_dict
        for player in self.players:
            self.pieces_dict[player] = []

        # Setting the board with pieces
        self.__populate_board()

    def get_possible_jumps(self, piece):
        """
        finds all the possible jumps of a given piece on the board
        :param piece
            piece for which we need to find jumps
        :returns
            list[(int, int)] - a list of tuples which represent the coordinates of jumps, or None
        """
        raise NotImplementedError

    def get_possible_moves(self, player):
        """
        finds possible moves for a given player
        :param player
            Player for whom possible moves are found
        :returns
            list[(piece, (int, int))] - list of tuples that show a piece and a possible move coordinate
            if jumps are possible returns only jump-moves
        """
        raise NotImplementedError

    def get_possible_moves_for_piece(self, piece):
        """
        finds possible moves for a given piece
        :param piece
            the specific game piece for which the moves are found
        :returns
            either list[(int,int)] which is a list of tuples of coordinates, representing moves,
            or None
        """
        raise NotImplementedError

    def get_all_jumps(self, player):
        """
        finds all possible jump-moves for a given player
        :param player
            Player for whom possible jumps are found
        :returns
            list[(piece, (int, int))] - list of all possible jump moves
            or None if no 'jump-moves' are found

        """
        raise NotImplementedError
    
    def __populate_board(self):

        """
        Populates the board with Game_Pieces accroding to the rules of checkers.
        """
        for row_num in range(self.number_populated_rows):
            start_pos = 1 if row_num % 2 == 0 else 0
            for col_num in range(start_pos,self.width, 2):
                # Placing game pieces to the grid of the board
                first_piece = GamePiece((row_num, col_num), self.players[0])
                self.board.place_piece(first_piece)

                second_piece = GamePiece(( len(self.board.grid) - row_num - 1, col_num), self.players[1])
                self.board.place_piece(second_piece)

                # Putting the pieces in the pieces_dict:
                self.pieces_dict[self.players[0]].append(first_piece)
                self.pieces_dict[self.players[1]].append(second_piece)



    def make_move(self, move):
        """
        Moves a Game_Piece from initial position to final position on the grid
        removes a Piece from the board if the 'jump-move' was performed
        :param initial_pos:
            (int, int) - represents the coordinates of the piece as (row, col)
        :param final_pos:
            (int, int) - represents the coordinates of the piece as (row, col)
        :returns
            None
        """
        piece = move[0]
        list_of_movements = move[1]
        for transposition in list_of_movements:
            self.board.move_piece(piece.position, transposition)



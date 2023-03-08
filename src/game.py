from src.board import Board
class Game:
    """
    Public attributes of this class:
        board: Board
        players: list[Player]
    """

    def __init__(self,   players: list, number_populated_rows, width=8):
        self.players = players
        self.board = Board(number_populated_rows*2 + 2, width)

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

    def make_move(self, initial_pos: tuple, final_pos: tuple):
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
        pass

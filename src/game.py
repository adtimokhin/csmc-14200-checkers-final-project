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

    def get_possible_moves_for_piece(self, piece):
        """
        finds possible moves for a given piece
        :param piece
            the specific game piece for which the moves are found
        :returns
            either list[(int,int)] which is a list of tuples of coordinates, representing moves,
            or None
        """
        player = piece.player
        direction = 1 if (self.players.index(player) % 2 == 0) else -1
        current_position = piece.position
        possible_move = []

        if self.board.is_empty_cell((current_position[0] + direction, current_position[1] + 1)):
            possible_move.append((piece, [(current_position[0] + direction, current_position[1] + 1)]))
        if self.board.is_empty_cell((current_position[0] + direction, current_position[1] - 1)):
            possible_move.append((piece, [(current_position[0] + direction, current_position[1] - 1)]))
        if piece.is_king:
            if self.board.is_empty_cell((current_position[0] - direction, current_position[1] + 1)):
                possible_move.append((piece, [(current_position[0] + direction, current_position[1] + 1)]))
            if self.board.is_empty_cell((current_position[0] + direction, current_position[1] - 1)):
                possible_move.append((piece, [(current_position[0] - direction, current_position[1] - 1)]))
        return possible_move

    def get_possible_jumps_for_piece(self, piece):
        """
        finds possible jumps for a given piece
        :param piece
            the specific game piece for which the jumps are found
        :returns
            either list[(int,int)] which is a list of tuples of coordinates, representing jumps,
            or None
        """
        unsorted_moves = self.get_all_jumps_moves(piece.position, piece)

        sorted_moves = []
        for unsorted_move in unsorted_moves:
            new_move = []
            while unsorted_move != []:
                new_move.append(unsorted_move[0])
                unsorted_move = unsorted_move[1]
            if new_move != []:
                sorted_moves.append(new_move)
        
        moves_formatted = []
        for move in sorted_moves:
            moves_formatted.append([piece, move])
        return moves_formatted

            
    def get_all_jumps_moves (self, start_pos, piece, blocked_pos=[]):
        player = piece.player
        direction = -1 if (self.players.index(player) % 2 == 0) else 1
        if piece.is_king:
            possible_pieces_moves = ((1, 1) , (1, -1), (-1, 1), (-1, -1))
        else:
            possible_pieces_moves = ((-1 * direction, -1 * direction), (-1 * direction, 1 * direction))

        possible_moves = []
        for coords in possible_pieces_moves:
                potential_final_pos = (coords[0] + start_pos[0], coords[1] + start_pos[1])
                if piece.is_king:
                    while self.board.is_empty_cell(potential_final_pos):
                        potential_final_pos = (coords[0] + potential_final_pos[0], coords[1] + potential_final_pos[1])

                if self.board.is_on_grid(potential_final_pos):
                    # If the final position contains enemy piece
                    if not self.board.is_empty_cell(potential_final_pos):
                        if self.board.grid[potential_final_pos[0]][potential_final_pos[1]].player!= player:

                            # We need to check if we can make a move in that direction over that piece
                            potential_jump_pos = (coords[0] + potential_final_pos[0] , coords[1] + potential_final_pos[1])
                            if self.board.is_empty_cell(potential_jump_pos):
                                if piece.is_king and potential_final_pos in blocked_pos:
                                    continue
                                # Add move to the list of possible moves
                                possible_moves.append((potential_jump_pos))
                                blocked_pos.append(potential_final_pos)
        if len(possible_moves) > 0:
            list_of_moves = []
            for move in possible_moves:
                if piece.is_king:
                    kol = self.get_all_jumps_moves(move, piece, blocked_pos=blocked_pos)
                else:
                    kol = self.get_all_jumps_moves(move, piece)
                if kol == []:
                    list_of_moves.append([move, []])
                for item in kol:
                    list_of_moves.append([move, item])
            return list_of_moves

        return possible_moves

    def get_possible_moves(self, player):
        """
        finds possible moves for a given player
        :param player
            Player for whom possible moves are found
        :returns
            list[(piece, [(int, int)])] - list of tuples that show a piece and a possible move coordinate
            if jumps are possible returns only jump-moves
        """
        list_to_return = self.get_all_jumps(player)
        if list_to_return != []:
            return list_to_return
        for piece in self.pieces_dict[player]:
            list_to_return += self.get_possible_moves_for_piece(piece)
        return list_to_return

    def get_all_jumps(self, player):
        """
        finds all possible jump-moves for a given player
        :param player
            Player for whom possible jumps are found
        :returns
            list[(piece, (int, int))] - list of all possible jump moves
            or None if no 'jump-moves' are found

        """
        list_to_return = []
        for piece in self.pieces_dict[player]:
            list_to_return += self.get_possible_jumps_for_piece(piece)
        return list_to_return
    
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
            self.board.move_piece(piece.position, transposition, self)



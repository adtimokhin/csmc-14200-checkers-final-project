from random import randint
from player import Player
from board import Board
from game import Game
from game_piece import GamePiece

from math import inf
# https://hobbylark.com/board-games/Checkers-Strategy-Tactics-How-To-Win - strategy source


class CheckersBot(Player):
    """
    CheckersBot is a child class of Player which with the simple heuristics suggests a move
    Public attributes:
        name: str  - name of the player, continuation of player interface
    Heuristics:
    1. Try to king with every possible opportunity
    2. Try to move so that the piece is not attacked
    3. Chose the longest jumps
    4. Move aggressively (closer to the enemy pieces but not such that they are attacked
    5. Don't move two back(flank) pieces if possible
    """
    def __init__(self, name: str, color: str):
        super().__init__(name=name, color=color)

    def choose_move(self, board: Board, possible_moves: list):
        """
        chooses the best possible move
        :param board: Board class instance: current game_board
        :return: tuple(GamePiece, tuple(int, int)):  a move in a move format specified in the design
        """

        valid_moves = possible_moves

        # checks if the returned moves are jump_moves by checking if position change
        # is larger than during a normal move
        if abs(valid_moves[0][0].position[0] - valid_moves[0][1][0][0]) +\
                abs(valid_moves[0][0].position[1] - valid_moves[0][1][0][1]) != 2:
            valid_moves = self.best_jump(valid_moves)
            king_moves = self.check_if_can_king(valid_moves, board.number_of_rows)

            if len(king_moves) != 0:
                # if we can king with the biggest jump, we do that
                return king_moves[randint(0, len(king_moves))]
            else:
                # if we can't king, then we perform the longest jump-move
                return valid_moves[randint(0, len(valid_moves))]

        else:
            # this logical block is responsible for choosing the best non-jump move
            king_moves = self.check_if_can_king(valid_moves, board.number_of_cols)

            if len(king_moves) != 0:
                # checks if we can turn a pice into king with one of the moves
                return king_moves[randint(0, len(king_moves)-1)]
            safe_moves = self.check_if_danger(valid_moves, board)

            # checks if it possible to make a move without loosing a piece
            if len(safe_moves) != 0:
                # if it is perform the most aggressive of the safe moves
                valid_moves = self.aggressive_moves(safe_moves, board)
            else:
                # if not perform the most aggressive move which looses a piece
                valid_moves = self.aggressive_moves(valid_moves, board)

            non_defensive_moves = self.check_if_back_pieces(valid_moves, board.number_of_rows)

            # checks if we can make a move without using two defensive pieces
            if len(non_defensive_moves) == 0:
                return valid_moves[randint(0, len(valid_moves))]
            else:
                return non_defensive_moves[randint(0, len(non_defensive_moves)-1)]

    def aggressive_moves(self, valid_moves: list, board: Board):
        """
        picks the most aggressive move, by choosing the move which minimizes distance to all of the enemy pieces
        :param valid_moves:
        :param board: Board class instance: current game_board
        :return: list(moves): list of moves which are the best by given metric
        """

        best_moves = []
        lowest_distance = inf
        name_of_the_opponent = None

        for move in valid_moves:

            coordinates_of_move = move[1][-1]
            cumulative_linear_distance = 0

            for row in board.grid:
                for piece in row:
                    if piece is None:
                        pass
                    else:
                        # calculates sum of squared linear distnaces to every enemy pice
                        cumulative_linear_distance += (coordinates_of_move[0] - piece.position[0])**2 + \
                                                      (coordinates_of_move[1] - piece.position[1])**2

                        if cumulative_linear_distance == lowest_distance:
                            # if the distance is the same to enemy pieces, this move is one of the most aggressive
                            best_moves.append(move)
                        elif cumulative_linear_distance < lowest_distance:
                            # if the distance is smaller than for other moves this move is the most aggressive
                            best_moves.append(move)
        return best_moves

    def check_if_back_pieces(self, valid_moves: list, row_num: int):
        """
        removes defensive pieces from the valid moves
        :param valid_moves: list of valid moves
        :param board_size: int: length of the side of the board
        :return: list[moves]: list of all moves that do not involve back pieces
        """
        best_moves = []
        for move in valid_moves:
            if not move[0].is_king:
                piece_position = move[0].position
                if not (piece_position in [(1, 0), (5, 0), (0, row_num-1), (4, row_num-1)]):
                    best_moves.append(move)
        return best_moves

    def check_if_danger(self, valid_moves: list, board: Board):
        """
        returns all the moves that do not put the piece in danger of being captured
        :param valid_moves: list of valid moves
        :param board: Board: game board which is currently played
        :return: list of all moves that are not loosing a piece
        """

        best_moves = []
        current_player = valid_moves[0][0].player

        for move in valid_moves:

            coordinates = move[1][-1]

            if coordinates[1] in (0, board.number_of_cols-1) or coordinates[0] in (0, board.number_of_rows-1):
                # if the move moves to the edge it is a safe move
                best_moves.append(move)
            else:
                # if it is not an edge move we have to check if it is safe to make this move
                validity = True
                diagonals = [(board.grid[coordinates[0]+1][coordinates[1]+1], board.grid[coordinates[0]-1][coordinates[1]-1]),
                             (board.grid[coordinates[0]+1][coordinates[1]-1], board.grid[coordinates[0]-1][coordinates[1]+1])]

                for diagonal in diagonals:
                    # diagonal is a tuple of two objects that are placed on the squares
                    # adjacent to the square the move wants us to move
                    # and are on the same diagonal
                    # if one square on the diagonal is empty and one has the enemy piece
                    # then the moving piece can be captured and hence the move is
                    # disqualified as a safe move
                    if diagonal[0] != None:
                        if diagonal[1] is None and diagonal[0].player != current_player:
                            validity = False
                            break

                    if diagonal[1] != None:
                        if diagonal[0] is None and diagonal[1].player != current_player:
                            validity = False
                            break

                if validity:
                    best_moves.append(move)

        return best_moves

    def best_jump(self, valid_moves: list):
        """
        Out of all jump moves chooses the farthest jump-move (the one which takes the most pieces)
        :param valid_moves: list of valid moves
        :return: list of all jumps that capture maximum amount of pieces
        """
        best_moves = []
        biggest_number_of_jumps = 0
        for move in valid_moves:
            if len(move[1]) == biggest_number_of_jumps:
                best_moves.append(move)
            elif len(move[1]) > biggest_number_of_jumps:
                best_moves = [move]
                biggest_number_of_jumps = len(move[1])
            else:
                pass
        return best_moves

    def check_if_can_king(self, valid_moves: list, number_of_rows: int):
        """
        Checks if we can turn a piece into a king with one of the moves
        :param valid_moves: list of valid moves
        :param number_of_rows: int: length of the vertical side of the board
        :return: list of all moves that turn a piece into a king
        """
        best_moves = []
        for move in valid_moves:
            if not move[0].is_king:
                if move[1][-1] in [0, number_of_rows-1]:
                    best_moves.append(move)
        return best_moves


class RandomBot(Player):
    """
    A bot that is able to make random moves, made for the tests
    Public attributes:
        name: str: name that is also a parameter of a parent class
    """
    def __init__(self, name: str, color: str):
        super().__init__(name=name, color=color)

    def choose_move(self, board, possible_moves):
        """
        Randomly chooses a move
        :param board: Board class instance: current game_board
        :return: tuple(GamePiece, tuple(int, int)): a tuple in a move format specified in the design
        """
        return possible_moves[randint(0, len(possible_moves)-1)]

def main():
        player_1 = RandomBot("Player 1", "white")
        player_2 = RandomBot("Player 2", "black")
        players = [player_1, player_2]
        game = Game(players, 2, 8)
        test_board = Board(10, 10)
        game.board = test_board
        piece_1 = GamePiece((0, 0), player_1)
        piece_2 = GamePiece((1, 1), player_2)
        piece_3 = GamePiece((3, 3), player_2)
        piece_4 = GamePiece((1, 3), player_2)
        piece_5 = GamePiece((3, 1), player_2)
        game.pieces_dict[player_1] = [piece_1]
        game.pieces_dict[player_2] = [piece_2, piece_3, piece_4, piece_5]
        game.board.place_piece(piece_1)
        game.board.place_piece(piece_2)
        game.board.place_piece(piece_3)
        game.board.place_piece(piece_4)
        game.board.place_piece(piece_5)
        moves = game.get_possible_moves(player_1)
        print(player_1.choose_move(game.board, moves))
        print(game.board.grid)

if __name__ == "__main__":
    main()

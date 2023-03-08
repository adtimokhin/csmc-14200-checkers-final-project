from game import Game
from player import Player
from game_piece import GamePiece
from board import Board

def main():
    player_1 = Player("Player 1", "white")
    player_2 = Player("Player 2", "black")
    players = [player_1, player_2]
    game = Game(players, 2, 5)

    player_1_pieces = game.pieces_dict[player_1]
    player_2_pieces = game.pieces_dict[player_2]


    for piece in player_1_pieces:
        game.board.remove_piece(piece)

    for piece in player_2_pieces:
        game.board.remove_piece(piece)



    piece_2 = GamePiece((0,0), player_1)
    piece_2.is_king = True
    game.pieces_dict[player_1] = game.pieces_dict[player_1] + [piece_2]
    game.board.place_piece(piece_2)

    new_piece_1 = GamePiece( (1, 1), player_2)
    game.pieces_dict[player_2] = game.pieces_dict[player_2] + [new_piece_1]
    game.board.place_piece(new_piece_1)

    new_piece_1 = GamePiece( (3, 3), player_2)
    game.pieces_dict[player_2] = game.pieces_dict[player_2] + [new_piece_1]
    game.board.place_piece(new_piece_1)

    print(game.board.grid)

    print(game.get_possible_jumps_for_piece(game.board.grid[0][0]))



if __name__ == '__main__':
    main()
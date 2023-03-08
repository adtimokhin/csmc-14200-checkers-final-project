from game import Game
from player import Player
from board import Board
from game_piece import GamePiece

def main():
    player_1 = Player("Player 1", "white")
    player_2 = Player("Player 2", "black")
    players = [player_1, player_2]
    game = Game(players, 2, 8)
    test_board = Board(5, 5)
    game.board = test_board
    piece_1 = GamePiece((0, 0), player_1)
    piece_2 = GamePiece((1, 1), player_2)
    piece_3 = GamePiece((3, 3), player_2)
    game.board.place_piece(piece_1)
    game.board.place_piece(piece_2)
    game.board.place_piece(piece_3)
    print(game.board.grid)
    move = (piece_1, [(2,2), (4,4)])
    game.make_move(move)
    print(game.board.grid)



if __name__ == '__main__':
    main()
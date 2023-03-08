import pytest
from src.game import Game
from src.player import Player
from src.board import Board
from src.game_piece import GamePiece
from src.bot import CheckersBot, RandomBot


def test_checkers_1():
    """asserts that out of two moves the bot chooses the move to king during jump situation"""
    player_1 = CheckersBot("Player 1", "white")
    player_2 = RandomBot("Player 2", "black")
    players = [player_1, player_2]
    game = Game(players, 2, 8)
    test_board = Board(11, 11)
    game.board = test_board
    piece_0 = GamePiece((1, 1), player_1)
    piece_1 = GamePiece((8, 8), player_1)
    piece_2 = GamePiece((9, 9), player_2)
    piece_3 = GamePiece((2, 2), player_2)
    game.pieces_dict[player_1] = [piece_1, piece_0]
    game.pieces_dict[player_2] = [piece_3, piece_2]
    game.board.place_piece(piece_0)
    game.board.place_piece(piece_1)
    game.board.place_piece(piece_2)
    game.board.place_piece(piece_3)
    chosen = player_1.choose_move(test_board, game.get_possible_moves(player_1))
    assert chosen == [piece_1, [(10, 10)]]


def test_checkers_2():
    """asserts that out of two moves the bot chooses the move to king during jump situation"""
    player_1 = CheckersBot("Player 1", "white")
    player_2 = RandomBot("Player 2", "black")
    players = [player_1, player_2]
    game = Game(players, 2, 8)
    test_board = Board(11, 11)
    game.board = test_board
    piece_0 = GamePiece((1, 1), player_1)
    piece_1 = GamePiece((9, 9), player_1)
    game.pieces_dict[player_1] = [piece_1, piece_0]
    game.board.place_piece(piece_0)
    game.board.place_piece(piece_1)
    chosen = player_1.choose_move(test_board, game.get_possible_moves(player_1))
    assert chosen == [piece_1, [(10, 10)]] or chosen == [piece_1, [(8, 10)]]


def test_checkers_3():
    """asserts that out of two moves the bot chooses the move to king during no-jump situation"""
    player_1 = CheckersBot("Player 1", "white")
    player_2 = RandomBot("Player 2", "black")
    players = [player_1, player_2]
    game = Game(players, 2, 8)
    test_board = Board(11, 11)
    game.board = test_board
    piece_0 = GamePiece((8, 8), player_2)
    piece_1 = GamePiece((6, 6), player_1)

    game.pieces_dict[player_1] = [piece_1]
    game.pieces_dict[player_2] = [piece_0]
    game.board.place_piece(piece_0)
    game.board.place_piece(piece_1)
    chosen = player_1.choose_move(test_board, game.get_possible_moves(player_1))
    assert chosen == (piece_1, [(7, 5)])


def test_checkers_4():
    """asserts if the best (longest) jump is chosen"""
    player_1 = CheckersBot("Player 1", "white")
    player_2 = RandomBot("Player 2", "black")
    players = [player_1, player_2]
    game = Game(players, 2, 8)
    test_board = Board(11, 11)
    game.board = test_board
    piece_0 = GamePiece((6, 6), player_1)
    piece_1 = GamePiece((7, 7), player_2)
    piece_2 = GamePiece((7, 5), player_2)
    piece_3 = GamePiece((9, 3), player_2)
    game.pieces_dict[player_1] = [piece_0]
    game.pieces_dict[player_2] = [piece_3, piece_2, piece_1]
    game.board.place_piece(piece_0)
    game.board.place_piece(piece_1)
    game.board.place_piece(piece_2)
    game.board.place_piece(piece_3)
    chosen = player_1.choose_move(test_board, game.get_possible_moves(player_1))
    assert chosen == [piece_1, [(8, 4), (10, 2)]]
import pytest
from unittest.mock import Mock

from board import Board
from player import Player
from bot import CheckersBot, RandomBot
from tui import TUIGame, is_bot



def test_should_say_is_bot_when_player_is_random_bot():
    simple_bot = RandomBot("simple_bot_name")
    assert is_bot(simple_bot)

def test_should_say_is_bot_when_player_is_checkers_bot():
    simple_bot = CheckersBot("checkers_bot_name")
    assert is_bot(simple_bot)

def test_should_say_is_not_bot_when_player_is_real_player():
    player = Player("name")
    assert not is_bot(player)


player_1 = Player("Player_1")
player_2 = Player("Player_2")

mock_board = Mock()
test_TUIGame = TUIGame([player_1, player_2], mock_board)

def test_check_player_lost_the_game():
    # Case 1 - Player has no more moves and thus must loose
    mock_board.valid_moves.return_value = []
    assert test_TUIGame.check_player_lost(player_1)

    # Case 2 - Player has moves and thus has not yet lost
    mock_board.valid_moves.return_value = [(1,2)]
    assert not test_TUIGame.check_player_lost(player_1)

def test_is_draw():
    mock_tui = Mock()
    real_tui = test_TUIGame.tui

    #Setting TUI to a mock since in an automated test we cannot test user input
    test_TUIGame.tui = mock_tui

    #Case 1 - Both players entered agreed for a draw
    mock_tui.get_bool_input.return_value = True
    assert test_TUIGame.is_draw(player_1, player_2)

    # Case 2 - Both players do not agree for a draw
    mock_tui.get_bool_input.return_value = False
    assert not test_TUIGame.is_draw(player_1, player_2)

    #Setting TUI back to a real TUI
    test_TUIGame.tui = real_tui
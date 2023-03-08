import pytest
from unittest.mock import Mock

from player import Player
from game import Game
from bot import CheckersBot, RandomBot
from tui import TUIGame, is_bot



def test_should_say_is_bot_when_player_is_random_bot():
    simple_bot = RandomBot("simple_bot_name", "color")
    assert is_bot(simple_bot)

def test_should_say_is_bot_when_player_is_checkers_bot():
    simple_bot = CheckersBot("checkers_bot_name", "color")
    assert is_bot(simple_bot)

def test_should_say_is_not_bot_when_player_is_real_player():
    player = Player("name", "color")
    assert not is_bot(player)


player_1 = Player("ddd", "")
player_2 = Player("eee", "d")
mock_game = Game([player_1,player_2], 2)
test_TUIGame = TUIGame(mock_game)

def test_is_draw():
    mock_tui = Mock()

    #Setting TUI to a mock since in an automated test we cannot test user input
    test_TUIGame.tui = mock_tui

    #Case 1 - Both players entered agreed for a draw
    mock_tui.get_bool_input.return_value = True
    assert test_TUIGame.is_draw(player_1, player_2)

    # Case 2 - Both players do not agree for a draw
    mock_tui.get_bool_input.return_value = False
    assert not test_TUIGame.is_draw(player_1, player_2)

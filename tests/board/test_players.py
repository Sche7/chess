from board.players import Player, ChessPlayers
from chess_pieces import Color


def test_player_to_player_comparison():
    """
    Test that Player instance can
    be compared with another Player instance
    """
    player_1 = Player(Color.white)
    player_2 = Player(Color.black)
    player_3 = Player(Color.white)
    assert player_1 == player_3
    assert player_1 != player_2


def test_player_to_string_comparison():
    """
    Test that Player instances can
    be compared with string
    """
    player = Player(Color.white)
    assert player == 'white'
    assert player != 'black'


def test_chess_players():
    """
    Test that ChessPlayer switch_turn method
    works as expected.
    """
    chess_players = ChessPlayers()

    assert chess_players.active_player == 'white'
    assert chess_players.inactive_player == 'black'

    chess_players.switch_turn()
    assert chess_players.active_player == 'black'
    assert chess_players.inactive_player == 'white'

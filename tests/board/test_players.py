from src.board.players import ChessPlayers, Player
from src.pieces import Color, Group
from src.pieces.pawn import Pawn


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
    assert player == "white"
    assert player != "black"


def test_add_remove_chess_piece():
    """
    Test that a chess piece can be added
    to Player instance.
    """
    player_1 = Player(Color.white)
    pawn = Pawn(position=(0, 0), piece_nr=1, group=Group.lower, color=Color.white)

    # See that chess pieces can be added
    player_1.add_chess_piece(pawn)
    assert len(player_1.chess_pieces["Pawn"]) == 1

    # See that chess pieces can be removed
    player_1.remove_chess_piece(pawn.name, pawn.id)
    assert len(player_1.chess_pieces["Pawn"]) == 0


def test_kill_chess_piece():
    """
    Test that Player.kill kills chess piece as expected
    """
    player_1 = Player(Color.white)
    pawn = Pawn(position=(0, 0), piece_nr=1, group=Group.lower, color=Color.white)

    # See that pawn was added
    player_1.add_chess_piece(pawn)
    assert len(player_1.chess_pieces["Pawn"]) == 1, "Expected 1 pawn"

    # See that chess piece is killed as expected
    player_1.kill(chess_piece_name=pawn.name, chess_piece_id=pawn.id)
    assert player_1.chess_pieces[pawn.name][pawn.id].status == 0


def test_chess_players():
    """
    Test that ChessPlayer switch_turn method
    works as expected.
    """
    chess_players = ChessPlayers()

    # See that white starts as active player
    # and black starts as inactive player
    assert chess_players.active_player == "white"
    assert chess_players.inactive_player == "black"

    # See switch turn works
    chess_players.switch_turn()
    assert chess_players.active_player == "black"
    assert chess_players.inactive_player == "white"

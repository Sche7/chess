import pytest
from board.engine import Engine


@pytest.mark.parametrize("expect_protectable", [True, False])
def test_checkmate_kill_threat(config_path, expect_protectable):
    """
    Test that there is no checkmate if threat can be killed
    """
    engine = Engine(config_path)

    if expect_protectable:
        # Include bishop to make king 'protectable'
        game_state = [
            [12, 7, 0, 0, 0, 10, 0, 0],
            [0, 0, 0, 2, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [2, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ]
    else:
        # Do not include bishop to make king 'unprotectable'
        game_state = [
            [12, 7, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 2, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [2, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ]

    _ = engine.initiate_board_from_array(game_state=game_state)

    # See that black king is threatened
    threats = engine._threats_to_the_king(player="black")
    assert len(threats) > 0

    # See that black king cannot move away from threat
    assert engine._king_cannot_move(player="black")

    if expect_protectable:
        # See that bishop can protect king by killing the threat
        assert not engine._cannot_protect_king(player="black")
    else:
        # See that king cannot be protected
        assert engine._cannot_protect_king(player="black")


@pytest.mark.parametrize("expect_protectable", [True, False])
def test_checkmate_intercept_attack(config_path, expect_protectable):
    """
    Test that there is no checkmate if a unit can intercept
    the threat attack
    2: White rook
    7: Black Pawn
    8: Black rook
    12: Black king
    """
    engine = Engine(config_path)
    if expect_protectable:
        # Include rook to make king 'protectable'
        game_state = [
            [12, 7, 0, 0, 0, 0, 0, 0],
            [0, 8, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 8, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [2, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ]
    else:
        # Include pawn that cannot intercept,
        # so king is not 'protectable'
        game_state = [
            [12, 7, 0, 0, 0, 0, 0, 0],
            [0, 0, 2, 0, 8, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [2, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ]

    _ = engine.initiate_board_from_array(game_state=game_state)

    # See that black king is threatened
    threats = engine._threats_to_the_king(player="black")
    assert len(threats) > 0

    # See that black king cannot move away from threat
    assert engine._king_cannot_move(player="black")

    if expect_protectable:
        # See that rook can protect king by killing the threat
        assert not engine._cannot_protect_king(
            player="black"
        ), "Expected king to be protectable"
    else:
        # See that king cannot be protected
        assert engine._cannot_protect_king(
            player="black"
        ), "Expected king to be unprotectable"


@pytest.mark.parametrize("expect_checkmate", [True, False])
def test_checkmate(config_path, expect_checkmate):
    """
    Test that checkmate works
    2: White rook
    7: Black Pawn
    8: Black rook
    12: Black king
    """
    engine = Engine(config_path)
    if expect_checkmate:
        # Set game state where we expect checkmate
        game_state = [
            [12, 7, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 2, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [2, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ]
    else:
        # Set game state where we do not expect checkmate
        game_state = [
            [12, 7, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [2, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ]

    _ = engine.initiate_board_from_array(game_state=game_state)

    # See that black king is threatened
    threats = engine._threats_to_the_king(player="black")
    assert len(threats) > 0

    if expect_checkmate:
        assert engine.is_checkmate(player="black"), "Expected checkmate game state"
    else:
        assert not engine.is_checkmate(
            player="black"
        ), "Expected no checkmate game state"

import pytest

from chess_pieces.pawn import Pawn
from chess_pieces.schema import Color, Group


# Test lower pawn moves from position (1, 1)
def test_pawn_moves_lower_1_1():
    expected_applied_moves = [
        (0, 2), (1, 2), (2, 2), (1, 3)
    ]
    pawn = Pawn(
        position=(1, 1),
        group=Group.lower,
        color=Color.white
    )

    # Make sure grid size is 8 when testing
    pawn.set_grid_size(size=8)

    moves = pawn.get_applied_moves()
    for move in moves:
        assert move in expected_applied_moves
    assert len(expected_applied_moves) == len(moves)


# Test lower pawn moves from position (4, 5)
def test_pawn_moves_lower_4_5():
    expected_applied_moves = [
        (3, 6), (4, 6), (5, 6), (4, 7)
    ]
    pawn = Pawn(
        position=(4, 5),
        group=Group.lower,
        color=Color.white
    )

    # Make sure grid size is 8 when testing
    pawn.set_grid_size(size=8)

    moves = pawn.get_applied_moves()
    for move in moves:
        assert move in expected_applied_moves
    assert len(expected_applied_moves) == len(moves)


# Test lower pawn moves from position (7, 7)
def test_pawn_moves_lower_7_7():
    pawn = Pawn(
        position=(7, 7),
        group=Group.lower,
        color=Color.white
    )

    # Make sure grid size is 8 when testing
    pawn.set_grid_size(size=8)

    moves = pawn.get_applied_moves()
    assert 0 == len(moves)


# Test upper pawn moves from position (1, 1)
def test_pawn_moves_upper_1_1():
    expected_applied_moves = [
        (0, 0), (1, 0), (2, 0)
    ]
    pawn = Pawn(
        position=(1, 1),
        group=Group.upper,
        color=Color.black
    )

    # Make sure grid size is 8 when testing
    pawn.set_grid_size(size=8)

    moves = pawn.get_applied_moves()
    for move in moves:
        assert move in expected_applied_moves
    assert len(expected_applied_moves) == len(moves)


# Test upper pawn moves from position (4, 5)
def test_pawn_moves_upper_4_5():
    expected_applied_moves = [
        (3, 4), (4, 4), (5, 4), (4, 3)
    ]
    pawn = Pawn(
        position=(4, 5),
        group=Group.upper,
        color=Color.black
    )

    # Make sure grid size is 8 when testing
    pawn.set_grid_size(size=8)

    moves = pawn.get_applied_moves()
    for move in moves:
        assert move in expected_applied_moves
    assert len(expected_applied_moves) == len(moves)


# Test upper pawn moves from position (8, 8)
def test_pawn_moves_upper_7_7():
    expected_applied_moves = [
        (6, 6), (7, 6), (7, 5)
    ]
    pawn = Pawn(
        position=(7, 7),
        group=Group.upper,
        color=Color.black
    )

    # Make sure grid size is 8 when testing
    pawn.set_grid_size(size=8)

    moves = pawn.get_applied_moves()
    for move in moves:
        assert move in expected_applied_moves
    assert len(expected_applied_moves) == len(moves)


def test_pawn_moves_exception():
    pawn = Pawn(
        position=(8, 8),
        group='not working',
        color=Color.black
    )

    # Make sure grid size is 8 when testing
    pawn.set_grid_size(size=8)

    with pytest.raises(ValueError) as e:
        pawn.moves()
        assert 'Group [not working] is not supported' == str(e.value)

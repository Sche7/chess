from chess_pieces.pawn import Pawn
from chess_pieces.schema import Color, Group


# Test lower pawn moves from position (1, 1)
def test_pawn_moves_lower_1_1():
    expected_applied_moves = [
        (0, 2),
        (1, 2),
        (2, 2)
    ]
    pawn = Pawn(
        position=(1, 1),
        group=Group.lower,
        color=Color.white
    )
    moves = pawn.get_applied_moves()
    for move in moves:
        assert move in expected_applied_moves
    assert len(expected_applied_moves) == len(moves)


# Test lower pawn moves from position (4, 5)
def test_pawn_moves_lower_4_5():
    expected_applied_moves = [
        (3, 6),
        (4, 6),
        (5, 6)
    ]
    pawn = Pawn(
        position=(4, 5),
        group=Group.lower,
        color=Color.white
    )
    moves = pawn.get_applied_moves()
    for move in moves:
        assert move in expected_applied_moves
    assert len(expected_applied_moves) == len(moves)


# Test lower pawn moves from position (8, 8)
def test_pawn_moves_lower_8_8():
    expected_applied_moves = [
        (7, 9),
        (8, 9),
        (9, 9)
    ]
    pawn = Pawn(
        position=(8, 8),
        group=Group.lower,
        color=Color.white
    )
    moves = pawn.get_applied_moves()
    for move in moves:
        assert move in expected_applied_moves
    assert len(expected_applied_moves) == len(moves)


# Test upper pawn moves from position (1, 1)
def test_pawn_moves_upper_1_1():
    expected_applied_moves = [
        (0, 0),
        (1, 0),
        (2, 0)
    ]
    pawn = Pawn(
        position=(1, 1),
        group=Group.upper,
        color=Color.black
    )
    moves = pawn.get_applied_moves()
    for move in moves:
        assert move in expected_applied_moves
    assert len(expected_applied_moves) == len(moves)


# Test upper pawn moves from position (4, 5)
def test_pawn_moves_upper_4_5():
    expected_applied_moves = [
        (3, 4),
        (4, 4),
        (5, 4)
    ]
    pawn = Pawn(
        position=(4, 5),
        group=Group.upper,
        color=Color.black
    )
    moves = pawn.get_applied_moves()
    for move in moves:
        assert move in expected_applied_moves
    assert len(expected_applied_moves) == len(moves)


# Test upper pawn moves from position (8, 8)
def test_pawn_moves_upper_8_8():
    expected_applied_moves = [
        (7, 7),
        (8, 7),
        (9, 7)
    ]
    pawn = Pawn(
        position=(8, 8),
        group=Group.upper,
        color=Color.black
    )
    moves = pawn.get_applied_moves()
    for move in moves:
        assert move in expected_applied_moves
    assert len(expected_applied_moves) == len(moves)

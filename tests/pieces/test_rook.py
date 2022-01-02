from chess_pieces.rook import Rook
from chess_pieces.schema import Color, Group


# Test lower rook moves from position (0, 0)
def test_pawn_rook_lower_0_0():
    expected_applied_moves = [
        (0, 1), (0, 2), (0, 3),
        (0, 4), (0, 5), (0, 6),
        (0, 7), (1, 0), (2, 0),
        (3, 0), (4, 0), (5, 0),
        (6, 0), (7, 0)
    ]

    rook = Rook(
        position=(0, 0),
        piece_nr=2,
        group=Group.lower,
        color=Color.white
    )

    # Make sure grid size is 8 when testing
    rook.set_grid_size(size=8)

    moves = rook.get_applied_moves()
    for move in moves:
        assert move in expected_applied_moves
    assert len(expected_applied_moves) == len(moves)


# Test lower rook moves from position (4, 4)
def test_pawn_rook_lower_4_4():
    expected_applied_moves = [
        (4, 0), (4, 1), (4, 2),
        (4, 3), (4, 5), (4, 6),
        (4, 7), (0, 4), (1, 4),
        (2, 4), (3, 4), (5, 4),
        (6, 4), (7, 4)
    ]
    rook = Rook(
        position=(4, 4),
        piece_nr=2,
        group=Group.lower,
        color=Color.white
    )

    # Make sure grid size is 8 when testing
    rook.set_grid_size(size=8)

    moves = rook.get_applied_moves()
    for move in moves:
        assert move in expected_applied_moves
    assert len(expected_applied_moves) == len(moves)


# Test lower rook moves from position (7, 7)
def test_pawn_rook_lower_7_7():
    expected_applied_moves = [
        (7, 0), (7, 1), (7, 2),
        (7, 3), (7, 4), (7, 5),
        (7, 6), (0, 7), (1, 7),
        (2, 7), (3, 7), (4, 7),
        (5, 7), (6, 7)
    ]
    rook = Rook(
        position=(7, 7),
        piece_nr=2,
        group=Group.lower,
        color=Color.white
    )

    # Make sure grid size is 8 when testing
    rook.set_grid_size(size=8)

    moves = rook.get_applied_moves()
    for move in moves:
        assert move in expected_applied_moves
    assert len(expected_applied_moves) == len(moves)

from chess_pieces.bishop import Bishop
from chess_pieces.schema import Color, Group


# Test lower rook moves from position (0, 0)
def test_pawn_rook_lower_0_0():
    expected_applied_moves = [
        (1, 1), (2, 2), (3, 3),
        (4, 4), (5, 5), (6, 6),
        (7, 7)
    ]

    rook = Bishop(
        position=(0, 0),
        group=Group.lower,
        color=Color.white
    )
    moves = rook.get_applied_moves()
    for move in moves:
        assert move in expected_applied_moves
    assert len(expected_applied_moves) == len(moves)


# Test lower rook moves from position (4, 4)
def test_pawn_rook_lower_4_4():
    expected_applied_moves = [
        (0, 0), (1, 1), (2, 2),
        (3, 3), (5, 5), (6, 6),
        (7, 7), (1, 7), (2, 6),
        (3, 5), (5, 3), (6, 2),
        (7, 1)
    ]
    rook = Bishop(
        position=(4, 4),
        group=Group.lower,
        color=Color.white
    )
    moves = rook.get_applied_moves()
    for move in moves:
        assert move in expected_applied_moves
    assert len(expected_applied_moves) == len(moves)
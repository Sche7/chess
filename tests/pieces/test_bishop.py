from src.pieces.bishop import Bishop
from src.pieces.schema import Color, Group


# Test lower bishop moves from position (0, 0)
def test_pawn_bishop_lower_0_0():
    expected_applied_moves = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)]

    bishop = Bishop(position=(0, 0), piece_nr=4, group=Group.lower, color=Color.white)

    # Make sure grid size is 8 when testing
    bishop.set_grid_size(size=8)

    moves = bishop.get_applied_moves()
    for move in moves:
        assert move in expected_applied_moves
    assert len(expected_applied_moves) == len(moves)


# Test lower bishop moves from position (4, 4)
def test_pawn_bishop_lower_4_4():
    expected_applied_moves = [
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3),
        (5, 5),
        (6, 6),
        (7, 7),
        (1, 7),
        (2, 6),
        (3, 5),
        (5, 3),
        (6, 2),
        (7, 1),
    ]
    bishop = Bishop(position=(4, 4), piece_nr=4, group=Group.lower, color=Color.white)

    # Make sure grid size is 8 when testing
    bishop.set_grid_size(size=8)

    moves = bishop.get_applied_moves()
    for move in moves:
        assert move in expected_applied_moves
    assert len(expected_applied_moves) == len(moves)


# Test lower bishop moves from position (7, 7)
def test_pawn_bishop_lower_7_7():
    expected_applied_moves = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)]

    bishop = Bishop(position=(7, 7), piece_nr=4, group=Group.lower, color=Color.white)

    # Make sure grid size is 8 when testing
    bishop.set_grid_size(size=8)

    moves = bishop.get_applied_moves()
    for move in moves:
        assert move in expected_applied_moves
    assert len(expected_applied_moves) == len(moves)

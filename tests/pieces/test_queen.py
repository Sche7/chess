from src.pieces.queen import Queen
from src.pieces.schema import Color, Group


# Test lower queen moves from position (0, 0)
def test_queen_moves_lower_0_0():
    expected_diagonal_moves = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)]

    expected_straight_moves = [
        (0, 1),
        (0, 2),
        (0, 3),
        (0, 4),
        (0, 5),
        (0, 6),
        (0, 7),
        (1, 0),
        (2, 0),
        (3, 0),
        (4, 0),
        (5, 0),
        (6, 0),
        (7, 0),
    ]

    expected_applied_moves = expected_diagonal_moves + expected_straight_moves

    queen = Queen(position=(0, 0), piece_nr=5, group=Group.lower, color=Color.white)

    # Make sure grid size is 8 when testing
    queen.set_grid_size(size=8)

    moves = queen.get_applied_moves()
    for move in moves:
        assert move in expected_applied_moves
    assert len(expected_applied_moves) == len(moves)


# Test lower queen moves from position (4, 4)
def test_queen_moves_lower_4_4():
    expected_diagonal_moves = [
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

    expected_straight_moves = [
        (4, 0),
        (4, 1),
        (4, 2),
        (4, 3),
        (4, 5),
        (4, 6),
        (4, 7),
        (0, 4),
        (1, 4),
        (2, 4),
        (3, 4),
        (5, 4),
        (6, 4),
        (7, 4),
    ]

    expected_applied_moves = expected_diagonal_moves + expected_straight_moves

    queen = Queen(position=(4, 4), piece_nr=5, group=Group.lower, color=Color.white)

    # Make sure grid size is 8 when testing
    queen.set_grid_size(size=8)

    moves = queen.get_applied_moves()
    for move in moves:
        assert move in expected_applied_moves
    assert len(expected_applied_moves) == len(moves)


# Test lower queen moves from position (7, 7)
def test_queen_moves_lower_7_7():
    expected_diagonal_moves = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)]

    expected_straight_moves = [
        (7, 0),
        (7, 1),
        (7, 2),
        (7, 3),
        (7, 4),
        (7, 5),
        (7, 6),
        (0, 7),
        (1, 7),
        (2, 7),
        (3, 7),
        (4, 7),
        (5, 7),
        (6, 7),
    ]

    expected_applied_moves = expected_diagonal_moves + expected_straight_moves

    queen = Queen(position=(7, 7), piece_nr=5, group=Group.lower, color=Color.white)

    # Make sure grid size is 8 when testing
    queen.set_grid_size(size=8)

    moves = queen.get_applied_moves()
    for move in moves:
        assert move in expected_applied_moves
    assert len(expected_applied_moves) == len(moves)

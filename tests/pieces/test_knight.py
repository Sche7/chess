from src.pieces.knight import Knight
from src.pieces.schema import Color, Group


# Test lower knight moves from position (1, 1)
def test_knight_moves_lower_1_1():
    expected_applied_moves = [(2, 3), (0, 3), (3, 2), (3, 0)]
    knight = Knight(position=(1, 1), piece_nr=3, group=Group.lower, color=Color.white)

    # Make sure grid size is 8 when testing
    knight.set_grid_size(size=8)

    moves = knight.get_applied_moves()
    for move in moves:
        assert move in expected_applied_moves
    assert len(expected_applied_moves) == len(moves)


# Test lower knight moves from position (0, 0)
def test_knight_moves_lower_0_0():
    expected_applied_moves = [(2, 1), (1, 2)]
    knight = Knight(position=(0, 0), piece_nr=3, group=Group.lower, color=Color.white)

    # Make sure grid size is 8 when testing
    knight.set_grid_size(size=8)

    moves = knight.get_applied_moves()
    for move in moves:
        assert move in expected_applied_moves
    assert len(expected_applied_moves) == len(moves)


# Test lower knight moves from position (4, 4)
def test_knight_moves_lower_4_4():
    expected_applied_moves = [
        (6, 3),
        (6, 5),  # right
        (2, 3),
        (2, 5),  # left
        (3, 6),
        (5, 6),  # up
        (3, 2),
        (5, 2),  # down
    ]
    knight = Knight(position=(4, 4), piece_nr=3, group=Group.lower, color=Color.white)

    # Make sure grid size is 8 when testing
    knight.set_grid_size(size=8)

    moves = knight.get_applied_moves()
    for move in moves:
        assert move in expected_applied_moves
    assert len(expected_applied_moves) == len(moves)


# Test lower knight moves from position (7, 7)
def test_knight_moves_lower_7_7():
    expected_applied_moves = [(5, 6), (6, 5)]
    knight = Knight(position=(7, 7), piece_nr=3, group=Group.lower, color=Color.white)

    # Make sure grid size is 8 when testing
    knight.set_grid_size(size=8)

    moves = knight.get_applied_moves()
    for move in moves:
        assert move in expected_applied_moves
    assert len(expected_applied_moves) == len(moves)

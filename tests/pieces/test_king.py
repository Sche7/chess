from chess_pieces.king import King
from chess_pieces.schema import Color, Group


# Test lower king moves from position (1, 1)
def test_king_moves_lower_1_1():
    expected_applied_moves = [
        (0, 0),
        (0, 1),
        (0, 2),
        (1, 0),
        (1, 2),
        (2, 0),
        (2, 1),
        (2, 2)
    ]
    king = King(
        position=(1, 1),
        group=Group.lower,
        color=Color.white
    )

    # Make sure grid size is 8 when testing
    king.set_grid_size(size=8)

    moves = king.get_applied_moves()
    for move in moves:
        assert move in expected_applied_moves
    assert len(expected_applied_moves) == len(moves)


# Test lower king moves from position (0, 0)
def test_king_moves_lower_0_0():
    expected_applied_moves = [
        (0, 1),
        (1, 0),
        (1, 1)
    ]
    king = King(
        position=(0, 0),
        group=Group.lower,
        color=Color.white
    )

    # Make sure grid size is 8 when testing
    king.set_grid_size(size=8)

    moves = king.get_applied_moves()
    for move in moves:
        assert move in expected_applied_moves
    assert len(expected_applied_moves) == len(moves)


# Test lower king moves from position (7, 7)
def test_king_moves_lower_7_7():
    expected_applied_moves = [
        (7, 6),
        (6, 7),
        (6, 6)
    ]
    king = King(
        position=(7, 7),
        group=Group.lower,
        color=Color.white
    )

    # Make sure grid size is 8 when testing
    king.set_grid_size(size=8)

    moves = king.get_applied_moves()
    for move in moves:
        assert move in expected_applied_moves
    assert len(expected_applied_moves) == len(moves)

import pytest
from src.pieces.knight import Knight
from src.pieces.schema import Color, Group


@pytest.mark.parametrize(
    "position, expected_applied_moves",
    [
        ((1, 1), [(2, 3), (0, 3), (3, 2), (3, 0)]),
        ((0, 0), [(2, 1), (1, 2)]),
        ((4, 4), [(6, 3), (6, 5), (2, 3), (2, 5), (3, 6), (5, 6), (3, 2), (5, 2)]),
        ((7, 7), [(5, 6), (6, 5)]),
    ],
)
def test_knight_moves(position, expected_applied_moves):
    knight = Knight(position=position, piece_nr=3, group=Group.lower, color=Color.white)

    # Make sure grid size is 8 when testing
    knight.set_grid_size(size=8)

    moves = knight.get_applied_moves()
    for move in moves:
        assert move in expected_applied_moves
    assert len(expected_applied_moves) == len(moves)

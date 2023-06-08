import pytest

from src.pieces.king import King
from src.pieces.schema import Color


@pytest.mark.parametrize(
    "position, expected_applied_moves",
    [
        ((1, 1), [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)]),
        ((0, 0), [(0, 1), (1, 0), (1, 1)]),
        ((7, 7), [(7, 6), (6, 7), (6, 6)]),
    ],
)
def test_king_moves(position, expected_applied_moves):
    king = King(
        position=position,
        piece_nr=6,
        color=Color.white,
    )
    # Make sure grid size is 8 when testing
    king.set_grid_size(size=8)

    moves = king.get_applied_moves()
    for move in moves:
        assert move in expected_applied_moves
    assert len(expected_applied_moves) == len(moves)

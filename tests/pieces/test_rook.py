import pytest

from src.pieces.rook import Rook
from src.pieces.schema import Color, Group


@pytest.mark.parametrize(
    "position, expected_applied_moves",
    [
        (
            (0, 0),
            [
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
            ],
        ),
        (
            (4, 4),
            [
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
            ],
        ),
        (
            (7, 7),
            [
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
            ],
        ),
    ],
)
def test_rook_moves(position, expected_applied_moves):
    rook = Rook(position=position, piece_nr=2, group=Group.lower, color=Color.white)

    # Make sure grid size is 8 when testing
    rook.set_grid_size(size=8)

    moves = rook.get_applied_moves()
    for move in moves:
        assert move in expected_applied_moves
    assert len(expected_applied_moves) == len(moves)

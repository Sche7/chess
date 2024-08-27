import pytest

from src.pieces.color import Color
from src.pieces.queen import Queen


@pytest.mark.parametrize(
    "position, expected_applied_moves",
    [
        (
            (0, 0),
            [  # diagonal moves
                (1, 1),
                (2, 2),
                (3, 3),
                (4, 4),
                (5, 5),
                (6, 6),
                (7, 7),
                # straight moves
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
            [  # diagonal moves
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
                # straight moves
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
            [  # diagonal moves
                (0, 0),
                (1, 1),
                (2, 2),
                (3, 3),
                (4, 4),
                (5, 5),
                (6, 6),
                # straight moves
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
def test_queen_moves(position, expected_applied_moves):
    queen = Queen(position=position, piece_nr=5, color=Color.white)

    # Make sure grid size is 8 when testing
    queen.set_grid_size(size=8)

    moves = queen.get_applied_moves()
    for move in moves:
        assert move in expected_applied_moves
    assert len(expected_applied_moves) == len(moves)

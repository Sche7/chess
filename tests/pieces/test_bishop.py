import pytest
from src.pieces.bishop import Bishop
from src.pieces.schema import Color, Group


@pytest.mark.parametrize(
    # Test lower bishop moves from position (0, 0)
    "position, expected_applied_moves",
    [
        ((0, 0), [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)]),
        (
            (4, 4),
            [
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
            ],
        ),
        ((7, 7), [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)]),
    ],
)
def test_pawn_bishop(position, expected_applied_moves):
    bishop = Bishop(position=position, piece_nr=4, group=Group.lower, color=Color.white)

    # Make sure grid size is 8 when testing
    bishop.set_grid_size(size=8)

    moves = bishop.get_applied_moves()
    for move in moves:
        assert move in expected_applied_moves
    assert len(expected_applied_moves) == len(moves)

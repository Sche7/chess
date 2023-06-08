import pytest

from src.pieces.pawn import Pawn
from src.pieces.color import Color


@pytest.mark.parametrize(
    "position, color, expected_applied_moves",
    [
        ((1, 1), Color.white, [(0, 2), (1, 2), (2, 2), (1, 3)]),
        ((4, 5), Color.white, [(3, 6), (4, 6), (5, 6), (4, 7)]),
        ((7, 7), Color.white, []),
        ((1, 1), Color.black, [(0, 0), (1, 0), (2, 0)]),
        ((4, 5), Color.black, [(3, 4), (4, 4), (5, 4), (4, 3)]),
        ((7, 7), Color.black, [(6, 6), (7, 6), (7, 5)]),
    ],
)
def test_pawn_moves(position, color, expected_applied_moves):
    pawn = Pawn(position=position, piece_nr=1, color=color)
    # Make sure grid size is 8 when testing
    pawn.set_grid_size(size=8)

    moves = pawn.get_applied_moves()
    for move in moves:
        assert move in expected_applied_moves
    assert len(expected_applied_moves) == len(moves)


def test_pawn_moves_exception():
    pawn = Pawn(position=(8, 8), piece_nr=7, color="not working")

    # Make sure grid size is 8 when testing
    pawn.set_grid_size(size=8)

    with pytest.raises(ValueError) as e:
        pawn.moves()
        assert "Color [not working] is not supported" == str(e.value)

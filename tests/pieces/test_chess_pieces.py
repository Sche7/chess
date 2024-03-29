from src.pieces.abstract import AbstractChessPiece
from src.pieces.color import Color


class DummyChessPiece(AbstractChessPiece):
    """
    Realization of AbstractChessPiece
    for testing purposes
    """

    @property
    def moves(self):
        pass


def test_kill_chess_piece():
    chess_piece = DummyChessPiece(position=(1, 1), piece_nr=4, color=Color.white)
    assert chess_piece.status == 1
    chess_piece.kill()
    assert chess_piece.status == 0


def test_update_position():
    chess_piece = DummyChessPiece(position=(1, 2), piece_nr=4, color=Color.white)
    assert chess_piece.position == (1, 2)
    chess_piece.update(move=(-1, 3))
    assert chess_piece.position == (0, 5)


def test_filter_by_grid_size_8():
    chess_piece = DummyChessPiece(position=(7, 7), piece_nr=4, color=Color.white)

    # Make sure grid size is 8 when testing
    chess_piece.set_grid_size(size=8)

    moves_outside = [(8, 7), (0, 9), (-5, 8), (-6, -6)]
    moves_inside = [(4, 4), (5, 5), (1, 5), (6, 7)]

    # all moves
    moves = moves_outside + moves_inside

    # see that the moves outside grid are filtered away
    assert chess_piece.filter_by_grid_size(moves) == moves_inside


def test_filter_by_grid_size_5():
    chess_piece = DummyChessPiece(position=(3, 3), piece_nr=4, color=Color.white)

    # Make sure grid size is 5 when testing
    chess_piece.set_grid_size(size=5)

    moves_outside = [(8, 7), (0, 9), (-5, 8), (-6, -6), (5, 5), (1, 5), (6, 7)]
    moves_inside = [(0, 0), (1, 1), (2, 2), (4, 4), (2, 2)]

    # all moves
    moves = moves_outside + moves_inside

    # see that the moves outside grid are filtered away
    assert chess_piece.filter_by_grid_size(moves) == moves_inside

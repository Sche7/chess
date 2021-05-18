from chess_pieces import ChessPiece
from chess_pieces.schema import Color, Group


def test_kill_chess_piece():
    chess_piece = ChessPiece(
        position=(1, 1),
        group=Group.lower,
        color=Color.white
    )
    assert chess_piece.status == 1
    chess_piece.kill()
    assert chess_piece.status == 0


def test_update_position():
    chess_piece = ChessPiece(
        position=(1, 2),
        group=Group.lower,
        color=Color.white
    )
    assert chess_piece.position == (1, 2)
    chess_piece.update(move=(-1, 3))
    assert chess_piece.position == (0, 5)


def test_filter_by_grid_size():
    chess_piece = ChessPiece(
        position=(8, 8),
        group=Group.lower,
        color=Color.white
    )
    assert chess_piece.position == (8, 8)
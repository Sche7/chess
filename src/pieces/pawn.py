from src.pieces.abstract import AbstractChessPiece
from src.pieces.color import Color


class Pawn(AbstractChessPiece):
    @property
    def moves(self):
        if self.color == Color.white:
            return [(-1, 1), (0, 1), (1, 1), (0, 2)]
        elif self.color == Color.black:
            return [(1, -1), (0, -1), (-1, -1), (0, -2)]
        else:
            raise ValueError(f"Color [{str(self.color)}] is not supported")

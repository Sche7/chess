from chess_pieces.abstract import AbstractChessPiece
from chess_pieces.schema import Group


class Pawn(AbstractChessPiece):
    @property
    def moves(self):
        if self.group == Group.lower:
            return [(-1, 1), (0, 1), (1, 1), (0, 2)]
        elif self.group == Group.upper:
            return [(1, -1), (0, -1), (-1, -1), (0, -2)]
        else:
            raise ValueError(f"Group [{str(self.group)}] is not supported")

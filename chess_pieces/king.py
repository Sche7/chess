from typing import Tuple
from chess_pieces import ChessPiece
from chess_pieces.schema import Color, Group


class King(ChessPiece):
    def __init__(
        self,
        position: Tuple,
        group: Group,
        color: Color
    ):
        super().__init__(
            position=position,
            group=group,
            color=color
        )

    @property
    def moves(self):
        output = [
            (-1, 1), (0, 1),
            (1, 1), (-1, 0),
            (1, 0), (-1, -1),
            (0, -1), (1, -1)
        ]
        return output

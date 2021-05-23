from typing import Tuple
from chess_pieces import ChessPiece
from chess_pieces.schema import Color, Group


class Knight(ChessPiece):
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
            (-2, 1), (-2, -1),  # left
            (2, 1), (2, -1),    # right
            (1, 2), (-1, 2),    # up
            (1, -2), (-1, -2)   # down
        ]
        return output

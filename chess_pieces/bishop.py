from typing import Tuple
from chess_pieces import ChessPiece
from chess_pieces.schema import Color, Group


class Bishop(ChessPiece):
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
        output = []
        for i in range(1, self.grid_size):
            output.extend([(i, i), (-i, i), (i, -i), (-i, -i)])
        return output
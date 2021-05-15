from typing import Tuple
from chess_pieces import ChessPiece
from chess_pieces.schema import Color, Group


class Pawn(ChessPiece):
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
        if self.group == Group.lower:
            return [(-1, 1), (0, 1), (1, 1)]
        elif self.group == Group.upper:
            return [(1, -1), (0, -1), (-1, -1)]
        else:
            raise ValueError(f'Group {self.group.name} is not supported')

    def get_applied_moves(self) -> list:
        output = [self.apply_move(move) for move in self.moves]

        return output

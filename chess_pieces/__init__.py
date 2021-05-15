from typing import Tuple, List
from chess_pieces.schema import Color, Group


class ChessPiece(object):
    def __init__(
        self,
        position: Tuple,
        group: Group,
        color: Color
    ):
        self.position = position
        self.group = group
        self.color = color
        self.status = 1

    def get_applied_moves(self) -> List[Tuple]:
        raise NotImplementedError(
            'subclasses must override get_applied_moves()'
        )

    def apply_move(self, move: Tuple) -> Tuple:
        return tuple(map(sum, zip(self.position, move)))

    def update(self, move: Tuple) -> None:
        self.position = self.apply_move(move)

    def kill(self) -> None:
        self.status = 0

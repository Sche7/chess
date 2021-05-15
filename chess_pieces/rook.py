from typing import Tuple
from chess_pieces import ChessPiece
from chess_pieces.schema import Color, Group


class Rook(ChessPiece):
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
        pass

    def get_applied_moves(self) -> list:
        output = [self.apply_move(move) for move in self.moves]

        return output
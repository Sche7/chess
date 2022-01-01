from typing import Tuple
from chess_pieces.schema import Color, Group


class ChessPiece(object):
    # Grid size of a chess board
    grid_size = 8

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
        self.name = self.__class__.__name__
        self.id = id(self)

    @property
    def moves():
        pass

    def is_inside_grid(self, position: Tuple):
        return (
            (position[0] >= 0) and (position[1] < self.grid_size) and
            (position[1] >= 0) and (position[0] < self.grid_size)
        )

    def filter_by_grid_size(self, moves: list):
        """
        Helper method to filter moves by grid size.
        Will filter out any moves resulting outside of grid.
        """
        return [
            coord for coord in moves if self.is_inside_grid(coord)
        ]

    def apply_move(self, move: Tuple) -> Tuple:
        return (self.position[0] + move[0], self.position[1] + move[1])

    def update(self, move: Tuple) -> None:
        self.position = self.apply_move(move)

    def set_grid_size(self, size: int):
        self.grid_size = size

    def get_applied_moves(self) -> list:
        output = self.filter_by_grid_size(
            [self.apply_move(move) for move in self.moves]
        )
        return output

    def kill(self) -> None:
        self.status = 0

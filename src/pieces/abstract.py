from abc import ABC, abstractmethod

from src.pieces.color import Color


class AbstractChessPiece(ABC):
    """
    Abstract class for chess pieces
    """

    grid_size = 8  # Grid size of a chess board
    status = 1  # Status of chess piece: Alive [1] or dead [0]

    def __init__(self, position: tuple, piece_nr: int, color: Color):
        self.position = position
        self.piece_nr = piece_nr
        self.color = color
        self.name = self.__class__.__name__
        self.id = id(self)

    @property
    @abstractmethod
    def moves(self):
        raise NotImplementedError("'moves' method not implemented")

    def is_inside_grid(self, position: tuple):
        return (
            (position[0] >= 0)
            and (position[1] < self.grid_size)
            and (position[1] >= 0)
            and (position[0] < self.grid_size)
        )

    def filter_by_grid_size(self, moves: list):
        """
        Helper method to filter moves by grid size.
        Will filter out any moves resulting outside of grid.
        """
        return [coord for coord in moves if self.is_inside_grid(coord)]

    def apply_move(self, move: tuple) -> tuple:
        return (self.position[0] + move[0], self.position[1] + move[1])

    def update(self, move: tuple) -> None:
        self.position = self.apply_move(move)

    def set_position(self, position: tuple) -> None:
        self.position = position

    def set_grid_size(self, size: int):
        self.grid_size = size

    def get_applied_moves(self) -> list:
        output = self.filter_by_grid_size(
            [self.apply_move(move) for move in self.moves]
        )
        return output

    def kill(self) -> None:
        self.status = 0

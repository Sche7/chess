from typing import Union
from chess_pieces import AbstractChessPiece


class Player:
    def __init__(self, color: str):
        self.color = color
        self.pieces = {}

    def __eq__(self, other: Union[str, object]) -> bool:
        if isinstance(other, str):
            return self.color == other
        return self.color == other.color

    def add_chess_piece(self, chess_piece: AbstractChessPiece):
        pass


class ChessPlayers:
    def __init__(self):
        self.white = Player('white')
        self.black = Player('black')
        self.active_player = self.white
        self.inactive_player = self.black

    def switch_turn(self) -> None:
        if self.active_player == self.white:
            self.active_player = self.black
            self.inactive_player = self.white
        else:
            self.active_player = self.white
            self.inactive_player = self.black

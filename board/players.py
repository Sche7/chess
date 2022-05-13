from typing import Union
from chess_pieces import Color
from chess_pieces import AbstractChessPiece


class Player:
    def __init__(self, color: Color):
        self.color = color
        self.pieces = {}

    def __eq__(self, other: Union[str, object]) -> bool:
        if isinstance(other, str):
            return self.color.value == other
        return self.color.value == other.color.value

    def add_chess_piece(self, chess_piece: AbstractChessPiece) -> None:
        id = chess_piece.id
        self.pieces[id] = chess_piece

    def remove_chess_piece(self, chess_piece_id: int) -> None:
        self.pieces.pop(chess_piece_id)


class ChessPlayers:
    def __init__(self):
        self.white = Player(color=Color.white)
        self.black = Player(color=Color.black)
        self.active_player = self.white
        self.inactive_player = self.black

    def switch_turn(self) -> None:
        if self.active_player == self.white:
            self.active_player = self.black
            self.inactive_player = self.white
        else:
            self.active_player = self.white
            self.inactive_player = self.black

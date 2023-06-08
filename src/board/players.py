from collections import defaultdict
from enum import Enum
from typing import TYPE_CHECKING, Dict, Union

from src.pieces import Color

if TYPE_CHECKING:
    from src.pieces.abstract import AbstractChessPiece


class ChessPieceType(Enum):
    pawn: str = "Pawn"
    bishop: str = "Bishop"
    rook: str = "Rook"
    knight: str = "Knight"
    queen: str = "Queen"
    king: str = "King"


class Player:
    """
    Player class that holds information about
    all chess pieces belonging to player.
    """

    def __init__(self, color: Color):
        self.color = color
        self.chess_pieces = defaultdict(dict)

    def __eq__(self, other: Union[str, object]) -> bool:
        if isinstance(other, str):
            return self.color.value == other
        return self.color.value == other.color.value

    def add_chess_piece(self, chess_piece: "AbstractChessPiece") -> None:
        id = chess_piece.id
        name = chess_piece.name
        self.chess_pieces[name][id] = chess_piece

    def remove_chess_piece(self, chess_piece_name: str, chess_piece_id: int) -> None:
        self.chess_pieces[chess_piece_name].pop(chess_piece_id)

    def kill(self, chess_piece_name: str, chess_piece_id: int) -> None:
        self.chess_pieces[chess_piece_name][chess_piece_id].kill()

    @classmethod
    def filter_alive_pieces(
        self, chess_pieces: Dict[int, "AbstractChessPiece"]
    ) -> Dict[int, "AbstractChessPiece"]:
        chess_pieces_alive = {
            chess_piece_id: chess_piece
            for chess_piece_id, chess_piece in chess_pieces.items()
            if chess_piece.status != 0
        }
        return chess_pieces_alive

    def get_pawns(self) -> Dict[int, "AbstractChessPiece"]:
        """
        Returns a dictionary of active Pawns
        """
        pawns = self.chess_pieces[ChessPieceType.pawn.value]
        active_pawns = self.filter_alive_pieces(pawns)
        return active_pawns

    def get_bishops(self) -> Dict[int, "AbstractChessPiece"]:
        """
        Returns a dictionary of active Bishops
        """
        bishops = self.chess_pieces[ChessPieceType.bishop.value]
        active_bishops = self.filter_alive_pieces(bishops)
        return active_bishops

    def get_rooks(self) -> Dict[int, "AbstractChessPiece"]:
        """
        Returns a dictionary of active Rooks
        """
        rooks = self.chess_pieces[ChessPieceType.rook.value]
        active_rooks = self.filter_alive_pieces(rooks)
        return active_rooks

    def get_knights(self) -> Dict[int, "AbstractChessPiece"]:
        """
        Returns a dictionary of active Knights
        """
        knights = self.chess_pieces[ChessPieceType.knight.value]
        active_knights = self.filter_alive_pieces(knights)
        return active_knights

    def get_queens(self) -> Dict[int, "AbstractChessPiece"]:
        """
        Returns a dictionary of active Queens
        """
        queens = self.chess_pieces[ChessPieceType.queen.value]
        active_queens = self.filter_alive_pieces(queens)
        return active_queens

    def get_king(self) -> Dict[int, "AbstractChessPiece"]:
        """
        Returns a dictionary of active King
        """
        return self.chess_pieces[ChessPieceType.king.value]


class ChessPlayers:
    """
    Class that contains two players, white and black,
    for chess game. It keeps track on which player
    is active and inactive during game play.
    """

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

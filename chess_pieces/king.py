from chess_pieces.abstract import AbstractChessPiece


class King(AbstractChessPiece):
    @property
    def moves(self):
        output = [(-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (0, -1), (1, -1)]
        return output

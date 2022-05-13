from chess_pieces.abstract import AbstractChessPiece


class Knight(AbstractChessPiece):

    @property
    def moves(self):
        output = [
            (-2, 1), (-2, -1),  # left
            (2, 1), (2, -1),    # right
            (1, 2), (-1, 2),    # up
            (1, -2), (-1, -2)   # down
        ]
        return output

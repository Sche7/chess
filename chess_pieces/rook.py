from chess_pieces import AbstractChessPiece


class Rook(AbstractChessPiece):

    @property
    def moves(self):
        output = []
        for i in range(1, self.grid_size):
            output.extend([(i, 0), (0, i), (-i, 0), (0, -i)])
        return output

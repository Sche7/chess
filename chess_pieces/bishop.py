from chess_pieces import AbstractChessPiece


class Bishop(AbstractChessPiece):

    @property
    def moves(self):
        output = []
        for i in range(1, self.grid_size):
            output.extend([(i, i), (-i, i), (i, -i), (-i, -i)])
        return output

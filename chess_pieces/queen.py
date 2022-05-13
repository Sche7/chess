from chess_pieces.abstract import AbstractChessPiece

class Queen(AbstractChessPiece):

    @property
    def moves(self):
        output = []

        # Straight moves
        for i in range(1, self.grid_size):
            output.extend([(i, 0), (0, i), (-i, 0), (0, -i)])

        # Diagonal moves
        for i in range(1, self.grid_size):
            output.extend([(i, i), (-i, i), (i, -i), (-i, -i)])

        return output

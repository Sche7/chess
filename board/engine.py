import numpy as np
from numpy import matrix

from board.files import read_yaml
from chess_pieces.pawn import Pawn
from chess_pieces.bishop import Bishop
from chess_pieces.knight import Knight
from chess_pieces.rook import Rook
from chess_pieces.queen import Queen
from chess_pieces.king import King
from chess_pieces.schema import Color, Group


class Engine:
    def __init__(self, config_path: str):
        self.config = read_yaml(config_path)
        self.representation = self.config['PIECE_REPRESENTATION']
        self.start_state = self.config['GAME_START']
        self.grid_size = self.config['GRID_SIZE']

    def create_piece(self, piece: int, position: tuple) -> None:
        kwargs = {
            'position': position,
        }
        if (piece < 7) and (piece > 0):
            kwargs['group'] = Group.lower
            kwargs['color'] = Color.white
        elif (piece >= 7) and (piece <= 12):
            kwargs['group'] = Group.upper
            kwargs['color'] = Color.black

        if piece in [1, 7]:
            return Pawn(**kwargs)
        elif piece in [2, 8]:
            return Rook(**kwargs)
        elif piece in [3, 9]:
            return Knight(**kwargs)
        elif piece in [4, 10]:
            return Bishop(**kwargs)
        elif piece in [5, 11]:
            return Queen(**kwargs)
        elif piece in [6, 12]:
            return King(**kwargs)
        else:
            return

    def initiate_pieces(self, board: matrix) -> None:
        pieces = []
        nrows, ncols = board.shape
        for i in range(0, nrows):
            for j in range(0, ncols):
                created_piece = self.create_piece(
                                    piece=board[i, j],
                                    position=(i, j)
                                )
                if created_piece:
                    pieces.append(created_piece)

        self.pieces = pieces

    def start_game(self) -> None:
        game_state = matrix(self.start_state).astype(int)

        # numpy matrix indexing works top and down,
        # therefore it is necessary to flip the table for
        # correct indexing
        self.game_state = np.flip(game_state).copy()

        self.initiate_pieces(board=self.game_state)

    def update_game_state(self, board: matrix) -> None:
        pass

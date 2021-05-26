import numpy as np
from nptyping import NDArray
from typing import Dict

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
        self.pieces = {}

    def _get_pieces(self, name: str, pieces: list):
        """
        Method to filter on list of pieces
        """
        return [
            piece for piece in pieces
            if piece.__class__.__name__.lower() == name.lower()
        ]

    def create_piece(self, piece: int, position: tuple) -> None:
        kwargs = {
            'position': position,
        }
        # TODO: Eventually make it possible to
        # open game with lower/upper options
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

    def initiate_pieces(self, board: NDArray) -> Dict[list, list]:
        black_pieces = []
        white_pieces = []
        nrows, ncols = board.shape

        # Loop through all entries in array to create pieces
        for i in range(nrows):
            for j in range(ncols):
                created_piece = self.create_piece(
                                    piece=board[i, j],
                                    position=(i, j)
                                )

                # If piece is created, distribute piece
                # to respective color group
                if created_piece:
                    if created_piece.color.name == 'white':
                        white_pieces.append(created_piece)
                    elif created_piece.color.name == 'black':
                        black_pieces.append(created_piece)

        return {
            'white': white_pieces,
            'black': black_pieces
        }

    def check_game_state(self):
        pass

    def update_game_state(self, board: NDArray) -> None:
        pass

    def handle_game(self, player_input) -> None:
        pass

    def get_possible_actions(self) -> dict:
        pass

    def switch_turn(self) -> None:
        switch = {
            'white': 'black',
            'black': 'white'
        }
        self.player_turn = switch[self.player_turn]

    def start_game(self) -> None:
        """
        Initiates a new game.
        Starting game state depends on config.GAME_START input.
        """
        game_state = np.array(self.start_state).astype(int)

        # numpy array indexing works top and down,
        # therefore it is necessary to flip the table for
        # correct indexing
        self.game_state = np.flip(game_state).copy()

        # Create pieces in game
        self.pieces = self.initiate_pieces(board=self.game_state)

        # Starting game
        self.game_over = False
        self.player_turn = 'white'

    def get_white_pawns(self):
        return self._get_pieces('pawn', self.pieces.get('white', []))

    def get_white_rooks(self):
        return self._get_pieces('rook', self.pieces.get('white', []))

    def get_white_bishops(self):
        return self._get_pieces('bishop', self.pieces.get('white', []))

    def get_white_knights(self):
        return self._get_pieces('knight', self.pieces.get('white', []))

    def get_white_queen(self):
        return self._get_pieces('queen', self.pieces.get('white', []))

    def get_white_king(self):
        return self._get_pieces('king', self.pieces.get('white', []))

    def get_black_pawns(self):
        return self._get_pieces('pawn', self.pieces.get('black', []))

    def get_black_rooks(self):
        return self._get_pieces('rook', self.pieces.get('black', []))

    def get_black_bishops(self):
        return self._get_pieces('bishop', self.pieces.get('black', []))

    def get_black_knights(self):
        return self._get_pieces('knight', self.pieces.get('black', []))

    def get_black_queen(self):
        return self._get_pieces('queen', self.pieces.get('black', []))

    def get_black_king(self):
        return self._get_pieces('king', self.pieces.get('black', []))
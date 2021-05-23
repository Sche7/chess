from numpy import matrix
from board.files import read_yaml


class View:
    def __init__(self, config_path: str):
        self.config = read_yaml(config_path)
        self.representation = self.config['PIECE_REPRESENTATION']

    def display_board(self, board: matrix) -> None:
        raise NotImplementedError('method "display_board" is not implemented')

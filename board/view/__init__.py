from nptyping import NDArray
from board.files import read_yaml


class View:
    def __init__(self, config_path: str):
        self.config = read_yaml(config_path)
        self.representation = self.config['PIECE_REPRESENTATION']

    def display_board(self, board: NDArray) -> None:
        raise NotImplementedError('method "display_board" is not implemented')

    def await_input(self, board: NDArray):
        raise NotImplementedError('method "await_input" is not implemented')

    def display_player_turn(self, player: str) -> None:
        raise NotImplementedError(
            'method "display_player_turn" is not implemented'
        )

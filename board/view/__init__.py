from nptyping import NDArray
from board.files import read_yaml
from abc import abstractmethod


class View:
    """
    Interface for chess viewer
    """
    def __init__(self, config_path: str):
        self.config = read_yaml(config_path)
        self.representation = self.config['PIECE_REPRESENTATION']

    @abstractmethod
    def initialize(self):
        raise NotImplementedError('method "initialize" is not implemented')

    @abstractmethod
    def display_board(self, board: NDArray):
        raise NotImplementedError('method "display_board" is not implemented')

    @abstractmethod
    def await_input(self, board: NDArray):
        raise NotImplementedError('method "await_input" is not implemented')

    @abstractmethod
    def display_player_turn(self, player: str):
        raise NotImplementedError(
            'method "display_player_turn" is not implemented'
        )

    def surrender_message(self, player: str):
        raise NotImplementedError('method "surrender_message" is not implemented')

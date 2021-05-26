from nptyping import NDArray
from board.view import View


class PygameView(View):
    def __init__(self, config_path: str):
        super().__init__(config_path=config_path)

    def display_board(self, board: NDArray) -> None:
        raise NotImplementedError('method "display_board" is not implemented')

    def await_input(self, board: NDArray):
        raise NotImplementedError('method "await_input" is not implemented')

    def display_player_turn(self, player: str) -> None:
        raise NotImplementedError(
            'method "display_player_turn" is not implemented'
        )

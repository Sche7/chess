from board.engine import Engine
from board.view import View


class ChessBoard(Engine):
    def __init__(self, config_path: str, displayer: View):
        super().__init__(config_path=config_path)

        self.view = displayer(config_path)

    def run(self):
        pass

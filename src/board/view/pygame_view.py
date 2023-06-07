import pygame

from src.board.files import read_yaml
from nptyping import NDArray
from src.board.view import View


class PygameView(View):
    def __init__(self, config_path: str):
        self.config = read_yaml(config_path)
        self.representation = self.config["PIECE_REPRESENTATION"]

    def initialize(self) -> None:
        pygame.init()
        pygame.display.set_caption("A bit Racey")

    def display_board(self, board: NDArray) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
        pygame.display.update()

    def await_input(self, board: NDArray):
        pass

    def display_player_turn(self, player: str) -> None:
        pass

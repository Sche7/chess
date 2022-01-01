import pygame

from nptyping import NDArray
from board.view import View


class PygameView(View):
    def __init__(self, config_path: str):
        super().__init__(config_path=config_path)

    def initialize(self) -> None:
        pygame.init()
        pygame.display.set_caption('A bit Racey')

    def display_board(self, board: NDArray) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
        pygame.display.update()

    def await_input(self, board: NDArray):
        pass

    def display_player_turn(self, player: str) -> None:
        pass

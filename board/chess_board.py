from board.engine import Engine
from board.displayer_factory import display_factory, Displayer


class ChessBoard(Engine):
    def __init__(self, config_path: str, displayer: Displayer):
        super().__init__(config_path=config_path)

        self.displayer = display_factory(
            displayer=displayer,
            config_path=config_path
        )

    def run(self):
        self.start_game()

        while not self.game_over:
            # Display board
            self.displayer.display_board(self.game_state)
            self.displayer.display_player_turn(self.player_turn)

            # Compute possible actions
            actions = self.get_possible_actions()
            player_input = self.displayer.await_input(actions)

            # Do action
            self.handle_game(player_input)

            # Before player turn is over
            self.check_game_state()
            self.switch_turn()
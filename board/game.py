from board.engine import Engine
from board.view.displayer_factory import View


class Chess:
    """
    This is the main chess game class.

    Parameters
    ----
    config_path: str
        Folder path to game configuration file.
        Has to be a yaml-file.
    displayer: Displayer
        The desired displayer for playing chess.
        See: chess/board/view/displayer_factory.py
        for more info.
    """

    def __init__(
        self,
        engine: Engine,
        displayer: View
    ):
        self.engine = engine
        self.displayer = displayer
        self.game_over = False

        # TODO: Have player_turn variable in this class instead of in the engine
        # It should be the Game class dictating the player turn and not the engine.

    def run(self):
        self.engine.start_game()
        self.displayer.initialize()
        while not self.game_over:
            # Display board
            self.displayer.display_board(self.engine.game_state)
            self.displayer.display_player_turn(self.engine.player_turn)

            # Compute possible actions
            actions = self.engine.get_all_possible_actions()
            player_input = self.displayer.await_input(actions)

            # If player surrendered, then end the game
            # else do action
            if not player_input:
                self.game_over = True
                # TODO: Log this instead of printing
                print(f'Player {self.engine.player_turn} surrendered. Game over.')
                continue

            self.engine.handle_game(player_input)

            # Before player turn is over
            self.engine.check_game_state()
            self.engine.switch_turn()

from board.engine import Engine
from board.view.displayer_factory import View


class Chess:
    """
    This is the main chess game class.

    Parameters
    ----
    engine: Engine
        An instance of the Engine class.
    displayer: View
        The desired displayer for playing chess.
        See: chess/board/view/displayer_factory.py
        for more info.
    """

    switch = {
        'white': 'black',
        'black': 'white'
    }

    def __init__(
        self,
        engine: Engine,
        displayer: View
    ):
        self.engine = engine
        self.displayer = displayer
        self.game_over = False
        self.player_turn = 'white'

    def switch_turn(self) -> None:
        self.player_turn = self.switch[self.player_turn]

    def run(self):
        self.engine.start_game()
        self.displayer.initialize()
        while not self.game_over:
            # Display board
            self.displayer.display_board(self.engine.game_state)
            self.displayer.display_player_turn(self.player_turn)

            # Compute possible actions
            actions = self.engine.get_all_possible_actions(player=self.player_turn)
            player_input = self.displayer.await_input(actions)

            # If player surrendered, then end the game
            # else do action
            if not player_input:
                self.game_over = True
                # TODO: Log this instead of printing
                print(f'Player {self.player_turn} surrendered. Game over.')
                continue

            self.engine.handle_game(player=self.player_turn, player_input=player_input)

            # Before player turn is over
            self.engine.check_game_state()
            self.switch_turn()

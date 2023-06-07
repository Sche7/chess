from src.board.engine import Engine
from src.board.view.displayer_factory import View


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

    switch = {"white": "black", "black": "white"}

    def __init__(self, engine: Engine, displayer: View):
        self.engine = engine
        self.displayer = displayer
        self.game_over = False
        self.player_turn = "white"
        self.game_state = None

    def switch_turn(self) -> None:
        self.player_turn = self.switch[self.player_turn]

    def run(self):
        self.game_state = self.engine.start_game()
        self.displayer.initialize()
        while not self.game_over:
            # Display board
            self.displayer.display_board(self.game_state)
            self.displayer.display_player_turn(self.player_turn)

            # Compute possible actions
            actions = self.engine.get_all_possible_actions(player=self.player_turn)
            player_input = self.displayer.await_input(actions)

            # If player surrendered, then end the game
            if not player_input:
                self.game_over = True
                self.displayer.surrender_message(player=self.player_turn)
                continue

            # Handle game with player input
            # Set new game state
            self.game_state = self.engine.handle_game(
                player=self.player_turn,
                player_input=player_input,
                game_state=self.game_state,
            )

            # Evaluate game state for player
            if self.engine.is_checkmate(player=self.switch[self.player_turn]):
                self.game_over = True
                self.displayer.game_over_message(player=self.player_turn)

            self.switch_turn()

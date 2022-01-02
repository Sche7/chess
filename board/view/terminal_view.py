"""
This class is used to generate the chess board view in the terminal.
The representation of each piece are described below:

0 | Empty tiles    | ' ' |
13| Possible moves |  +  |

White                        Black
-------------------          ------------------
| 1 | Pawn    | P |         | 7 | Pawn    | p |
| 2 | Rook    | R |         | 8 | Rook    | r |
| 3 | Knight  | N |         | 9 | Knight  | n |
| 4 | Bishop  | B |         | 10| Bishop  | b |
| 5 | Queen   | Q |         | 11| Queen   | q |
| 6 | King    | K |         | 12| King    | k |
-------------------         -------------------

"""


from nptyping import NDArray
from typing import Tuple
from board.view import View
from simple_term_menu import TerminalMenu


class TerminalView(View):
    def __init__(self, config_path: str):
        super().__init__(config_path=config_path)

    def initialize(self):
        """
        This method is not needed for TerminaViewer
        """
        pass

    def generate_view(self, board: NDArray) -> str:
        grid_size = len(board)

        line = f'{(grid_size*4+5)*"-"}\n'

        # Start with two whitespaces
        output = ["  "]

        def divider():
            output.append("| \n")
            output.append(line)

        # First row
        for j in range(grid_size):
            output.append(f"| {j} ")
        divider()

        # Other rows
        for i in range(grid_size-1, -1, -1):
            output.append(f"{i} ")
            for j in range(grid_size):
                output.append(
                    f"| {self.representation.get(board[i, j])} "
                )
            divider()
        return "".join(output)

    def display_board(self, board: NDArray) -> None:
        # Clear terminal
        print("\033c")

        # Print new board
        print(self.generate_view(board), flush=True)

    def display_player_turn(self, player: str) -> None:
        print(f'It is {player}´s turn to make a move')

    def menu(self, possible_actions) -> Tuple[list, TerminalMenu]:
        """
        Menu method initiates TerminalMenu class.
        """
        choices = [key for key in possible_actions.keys()]

        # Display exit option
        choices.append('[g] Give up')

        return choices, TerminalMenu(choices)

    def await_input(self, possible_actions: dict) -> dict:
        """
        Method for showing console menu that awaits
        user input.

        Returns
        ----
            Dictionary containing two keys:
                id: ID of chess piece
                action: New position for specififed chess piece
            returns empty dict if player surrenders.
        """
        choices, main_menu = self.menu(possible_actions)
        exit = False

        while not exit:
            # Display main menu
            main_option_index = main_menu.show()

            # Get chosen option
            main_option_selected = choices[main_option_index]

            # Handle choice of option.
            if (main_option_selected == '[g] Give up'):
                # if player gives up, then exit while-loop
                exit = True
            else:
                # Retrieve information from player input
                actions = possible_actions[main_option_selected].get('actions')
                chess_piece_id = possible_actions[main_option_selected].get('id')

                # Prepare options for submenu.
                # This submenu will show possible actions for the selected
                # chess piece.
                # Make sure options are of type string, otherwise TerminalMenu
                # will complain.
                sub_options = [str(opt) for opt in actions]

                # Append option to go back to main menu where user can reselect
                # chess piece.
                sub_options.append('[b] Go Back')

                # Initiate sub menu that displays possible actions
                # for a chess piece.
                sub_menu = TerminalMenu(
                    sub_options,
                    title=f'Where would you like to move {main_option_selected}?'
                )
                sub_option_index = sub_menu.show()

                # Get chosen option for chess piece
                sub_option_selected = sub_options[sub_option_index]

                # NOTE: No action for sub option '[b] Go Back'.
                # by default this works like a 'step back' to main menu.
                if (sub_option_selected != '[b] Go Back'):
                    return {
                        'id': chess_piece_id,
                        'action': actions[sub_option_index]
                    }

        return {}

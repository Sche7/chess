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
from string import ascii_lowercase
import numpy as np

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
        copied_board = board.copy()

        # Rotate board to create better view
        copied_board = np.rot90(copied_board, k=5)

        line = f'{(grid_size*4+5)*"-"}\n'

        # Start with two whitespaces
        output = ["  "]

        def divider():
            output.append("| \n")
            output.append(line)

        # First row
        for j in [ascii_lowercase[i] for i in range(grid_size)]:
            output.append(f"| {j} ")
        divider()

        # Other rows
        for i in range(0, grid_size, 1):
            output.append(f"{grid_size - i} ")
            for j in range(grid_size):
                output.append(
                    f"| {self.representation.get(copied_board[i, j])} "
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

    def _convert_cell_index(self, index_tuple: Tuple[int, int]) -> Tuple[int, str]:
        """
        Converts numpy cell indices to their respective
        readable representation.
        For example:
            (0, 1) -> (a, 2)
            (2, 4) -> (c, 5)

        """
        x = ascii_lowercase[index_tuple[0]]
        y = index_tuple[1] + 1
        return (x, y)

    def unwrap_possible_actions(
        self,
        possible_actions,
        convert_indices=False
    ) -> dict:
        """
        Convenience method for unwrapping possible actions output
        from engine.
        """
        output = {}
        # Unwrap information
        for piece_type, pieces in possible_actions.items():
            for piece in pieces:
                position = piece.get('position')
                representation = self.representation.get(piece.get('piece_nr'))
                if convert_indices:
                    position = self._convert_cell_index(position)
                    position_str = f'({position[0]}, {position[1]})'

                name = f'{representation} {piece_type} {position_str}'
                output[name] = piece
        return output

    def menu(self, possible_actions) -> Tuple[list, TerminalMenu]:
        """
        Menu method initiates TerminalMenu class.
        """
        choices = [key for key in possible_actions.keys()]

        # Display exit option
        choices.append('[g] Give up')

        return choices, TerminalMenu(choices)

    def initialize_dialog(self, title: str, options: list) -> Tuple[str, int]:
        menu = TerminalMenu(
                options,
                title=title
            )
        option_index = menu.show()
        option_selected = options[option_index]

        return option_selected, option_index

    def surrender_message(self, player: str) -> None:
        print(f'Player {player} surrendered. Game over.')

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
        # Unwrap information
        unwrapped_actions = self.unwrap_possible_actions(
            possible_actions=possible_actions,
            convert_indices=True
        )

        choices, main_menu = self.menu(unwrapped_actions)
        exit = False

        while not exit:
            # Display main menu
            main_option_index = main_menu.show()

            # Get chosen option
            main_option_selected = choices[main_option_index]

            # Handle choice of option.
            if (main_option_selected == '[g] Give up'):

                # Extra safeguard from accidentally giving up
                surrender_option_selected, _ = self.initialize_dialog(
                    title='Are you sure you want to surrender?',
                    options=['No', 'Yes']
                )
                if surrender_option_selected == 'Yes':
                    # if player gives up, then exit while-loop
                    exit = True
            else:
                # Retrieve information from player input
                actions = unwrapped_actions[main_option_selected].get('actions')
                chess_piece_id = unwrapped_actions[main_option_selected].get('id')

                # Prepare options for submenu.
                # This submenu will show possible actions for the selected
                # chess piece.
                # Make sure options are converted to the right indices
                def _convert_index_to_string(option):
                    str_option = self._convert_cell_index(option)
                    return f'({str_option[0]}, {str_option[1]})'

                sub_options = [
                    _convert_index_to_string(opt) for opt in actions
                ]

                # Append option to go back to main menu where user can reselect
                # chess piece.
                sub_options.append('[b] Go Back')

                # Initiate sub menu that displays possible actions
                # for a chess piece.
                sub_option_selected, sub_option_index = self.initialize_dialog(
                    title=f'Where would you like to move {main_option_selected}?',
                    options=sub_options
                )

                # NOTE: No action for sub option '[b] Go Back'.
                # by default this works like a 'step back' to main menu.
                if (sub_option_selected != '[b] Go Back'):
                    return {
                        'id': chess_piece_id,
                        'action': actions[sub_option_index]
                    }

        return {}

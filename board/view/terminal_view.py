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

    def await_input(self, possible_actions: dict):
        """
        Method for showing console menu that awaits
        user input.
        """
        choices, terminal_menu = self.menu(possible_actions)
        exit = False

        while not exit:
            # Display menu
            option_index = terminal_menu.show()

            # Get chosen option
            option_choice = choices[option_index]

            # Handle chose of option.
            if (option_choice == '[g] Give up'):
                exit = True
            else:
                # Retrieve chess piece information
                actions = possible_actions[option_choice].get('actions')
                chess_piece_id = possible_actions[option_choice].get('id')

                # Prepare options for submenu
                sub_options = [
                    str(opt) for opt in
                    actions
                ]
                sub_options.append('[b] Go Back')

                # Initiate sub menu that displays possible actions
                # for a chess piece.
                sub_menu = TerminalMenu(
                    sub_options,
                    title=f'Where would you like to move {option_choice}?'
                )
                sub_option_index = sub_menu.show()

                # Get chosen option for chess piece
                sub_option_choice = sub_options[sub_option_index]

                if (sub_option_choice != '[b] Go Back'):
                    return {
                        'id': chess_piece_id,
                        'action': actions[sub_option_index]
                    }

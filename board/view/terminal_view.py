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
from board.view import View


class TerminalView(View):
    def __init__(self, config_path: str):
        super().__init__(config_path=config_path)

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

    def await_input(self, possible_actions: dict):
        print('What will you do?')
        action = input()
        return action

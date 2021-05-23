"""
0 | Empty tiles    | ' ' |
13| Possible moves |  +  |

White                        Black
-------------------          ------------------
| 1 | Pawn    | W |         | 7 | Pawn    | w |
| 2 | Rook    | R |         | 8 | Rook    | r |
| 3 | Knight  | N |         | 9 | Knight  | n |
| 4 | Bishop  | B |         | 10| Bishop  | b |
| 5 | Queen   | Q |         | 11| Queen   | q |
| 6 | King    | K |         | 12| King    | k |
-------------------         -------------------

"""


from numpy import matrix
from board.files import read_yaml


class View:
    def __init__(self, config_path: str):
        self.config = read_yaml(config_path)
        self.representation = self.config['PIECE_REPRESENTATION']
        self.game_state = self.config['GAME_START']

    def generate_view(self, board: matrix) -> str:
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
                output.append(f"| {self.representation.get(board[i, j])} ")
            divider()
        return "".join(output)

    def display_board(self, board: matrix) -> None:
        print(self.generate_view(board))

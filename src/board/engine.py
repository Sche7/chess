from typing import TYPE_CHECKING, Dict, List, Literal, Optional, Tuple, Type, Union

import numpy as np
from nptyping import NDArray

from src.board.files import read_yaml
from src.pieces import Bishop, Color, Group, King, Knight, Pawn, Queen, Rook

if TYPE_CHECKING:
    from src.pieces.abstract import AbstractChessPiece


class GameError(Exception):
    pass


class Engine:

    opponent_of = {"white": "black", "black": "white"}

    def __init__(self, config_path: str):
        self.config = read_yaml(config_path)
        self.representation = self.config["PIECE_REPRESENTATION"]
        self.start_state = self.config["GAME_START"]
        self.pieces = {}

    def start_game(self) -> NDArray:
        """
        Initiates a new game.
        Starting game state depends on config.GAME_START input.
        """
        game_state = np.array(self.start_state).astype(int)

        # numpy array indexing works top and down,
        # row on y-axis and column on x-axis,
        # therefore it is necessary to flip and transpose
        # the table for correct indexing
        game_state = np.transpose(np.flip(game_state))

        # Create pieces in game and save in dictionary
        # for later monitoring of each pieces position
        self.pieces = self.initiate_pieces(board=game_state)

        # Starting game
        return game_state

    def initiate_board_from_array(self, game_state: Union[NDArray, list]):
        """
        Method for initiating chess board based on array input, 'game_state'.
        Current only supports array with dimension 8x8.
        """
        if isinstance(game_state, list):
            game_state = np.array(game_state)

        # Make sure that elements are integers.
        game_state = game_state.astype(int)

        assert game_state.shape[0] == 8, "Board has to have 8 rows"
        assert game_state.shape[1] == 8, "Board has to have 8 columns"
        self.pieces = self.initiate_pieces(board=game_state)

        return game_state

    def create_piece(self, piece_nr: int, position: tuple) -> AbstractChessPiece:
        """
        Method for creating a chess piece.

        Parameters
        ---
        piece_nr: int
            Piece number that determines which kind of chess piece to create.
            The options are:
                1: White Pawn
                2: White Rook
                3: White Knight
                4: White Bishop
                5: White Queen
                6: White King
                7: Black Pawn
                8: Black Rook
                9: Black Knight
                10: Black Bishop
                11: Black Queen
                12: Black King

        position: tuple
            A tuple where the chess piece is desired to be spawned.
        """
        kwargs = {"position": position, "piece_nr": piece_nr}
        # TODO: Eventually make it possible to
        # open game with lower/upper options
        if (piece_nr < 7) and (piece_nr > 0):
            kwargs["group"] = Group.lower
            kwargs["color"] = Color.white
        elif (piece_nr >= 7) and (piece_nr <= 12):
            kwargs["group"] = Group.upper
            kwargs["color"] = Color.black

        if piece_nr in [1, 7]:
            return Pawn(**kwargs)
        elif piece_nr in [2, 8]:
            return Rook(**kwargs)
        elif piece_nr in [3, 9]:
            return Knight(**kwargs)
        elif piece_nr in [4, 10]:
            return Bishop(**kwargs)
        elif piece_nr in [5, 11]:
            return Queen(**kwargs)
        elif piece_nr in [6, 12]:
            return King(**kwargs)
        else:
            return

    def initiate_pieces(self, board: NDArray) -> Dict[str, list]:
        """
        Method used to initiate and keep track of position
        of each piece in the game.

        Returns a dictionary with white and black pieces:
            {
                'white': [...],
                'black': [...]
            }
        """
        black_pieces = []
        white_pieces = []
        nrows, ncols = board.shape

        # Loop through all entries in array to create pieces
        for i in range(nrows):
            for j in range(ncols):
                created_piece = self.create_piece(piece_nr=board[i, j], position=(i, j))

                # If piece is created, distribute piece
                # to respective color group
                if created_piece:
                    if created_piece.color.name == "white":
                        white_pieces.append(created_piece)
                    elif created_piece.color.name == "black":
                        black_pieces.append(created_piece)

        return {"white": white_pieces, "black": black_pieces}

    def spawn_piece(self, piece_nr: int, position: tuple) -> None:
        created_piece = self.create_piece(piece_nr=piece_nr, position=position)

        if (piece_nr < 7) and (piece_nr > 0):
            self.pieces["white"].append(created_piece)
        elif (piece_nr >= 7) and (piece_nr <= 12):
            self.pieces["black"].append(created_piece)
        else:
            raise ValueError("Nothing was added")

        name = created_piece.name
        color = created_piece.color.name
        position = created_piece.position
        print(f"Spawned a {name} for {color} at position {position}")

    def attack_trajectory(
        self, attacker: AbstractChessPiece, target: AbstractChessPiece
    ) -> List[tuple]:
        """
        Method that returns the path trajectory of an attack (excluding
        positions of the target and the attacker).

        Returns
        ----
        List of positions of the trajectory path. If no trajectory exists,
        then an empty list is returned.
        Note that Pawn, Knight, and King in theory do not have an attack trajectory.
        """

        def _trajectory_type(attacker, target):
            """Evaluate attack trajectory type (diagonal, vertical, or horizontal)"""
            if abs(attacker[0] - target[0]) == abs(attacker[1] - target[1]):
                return "diagonal"
            elif (attacker[0] - target[0] == 0) and (attacker[1] - target[1] != 0):
                return "vertical"
            elif (attacker[0] - target[0] != 0) and (attacker[1] - target[1] == 0):
                return "horizontal"

        trajectory_type = _trajectory_type(
            attacker=attacker.position, target=target.position
        )
        if trajectory_type is None:
            raise ValueError("Trajectory type is unknown")

        piece_with_trajectory = [
            2,
            8,  # Rook
            4,
            10,  # Bishop
            5,
            11,  # Queen
        ]
        if attacker.piece_nr in piece_with_trajectory:
            deltax = target.position[0] - attacker.position[0]
            deltay = target.position[1] - attacker.position[1]

            xsign = int(abs(deltax) / deltax) if deltax != 0 else 1
            ysign = int(abs(deltay) / deltay) if deltay != 0 else 1

            x_axis = range(attacker.position[0], target.position[0], xsign) or [
                attacker.position[0]
            ]

            y_axis = range(attacker.position[1], target.position[1], ysign) or [
                attacker.position[1]
            ]
            if trajectory_type == "horizontal":
                trajectory = [(x, attacker.position[1]) for x in x_axis]
            elif trajectory_type == "vertical":
                trajectory = [(attacker.position[0], y) for y in y_axis]
            else:
                trajectory = [(x, y) for x, y in zip(x_axis, y_axis)]
            return [p for p in trajectory if p != attacker.position]
        return []

    def _threats_to_the_king(
        self, player: Literal["white", "black"]
    ) -> List[AbstractChessPiece]:
        """
        Method for retrieving all pieces that are a threat to
        the king, e.g., enemy units that in one turn can kill the king.
        NOTE: In chess there is only 1 threat to the king at a time.

        Returns a list of chess pieces that are threats.
        """
        threats_id = []
        opponent = self.opponent_of[player]

        # Get king position
        if player == "black":
            king = self.get_black_king()[-1]
        elif player == "white":
            king = self.get_white_king()[-1]

        king_position = king.position

        # Get all possible moves for opponent player
        opponent_actions = self.get_all_possible_actions(opponent)

        # If opponent moves overlap with king position,
        # then there is a check
        for _, pieces in opponent_actions.items():
            for piece in pieces:
                if king_position in piece.get("actions"):
                    threats_id.append(piece.get("id"))

        # Get chess pieces from their IDs
        threats_piece = []
        for threat in threats_id:
            threats_piece.append(self.get_piece_by_id(id=threat, player=opponent))

        return threats_piece

    def _player_is_in_check(self, player: Literal["white", "black"]) -> bool:
        """
        Method for evaluating whether player is in check.

        Returns
        ----
            True, if player is in check.
            False, otherwise.
        """
        threats = self._threats_to_the_king(player)
        return len(threats) > 0

    def _king_cannot_move(self, player: Literal["white", "black"]) -> bool:
        """
        Method for checking whether king can move.

        Returns
        ----
            True,  if king cannot move.
            False, if king can move.
        """
        # Get king position
        if player == "black":
            king = self.get_black_king()[-1]
        elif player == "white":
            king = self.get_white_king()[-1]

        moves = self.get_possible_actions(id=king.id, color=player)

        return len(moves) == 0

    def _cannot_protect_king(self, player: Literal["white", "black"]) -> bool:
        """
        Method for checking whether other units can protect the king.
        For example, by killing the threat or by blocking the hit.

        Returns
        ----
            True, if king cannot be protected.
            False, if king can be protected.
        """
        threats = self._threats_to_the_king(player)

        # If no threats, there is no need to protect
        # hence we return False
        if len(threats) == 0:
            return False

        # The assumption is that there can be only 1 threat
        # at a time in chess.
        if len(threats) > 1:
            # TODO: Logging of errors
            raise GameError(
                "Unknown game state. More than one attacking king at the same time."
            )

        # Retrieve information about the threat
        threat = threats[-1]
        threat_position = threat.position

        ally_actions = self.get_all_possible_actions(player=player)
        if player == "white":
            king = self.get_white_king()[0]
        else:
            king = self.get_black_king()[0]

        attack_trajectory = set(self.attack_trajectory(attacker=threat, target=king))
        for _, pieces in ally_actions.items():
            for piece in pieces:
                ally_piece_actions = set(piece.get("actions"))
                # See whether an ally unit can kill the threat.
                if threat_position in ally_piece_actions:
                    return False

                # See whether ally unit can block the attack.
                if len(attack_trajectory.intersection(ally_piece_actions)) > 0:
                    return False
        return True

    def is_checkmate(self, player: Literal["white", "black"]):
        """
        Method for evaluating game for checkmate.
        """
        is_in_check = self._player_is_in_check(player)
        king_cannot_move = self._king_cannot_move(player)
        cannot_protect_king = self._cannot_protect_king(player)
        return is_in_check and king_cannot_move and cannot_protect_king

    def handle_game(
        self, player: Literal["white", "black"], player_input: dict, game_state: NDArray
    ) -> NDArray:
        """
        Method for making updates according to player input.
        """
        piece_id = player_input.get("id")
        action = player_input.get("action")
        piece = self.get_piece_by_id(id=piece_id, player=player)
        old_position = piece.position
        piece_nr = piece.piece_nr

        # Update piece position in the piece object
        piece.set_position(position=action)

        # Update board
        game_state[old_position] = 0  # empty old position
        game_state[action] = piece_nr  # move chess piece to new position

        # Kill enemy piece if new position hits an enemy
        enemy_pieces = [
            piece for piece in self.pieces.get(self.opponent_of[player]) if piece.status
        ]

        for enemy_piece in enemy_pieces:
            if enemy_piece.position == action:
                # if true then kill enemy and update board
                enemy_piece.kill()

        return game_state

    def _get_all_pieces_by_color(self, color: Literal["white", "black"]):
        """
        Collect all alive pieces by color

        Parameters:
        ---
        color: Literal['white', 'black']
            The color of the chess pieces to retrieve

        """
        return [piece for piece in self.pieces.get(color) if piece.status]

    def _get_enemy_pieces(self, color: Literal["white", "black"]):
        """
        Collect alive chess pieces belonging to the opponent

        Parameters:
        ---
        color: Literal['white', 'black']
            The color of the chess pieces to retrieve

        """
        return self._get_all_pieces_by_color(color=self.opponent_of[color])

    def _get_ally_pieces(self, color: Literal["white", "black"]):
        """
        Collect alive ally chess pieces belonging to the current player turn

        Parameters:
        ---
        color: Literal['white', 'black']
            The color of the chess pieces to retrieve

        """
        return self._get_all_pieces_by_color(color=color)

    def _get_positions_by_color(self, color: Literal["white", "black"]) -> List[tuple]:
        """
        Collect all positions of chess pieces by color.
        This method is different from '_get_all_pieces_by_color' as
        it only returns a list of positions.

        Parameters:
        ---
        color: Literal['white', 'black']
            The color of the chess pieces to retrieve

        """
        return [piece.position for piece in self.pieces.get(color) if piece.status]

    def _get_ally_positions(self, color: Literal["white", "black"]):
        """
        Collect positions of alive ally chess pieces belonging
        to the current player turn.

        Parameters:
        ---
        color: Literal['white', 'black']
            The color of the chess pieces to retrieve

        """
        return self._get_positions_by_color(color=color)

    def _get_enemy_positions(self, color: Literal["white", "black"]):
        """
        Collect positions of alive chess pieces belonging to the opponent.

        Parameters:
        ---
        color: Literal['white', 'black']
            The color of the chess pieces to retrieve
        """
        return self._get_positions_by_color(color=self.opponent_of[color])

    def apply_game_rules(self, piece: Type[AbstractChessPiece]) -> list:
        """
        Method for applying game rules based on piece type.
        """

        if piece.name == "Pawn":
            moves = self.pawn_rules(piece=piece)
        elif piece.name == "Rook":
            moves = self.rook_rules(piece=piece)
        elif piece.name == "Bishop":
            moves = self.bishop_rules(piece=piece)
        elif piece.name == "Knight":
            moves = self.knight_rules(piece=piece)
        elif piece.name == "Queen":
            moves = self.queen_rules(piece=piece)
        elif piece.name == "King":
            moves = self.king_rules(piece=piece)
        else:
            raise ValueError(f"Unknown chess piece [{piece.name}] used.")

        return moves

    def get_piece_by_id(
        self, id: int, player: Literal["white", "black"]
    ) -> Type[AbstractChessPiece]:
        """
        Get piece in game by instance ID.

        Parameters
        ----
        id: int
            the instance id of chess piece
        player: str
            possible values are 'white' or 'black'
        """
        player_pieces = self.pieces.get(player)

        piece = [piece for piece in player_pieces if piece.id == id]

        if len(piece) == 0:
            raise ValueError(f"ID [{id}] does not exist")

        if len(piece) > 1:
            raise ValueError(f"Two or more instances has same id [{id}]")

        return piece[0]

    def get_possible_actions(
        self, id: int, color: Literal["white", "black"]
    ) -> List[tuple]:
        """
        Get all possible actions on specific chess piece
        on desired player color.

        Parameters
        ----
        id: int, the instance id of chess piece
        """
        piece = self.get_piece_by_id(id=id, player=color)

        return self.apply_game_rules(piece)

    def get_all_possible_actions(
        self,
        player: Literal["white", "black"],
    ) -> Dict[str, list]:
        """
        Get possible actions for all pieces that belong to the desired
        player.

        Parameters
        ----
        player, optional 'white' or 'black'
            Determines which player to get all possible actions.

        Returns
        ----
        A dictionary of chess pieces on the board that belong to
        the active player.
        For example:
            {
                'Rook': [{
                    'actions': [],
                    'position': (0, 0),
                    'id': 1234,
                    'piece_type': 2
                }],
                'Pawn': [{
                    'actions': [(0, 2), (0, 3)],
                    'position': (0, 1)
                    'id': 2345
                    'piece_nr': 1
                }, {
                    'actions': [(1, 2), (1, 3)],
                    'position': (1, 1)
                    'id': 2347,
                    'piece_nr': 1
                }],
                'Knight': [{
                    'actions': [(2, 2), (0, 2)],
                    'position': (1, 0)
                    'id': 3456,
                    'piece_nr': 3
                }],
                'King': [{
                    'actions': [],
                    'position': (4, 0)
                    'id': 4567,
                    'piece_nr': 6
                }]
            }

        """
        player_pieces = self._get_ally_pieces(color=player)
        all_piece_actions = dict()
        for piece in player_pieces:

            # Create information dict
            name = piece.name
            color = piece.color.name
            piece_id = piece.id
            piece_info = {
                "actions": self.get_possible_actions(id=piece_id, color=color),
                "id": piece_id,
                "position": piece.position,
                "piece_nr": piece.piece_nr,
            }

            # If key is already created, then append to
            # existing list, else create key in dict.
            if name in all_piece_actions:
                all_piece_actions[name].append(piece_info)
            else:
                all_piece_actions[name] = [piece_info]

        return all_piece_actions

    def _get_pieces(self, name: str, pieces: list):
        """
        Method to filter on list of pieces
        """
        return [piece for piece in pieces if piece.name.lower() == name.lower()]

    def _remove_ally_positions(self, moves: list, color: Color) -> list:
        """
        Removes moves where allies are standing relative to input piece
        """
        ally_positions = self._get_ally_positions(color=color.name)
        moves = [move for move in moves if move not in ally_positions]
        return moves

    def horizontal_move_is_legal(
        self, start_position: tuple, move: tuple, color: Color
    ) -> bool:
        """
        Checks whether move is legal based on position
        of enemy and ally pieces
        """
        x = start_position[0]
        ally_horizontal = self.get_horizontal_moves(
            start_position=start_position,
            moves=self._get_ally_positions(color=color.name),
        )
        # Remove the starting position itself
        ally_horizontal = [
            coord for coord in ally_horizontal if coord != start_position
        ]

        enemy_horizontal = self.get_horizontal_moves(
            start_position=start_position,
            moves=self._get_enemy_positions(color=color.name),
        )
        not_walk_through_allies = all(
            [
                ((pos[0] > move[0]) and (pos[0] > x))
                or ((pos[0] < move[0]) and (pos[0] < x))  # Right  # Left
                for pos in ally_horizontal
            ]
        )
        not_walk_through_enemies = all(
            [
                ((pos[0] >= move[0]) and (pos[0] >= x))
                or ((pos[0] <= move[0]) and (pos[0] <= x))  # Right  # Left
                for pos in enemy_horizontal
            ]
        )
        return not_walk_through_allies and not_walk_through_enemies

    def vertical_move_is_legal(self, start_position: tuple, move: tuple, color: Color):
        """
        Checks whether move is legal based on position
        of enemy and ally pieces
        """
        y = start_position[1]
        ally_vertical = self.get_vertical_moves(
            start_position=start_position,
            moves=self._get_ally_positions(color=color.name),
        )
        # Remove the starting position itself
        ally_vertical = [coord for coord in ally_vertical if coord != start_position]

        enemy_vertical = self.get_vertical_moves(
            start_position=start_position,
            moves=self._get_enemy_positions(color=color.name),
        )
        not_walk_through_allies = all(
            [
                ((pos[1] > move[1]) and (pos[1] > y))
                or ((pos[1] < move[1]) and (pos[1] < y))  # Up  # Down
                for pos in ally_vertical
            ]
        )
        not_walk_through_enemies = all(
            [
                ((pos[1] >= move[1]) and (pos[1] >= y))
                or ((pos[1] <= move[1]) and (pos[1] <= y))  # Up  # Down
                for pos in enemy_vertical
            ]
        )
        return not_walk_through_allies and not_walk_through_enemies

    def handle_blocked_straight_path(
        self, start_position: tuple, piece: Type[AbstractChessPiece]
    ) -> list:
        """
        Removes moves where allies or enemies are blocking the straight path
        """
        moves = piece.get_applied_moves()
        output = []

        vertical_moves = self.get_vertical_moves(
            start_position=start_position, moves=moves
        )
        horizontal_moves = self.get_horizontal_moves(
            start_position=start_position, moves=moves
        )

        # Horizontal
        for move in horizontal_moves:
            if self.horizontal_move_is_legal(
                start_position=start_position, move=move, color=piece.color
            ):
                output.append(move)
        # Vertical
        for move in vertical_moves:
            if self.vertical_move_is_legal(
                start_position=start_position, move=move, color=piece.color
            ):
                output.append(move)

        return output

    def diagonal_incline_move_is_legal(
        self, start_position: tuple, move: tuple, color: Color
    ) -> bool:
        """
        Checks whether move is legal based on position
        of enemy and ally pieces
        """
        x = start_position[0]
        ally_incline = self.get_diagonal_moves_incline(
            start_position=start_position,
            moves=self._get_ally_positions(color=color.name),
        )
        # Remove the starting position itself
        ally_incline = [coord for coord in ally_incline if coord != start_position]

        enemy_incline = self.get_diagonal_moves_incline(
            start_position=start_position,
            moves=self._get_enemy_positions(color=color.name),
        )
        not_walk_through_allies = all(
            [
                ((pos[0] > move[0]) and (pos[0] > x))
                or ((pos[0] < move[0]) and (pos[0] < x))  # Right  # Left
                for pos in ally_incline
            ]
        )
        not_walk_through_enemies = all(
            [
                ((pos[0] >= move[0]) and (pos[0] >= x))
                or ((pos[0] <= move[0]) and (pos[0] <= x))  # Right  # Left
                for pos in enemy_incline
            ]
        )
        return not_walk_through_allies and not_walk_through_enemies

    def diagonal_decline_move_is_legal(
        self, start_position: tuple, move: tuple, color: Color
    ) -> bool:
        """
        Checks whether move is legal based on position
        of enemy and ally pieces
        """
        x = start_position[0]
        ally_decline = self.get_diagonal_moves_decline(
            start_position=start_position,
            moves=self._get_ally_positions(color=color.name),
        )
        # Remove the starting position itself
        ally_decline = [coord for coord in ally_decline if coord != start_position]

        enemy_decline = self.get_diagonal_moves_decline(
            start_position=start_position,
            moves=self._get_enemy_positions(color=color.name),
        )
        not_walk_through_allies = all(
            [
                ((pos[0] > move[0]) and (pos[0] > x))
                or ((pos[0] < move[0]) and (pos[0] < x))  # Right  # Left
                for pos in ally_decline
            ]
        )
        not_walk_through_enemies = all(
            [
                ((pos[0] >= move[0]) and (pos[0] >= x))
                or ((pos[0] <= move[0]) and (pos[0] <= x))  # Right  # Left
                for pos in enemy_decline
            ]
        )
        return not_walk_through_allies and not_walk_through_enemies

    def handle_blocked_diagonal_path(
        self, start_position: tuple, piece: Type[AbstractChessPiece]
    ) -> list:
        """
        Removes moves where allies or enemies are blocking the diagonal path
        """
        moves = piece.get_applied_moves()
        output = []

        incline_moves = self.get_diagonal_moves_incline(
            start_position=start_position, moves=moves
        )
        decline_moves = self.get_diagonal_moves_decline(
            start_position=start_position, moves=moves
        )

        # Incline
        for move in incline_moves:
            if self.diagonal_incline_move_is_legal(
                start_position=start_position, move=move, color=piece.color
            ):
                output.append(move)
        # Decline
        for move in decline_moves:
            if self.diagonal_decline_move_is_legal(
                start_position=start_position, move=move, color=piece.color
            ):
                output.append(move)

        return output

    def _pawn_rule_handle_double_jump(
        self, moves: list, position: tuple, color: Literal["white", "black"]
    ) -> list:
        """
        Private method meant for simplifying pawn rules.
        Method checks whether pawn is in starting position,
        if this is the case, then double jump is allowed.
        Otherwise, the double jump is removed from the allowed movement list.
        """
        start_positions = {
            "white": [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)],
            "black": [(0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)],
        }
        double_jump = {
            "white": (position[0], position[1] + 2),
            "black": (position[0], position[1] - 2),
        }

        # If pawn is not in starting position, then remove double jump
        if position not in start_positions[color] and double_jump[color] in moves:
            moves.remove(double_jump[color])

        return moves

    def _pawn_rule_handle_diagonal_movement(
        self, moves: list, position: tuple, color: Literal["white", "black"]
    ):
        """
        Private method meant for simplifying pawn rules.
        Method checks whether an enemy is in the immediate diagonal cell,
        if so then a diagonal movement is allowed.
        Otherwise, the move is removed from the allowed movement list.
        """
        # Diagonal movement only if enemy is there
        enemy_positions = self._get_enemy_positions(color=color)
        moves = [
            move
            for move in moves
            if not (
                (move[0] - position[0] != 0)  # is diagonal move
                and (move not in enemy_positions)  # does not hit enemy
            )
        ]

        return moves

    def _pawn_rule_enemy_blocking(
        self, moves: list, position: tuple, color: Literal["white", "black"]
    ):
        enemy_positions = self._get_enemy_positions(color=color)
        moves = [
            move
            for move in moves
            if not (
                (move[1] - position[1] != 0)
                and (move[0] - position[0] == 0)  # is straight move
                and (move in enemy_positions)  # hits enemy
            )
        ]
        return moves

    def pawn_rules(self, piece: Type[AbstractChessPiece]):
        moves = piece.get_applied_moves()
        position = piece.position
        color = piece.color.name
        moves = self._pawn_rule_handle_double_jump(
            moves=moves, position=position, color=color
        )

        # Remove moves where allies are standing
        moves = self._remove_ally_positions(moves, color=piece.color)

        # Diagonal movement only if enemy is there
        moves = self._pawn_rule_handle_diagonal_movement(
            moves=moves, position=position, color=color
        )

        # Remove movement where enemy is blocking the straight path
        moves = self._pawn_rule_enemy_blocking(
            moves=moves, position=position, color=color
        )

        # Check for legal horizontal_moves moves
        moves = [
            move
            for move in moves
            if self.vertical_move_is_legal(
                start_position=position, move=move, color=piece.color
            )
        ]
        return moves

    def rook_rules(self, piece: Type[AbstractChessPiece]):
        moves = self.handle_blocked_straight_path(
            start_position=piece.position, piece=piece
        )
        return moves

    def knight_rules(self, piece: Type[AbstractChessPiece]):
        moves = piece.get_applied_moves()
        return self._remove_ally_positions(moves, color=piece.color)

    def bishop_rules(self, piece: Type[AbstractChessPiece]):
        moves = self.handle_blocked_diagonal_path(
            start_position=piece.position, piece=piece
        )
        return moves

    def king_rules(self, piece: Type[AbstractChessPiece]):
        moves = piece.get_applied_moves()
        enemy_pieces = self._get_enemy_pieces(color=piece.color.name)

        enemy_moves = []
        for enemy_piece in enemy_pieces:
            # Pawn and king are treated specially.
            # Pawn: Has a kill-move only if an enemy is diagonal to it.
            #       The kill-move will not be apparent if we apply game rules.
            # King: Not neccesary to apply game rules on enemy king piece.
            #       king_rules, will also become an infinite nested function
            #       if we apply game rules to the kings.
            if enemy_piece.name == "Pawn":
                # Handle enemy pawns specifically
                # Do not handle diagonal movement,
                # because this is needed for the king to
                # not make suicidal movement.

                enemy_position = enemy_piece.position
                enemy_color = enemy_piece.color.name

                # Handle double jump
                pawn_moves = self._pawn_rule_handle_double_jump(
                    moves=enemy_piece.get_applied_moves(),
                    position=enemy_position,
                    color=enemy_color,
                )

                # Handle blocking enemies
                pawn_moves = self._pawn_rule_enemy_blocking(
                    moves=pawn_moves, position=enemy_position, color=enemy_color
                )
                enemy_moves.extend(pawn_moves)

            elif enemy_piece.name == "King":
                enemy_moves.extend(enemy_piece.get_applied_moves())

            else:
                enemy_moves.extend(self.apply_game_rules(piece=enemy_piece))

        moves = [move for move in moves if move not in enemy_moves]

        return self._remove_ally_positions(moves, color=piece.color)

    def queen_rules(self, piece: Type[AbstractChessPiece]):
        # Get the straight pathing that is legally allowed
        straight_moves = self.handle_blocked_straight_path(
            start_position=piece.position, piece=piece
        )

        # Get the diagonal pathing that is legally allowed
        vertical_moves = self.handle_blocked_diagonal_path(
            start_position=piece.position, piece=piece
        )

        return straight_moves + vertical_moves

    def initiate_empty_board(self, grid_size: Optional[int] = 8) -> NDArray:
        """
        Initiates a new game with empty board.
        Mostly for testing purposes
        """
        game_state = np.zeros(shape=(grid_size, grid_size))

        # numpy array indexing works top and down,
        # row on y-axis and column on x-axis,
        # therefore it is necessary to flip and transpose
        # the table for correct indexing
        game_state = np.transpose(np.flip(game_state))

        # Create pieces in game and save in dictionary
        # for later monitoring of each pieces position
        self.pieces = self.initiate_pieces(board=game_state)

        # Starting game
        return game_state

    def get_vertical_moves(self, start_position: tuple, moves: list) -> list:
        """
        Get all moves that are part of the vertical path

        Parameters
        ----
        start_position: tuple
            the starting position of the chess piece
        moves: list
            the list of all moves of chess piece,
            for example, from the method chess_piece.get_applied_moves
        """
        # Fixed x-axis
        x_axis = start_position[0]
        vertical_moves = [move for move in moves if move[0] == x_axis]
        return vertical_moves

    def get_horizontal_moves(self, start_position: tuple, moves: list) -> list:
        """
        Get all moves that are part of the horizontal path

        Parameters
        ----
        start_position: tuple
            the starting position of the chess piece
        moves: list
            the list of all moves of chess piece,
            for example, from the method chess_piece.get_applied_moves
        """
        # Fixed y-axis
        y_axis = start_position[1]
        horizontal_moves = [move for move in moves if move[1] == y_axis]
        return horizontal_moves

    def get_diagonal_moves(self, start_position: tuple, moves: list) -> list:
        """
        Method to get all moves that are diagonal to the
        starting position.
        """

        def is_diagonally_aligned(a: Tuple[int, int], b: Tuple[int, int]) -> bool:
            """
            Helper method to check that coordinate a
            is diagonally aligned with coordinate b.
            Note: This method only works on 2D
            Returns
            ----
                - True if 'a' and 'b' are diagonally aligned
                - False otherwise
            """
            return abs(a[0] - b[0]) == abs(a[1] - b[1])

        return [move for move in moves if is_diagonally_aligned(move, start_position)]

    def get_diagonal_moves_incline(self, start_position: tuple, moves: list) -> list:
        x = start_position[0]
        y = start_position[1]

        # Filter on incline moves that are diagonally aligned to
        # the starting position
        incline_moves = self.get_diagonal_moves(
            start_position=start_position, moves=moves
        )

        # Now filter on incline moves
        incline_moves = [
            move
            for move in incline_moves
            if ((move[0] > x) and (move[1] > y)) or ((move[0] < x) and (move[1] < y))
        ]
        return incline_moves

    def get_diagonal_moves_decline(self, start_position: tuple, moves: list) -> list:
        x = start_position[0]
        y = start_position[1]

        # Filter on incline moves that are diagonally aligned to
        # the starting position
        decline_moves = self.get_diagonal_moves(
            start_position=start_position, moves=moves
        )

        # Now filter on decline moves
        decline_moves = [
            move
            for move in decline_moves
            if ((move[0] < x) and (move[1] > y)) or ((move[0] > x) and (move[1] < y))
        ]
        return decline_moves

    def get_white_pawns(self):
        return self._get_pieces("pawn", self.pieces.get("white", []))

    def get_white_rooks(self):
        return self._get_pieces("rook", self.pieces.get("white", []))

    def get_white_bishops(self):
        return self._get_pieces("bishop", self.pieces.get("white", []))

    def get_white_knights(self):
        return self._get_pieces("knight", self.pieces.get("white", []))

    def get_white_queen(self):
        return self._get_pieces("queen", self.pieces.get("white", []))

    def get_white_king(self):
        return self._get_pieces("king", self.pieces.get("white", []))

    def get_black_pawns(self):
        return self._get_pieces("pawn", self.pieces.get("black", []))

    def get_black_rooks(self):
        return self._get_pieces("rook", self.pieces.get("black", []))

    def get_black_bishops(self):
        return self._get_pieces("bishop", self.pieces.get("black", []))

    def get_black_knights(self):
        return self._get_pieces("knight", self.pieces.get("black", []))

    def get_black_queen(self):
        return self._get_pieces("queen", self.pieces.get("black", []))

    def get_black_king(self):
        return self._get_pieces("king", self.pieces.get("black", []))

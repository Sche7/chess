from chess_pieces import AbstractChessPiece
import numpy as np
from nptyping import NDArray
from typing import Dict, List, Type, Optional, Tuple
from board.files import read_yaml
from chess_pieces.pawn import Pawn
from chess_pieces.bishop import Bishop
from chess_pieces.knight import Knight
from chess_pieces.rook import Rook
from chess_pieces.queen import Queen
from chess_pieces.king import King
from chess_pieces.schema import Color, Group


class Engine:

    switch = {
        'white': 'black',
        'black': 'white'
    }

    def __init__(self, config_path: str):
        self.config = read_yaml(config_path)
        self.representation = self.config['PIECE_REPRESENTATION']
        self.start_state = self.config['GAME_START']
        self.pieces = {}

    def start_game(self) -> None:
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
        self.game_state = game_state
        self.game_over = False
        self.player_turn = 'white'

    def create_piece(self, piece_nr: int, position: tuple) -> None:
        kwargs = {
            'position': position,
            'piece_nr': piece_nr
        }
        # TODO: Eventually make it possible to
        # open game with lower/upper options
        if (piece_nr < 7) and (piece_nr > 0):
            kwargs['group'] = Group.lower
            kwargs['color'] = Color.white
        elif (piece_nr >= 7) and (piece_nr <= 12):
            kwargs['group'] = Group.upper
            kwargs['color'] = Color.black

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
                created_piece = self.create_piece(
                                    piece_nr=board[i, j],
                                    position=(i, j)
                                )

                # If piece is created, distribute piece
                # to respective color group
                if created_piece:
                    if created_piece.color.name == 'white':
                        white_pieces.append(created_piece)
                    elif created_piece.color.name == 'black':
                        black_pieces.append(created_piece)

        return {
            'white': white_pieces,
            'black': black_pieces
        }

    def spawn_piece(self, piece_nr: int, position: tuple) -> None:
        created_piece = self.create_piece(piece_nr=piece_nr, position=position)

        if (piece_nr < 7) and (piece_nr > 0):
            self.pieces['white'].append(created_piece)
        elif (piece_nr >= 7) and (piece_nr <= 12):
            self.pieces['black'].append(created_piece)
        else:
            raise ValueError('Nothing was added')

        name = created_piece.name
        color = created_piece.color.name
        position = created_piece.position
        print(f'Spawned a {name} for {color} at position {position}')

    def check_game_state(self):
        pass

    def handle_game(self, player_input: dict) -> None:
        """
        Method for making updates according to player input.
        """

        if not player_input:
            self.game_over = True
            print(f'Player {self.player_turn} surrendered. Game over.')
            return

        piece_id = player_input.get('id')
        action = player_input.get('action')
        piece = self.get_piece_by_id(
            id=piece_id,
            player=self.player_turn
        )
        old_position = piece.position
        piece_nr = piece.piece_nr

        # Update piece position in the piece object
        piece.set_position(position=action)

        # Update board
        self.game_state[old_position] = 0   # empty old position
        self.game_state[action] = piece_nr  # move chess piece to new position

        # Kill enemy piece if new position hits an enemy
        enemy_pieces = self.get_enemy_pieces()
        for enemy_piece in enemy_pieces:
            if enemy_piece.position == action:
                # if true then kill enemy and update board
                enemy_piece.kill()

    def get_enemy_pieces(self):
        """
        Collect alive enemy pieces
        """
        return [
            piece for piece in
            self.pieces.get(self.switch[self.player_turn]) if piece.status
        ]

    def get_ally_pieces(self):
        """
        Collect alive ally pieces
        """
        return [
            piece for piece in
            self.pieces.get(self.player_turn) if piece.status
        ]

    def get_ally_positions(self):
        """
        Collect positions of alive ally pieces
        """
        return [
            piece.position for piece in
            self.pieces.get(self.player_turn) if piece.status
        ]

    def get_enemy_positions(self):
        """
        Collect positions of alive enemy pieces
        """

        return [
            piece.position for piece in
            self.pieces.get(self.switch[self.player_turn]) if piece.status
        ]

    def apply_game_rules(self, piece: Type[AbstractChessPiece]) -> list:

        if piece.name == 'Pawn':
            moves = self.pawn_rules(piece=piece)
        elif piece.name == 'Rook':
            moves = self.rook_rules(piece=piece)
        elif piece.name == 'Bishop':
            moves = self.bishop_rules(piece=piece)
        elif piece.name == 'Knight':
            moves = self.knight_rules(piece=piece)
        elif piece.name == 'Queen':
            moves = self.queen_rules(piece=piece)
        elif piece.name == 'King':
            moves = self.king_rules(piece=piece)
        else:
            raise ValueError(f'Unknown chess piece [{piece.name}] used.')

        return moves

    def get_piece_by_id(self, id: int, player: str) -> Type[AbstractChessPiece]:
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
            raise ValueError(f'ID [{id}] does not exist')

        if len(piece) > 1:
            raise ValueError(f'Two or more instances has same id [{id}]')

        return piece[0]

    def get_possible_actions(self, id: int) -> List[tuple]:
        """
        Get all possible actions on specific chess piece
        on players turn.

        Parameters
        ----
        id: int, the instance id of chess piece
        """
        piece = self.get_piece_by_id(id=id, player=self.player_turn)

        return self.apply_game_rules(piece)

    def get_all_possible_actions(self) -> Dict[str, list]:
        """
        Get possible moves for all pieces that current player
        has on the board.

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
        player_pieces = self.get_ally_pieces()
        all_piece_actions = dict()
        for piece in player_pieces:

            # Create information dict
            name = piece.name
            piece_info = {
                    'actions': self.get_possible_actions(id=piece.id),
                    'id': piece.id,
                    'position': piece.position,
                    'piece_nr': piece.piece_nr
                }

            # If key is already created, then append to
            # exitsting list, else create key in dict.
            if name in all_piece_actions:
                all_piece_actions[name].append(piece_info)
            else:
                all_piece_actions[name] = [piece_info]

        return all_piece_actions

    def switch_turn(self) -> None:
        self.player_turn = self.switch[self.player_turn]

    def _get_pieces(self, name: str, pieces: list):
        """
        Method to filter on list of pieces
        """
        return [
            piece for piece in pieces
            if piece.name.lower() == name.lower()
        ]

    def _remove_ally_positions(self, moves: list) -> list:
        """
        Removes moves where allies are standing
        """
        ally_positions = self.get_ally_positions()
        moves = [
            move for move in moves if move not in ally_positions
        ]
        return moves

    def horizontal_move_is_legal(
        self,
        start_position: tuple,
        move: tuple
    ) -> bool:
        """
        Checks whether move is legal based on position
        of enemy and ally pieces
        """
        x = start_position[0]
        ally_horizontal = self.get_horizontal_moves(
            start_position=start_position,
            moves=self.get_ally_positions()
        )
        # Remove the starting position itself
        ally_horizontal = [
            coord for coord in ally_horizontal if coord != start_position
        ]

        enemy_horizontal = self.get_horizontal_moves(
            start_position=start_position,
            moves=self.get_enemy_positions()
        )
        not_walk_through_allies = all([
            ((pos[0] > move[0]) and (pos[0] > x)) or   # Right
            ((pos[0] < move[0]) and (pos[0] < x))      # Left
            for pos in ally_horizontal
        ])
        not_walk_through_enemies = all([
            ((pos[0] >= move[0]) and (pos[0] >= x)) or   # Right
            ((pos[0] <= move[0]) and (pos[0] <= x))      # Left
            for pos in enemy_horizontal
        ])
        return not_walk_through_allies and not_walk_through_enemies

    def vertical_move_is_legal(
        self,
        start_position: tuple,
        move: tuple
    ):
        """
        Checks whether move is legal based on position
        of enemy and ally pieces
        """
        y = start_position[1]
        ally_vertical = self.get_vertical_moves(
            start_position=start_position,
            moves=self.get_ally_positions()
        )
        # Remove the starting position itself
        ally_vertical = [
            coord for coord in ally_vertical if coord != start_position
        ]

        enemy_vertical = self.get_vertical_moves(
            start_position=start_position,
            moves=self.get_enemy_positions()
        )
        not_walk_through_allies = all([
            ((pos[1] > move[1]) and (pos[1] > y)) or   # Up
            ((pos[1] < move[1]) and (pos[1] < y))      # Down
            for pos in ally_vertical
        ])
        not_walk_through_enemies = all([
            ((pos[1] >= move[1]) and (pos[1] >= y)) or   # Up
            ((pos[1] <= move[1]) and (pos[1] <= y))      # Down
            for pos in enemy_vertical
        ])
        return not_walk_through_allies and not_walk_through_enemies

    def handle_blocked_straight_path(
        self,
        start_position: tuple,
        moves: list
    ) -> list:
        """
        Removes moves where allies or enemies are blocking the straight path
        """
        output = []

        vertical_moves = self.get_vertical_moves(
            start_position=start_position,
            moves=moves
        )
        horizontal_moves = self.get_horizontal_moves(
            start_position=start_position,
            moves=moves
        )

        # Horizontal
        for move in horizontal_moves:
            if self.horizontal_move_is_legal(
                start_position=start_position,
                move=move
            ):
                output.append(move)
        # Vertical
        for move in vertical_moves:
            if self.vertical_move_is_legal(
                start_position=start_position,
                move=move
            ):
                output.append(move)

        return output

    def diagonal_incline_move_is_legal(
        self,
        start_position: tuple,
        move: tuple
    ) -> bool:
        """
        Checks whether move is legal based on position
        of enemy and ally pieces
        """
        x = start_position[0]
        ally_incline = self.get_diagonal_moves_incline(
            start_position=start_position,
            moves=self.get_ally_positions()
        )
        # Remove the starting position itself
        ally_incline = [
            coord for coord in ally_incline if coord != start_position
        ]

        enemy_incline = self.get_diagonal_moves_incline(
            start_position=start_position,
            moves=self.get_enemy_positions()
        )
        not_walk_through_allies = all([
            ((pos[0] > move[0]) and (pos[0] > x)) or   # Right
            ((pos[0] < move[0]) and (pos[0] < x))      # Left
            for pos in ally_incline
        ])
        not_walk_through_enemies = all([
            ((pos[0] >= move[0]) and (pos[0] >= x)) or   # Right
            ((pos[0] <= move[0]) and (pos[0] <= x))      # Left
            for pos in enemy_incline
        ])
        return not_walk_through_allies and not_walk_through_enemies

    def diagonal_decline_move_is_legal(
        self,
        start_position: tuple,
        move: tuple
    ) -> bool:
        """
        Checks whether move is legal based on position
        of enemy and ally pieces
        """
        x = start_position[0]
        ally_decline = self.get_diagonal_moves_decline(
            start_position=start_position,
            moves=self.get_ally_positions()
        )
        # Remove the starting position itself
        ally_decline = [
            coord for coord in ally_decline if coord != start_position
        ]

        enemy_decline = self.get_diagonal_moves_decline(
            start_position=start_position,
            moves=self.get_enemy_positions()
        )
        not_walk_through_allies = all([
            ((pos[0] > move[0]) and (pos[0] > x)) or   # Right
            ((pos[0] < move[0]) and (pos[0] < x))      # Left
            for pos in ally_decline
        ])
        not_walk_through_enemies = all([
            ((pos[0] >= move[0]) and (pos[0] >= x)) or   # Right
            ((pos[0] <= move[0]) and (pos[0] <= x))      # Left
            for pos in enemy_decline
        ])
        return not_walk_through_allies and not_walk_through_enemies

    def handle_blocked_diagonal_path(
        self,
        start_position: tuple,
        moves: list
    ) -> list:
        """
        Removes moves where allies or enemies are blocking the diagonal path
        """
        output = []

        incline_moves = self.get_diagonal_moves_incline(
            start_position=start_position,
            moves=moves
        )
        decline_moves = self.get_diagonal_moves_decline(
            start_position=start_position,
            moves=moves
        )

        # Incline
        for move in incline_moves:
            if self.diagonal_incline_move_is_legal(
                start_position=start_position,
                move=move
            ):
                output.append(move)
        # Decline
        for move in decline_moves:
            if self.diagonal_decline_move_is_legal(
                start_position=start_position,
                move=move
            ):
                output.append(move)

        return output

    def pawn_rules(self, piece: Type[AbstractChessPiece]):
        moves = piece.get_applied_moves()
        position = piece.position
        start_positions = {
            'white': [
                (0, 1), (1, 1), (2, 1),
                (3, 1), (4, 1), (5, 1),
                (6, 1), (7, 1)
            ],
            'black': [
                (0, 6), (1, 6), (2, 6),
                (3, 6), (4, 6), (5, 6),
                (6, 6), (7, 6)
            ]
        }
        double_jump = {
            'white': (position[0], position[1] + 2),
            'black': (position[0], position[1] - 2)
        }

        color = piece.color.name
        # If pawn is not in starting position, then remove double jump
        if (position not in start_positions[color] and
                double_jump[color] in moves):
            moves.remove(double_jump[color])

        # Remove moves where allies are standing
        moves = self._remove_ally_positions(moves)

        # Diagonal movement only if enemy is there
        enemy_positions = self.get_enemy_positions()
        moves = [
            move for move in moves if not (
                (move[0] - position[0] != 0)        # is diagonal move
                and (move not in enemy_positions)   # does not hit enemy
            )
        ]

        # Remove movement where enemy is blocking the straight path
        moves = [
            move for move in moves if not (
                (move[1] - position[1] != 0) and (move[0] - position[0] == 0)    # is straight move
                and (move in enemy_positions)                                    # hits enemy
            )
        ]
        return moves

    def rook_rules(self, piece: Type[AbstractChessPiece]):
        moves = self.handle_blocked_straight_path(
            start_position=piece.position,
            moves=piece.get_applied_moves()
        )
        return moves

    def knight_rules(self, piece: Type[AbstractChessPiece]):
        moves = piece.get_applied_moves()
        return self._remove_ally_positions(moves)

    def bishop_rules(self, piece: Type[AbstractChessPiece]):
        moves = self.handle_blocked_diagonal_path(
            start_position=piece.position,
            moves=piece.get_applied_moves()
        )
        return moves

    def king_rules(self, piece: Type[AbstractChessPiece]):
        moves = piece.get_applied_moves()

        enemy_pieces = self.get_enemy_pieces()

        enemy_moves = []
        for enemy_piece in enemy_pieces:
            enemy_moves.extend(enemy_piece.get_applied_moves())

        moves = [
            move for move in moves if move not in enemy_moves
        ]

        return self._remove_ally_positions(moves)

    def queen_rules(self, piece: Type[AbstractChessPiece]):
        # Get the straight pathing that is legally allowed
        straight_moves = self.handle_blocked_straight_path(
            start_position=piece.position,
            moves=piece.get_applied_moves()
        )

        # Get the diagonal pathing that is legally allowed
        vertical_moves = self.handle_blocked_diagonal_path(
            start_position=piece.position,
            moves=piece.get_applied_moves()
        )

        return straight_moves + vertical_moves

    def initiate_empty_board(self, grid_size: Optional[int] = 8) -> None:
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
        self.game_state = game_state
        self.game_over = False
        self.player_turn = 'white'

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
        vertical_moves = [
            move for move in moves if move[0] == x_axis
        ]
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
        horizontal_moves = [
            move for move in moves if move[1] == y_axis
        ]
        return horizontal_moves

    def get_diagonal_moves(
        self,
        start_position: tuple,
        moves: list
    ) -> list:
        """
        Method to get all moves that are diagonal to the
        starting position.
        """
        def is_diagonally_aligned(
            a: Tuple[int, int], b: Tuple[int, int]
        ) -> bool:
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
        return [
            move for move in moves if is_diagonally_aligned(
                move, start_position
            )
        ]

    def get_diagonal_moves_incline(
        self,
        start_position: tuple,
        moves: list
    ) -> list:
        x = start_position[0]
        y = start_position[1]

        # Filter on incline moves that are diagonally aligned to
        # the starting position
        incline_moves = self.get_diagonal_moves(
            start_position=start_position,
            moves=moves
        )

        # Now filter on incline moves
        incline_moves = [
            move for move in incline_moves if
            ((move[0] > x) and (move[1] > y)) or
            ((move[0] < x) and (move[1] < y))
        ]
        return incline_moves

    def get_diagonal_moves_decline(
        self,
        start_position: tuple,
        moves: list
    ) -> list:
        x = start_position[0]
        y = start_position[1]

        # Filter on incline moves that are diagonally aligned to
        # the starting position
        decline_moves = self.get_diagonal_moves(
            start_position=start_position,
            moves=moves
        )

        # Now filter on decline moves
        decline_moves = [
            move for move in decline_moves if
            ((move[0] < x) and (move[1] > y)) or
            ((move[0] > x) and (move[1] < y))
        ]
        return decline_moves

    def get_white_pawns(self):
        return self._get_pieces('pawn', self.pieces.get('white', []))

    def get_white_rooks(self):
        return self._get_pieces('rook', self.pieces.get('white', []))

    def get_white_bishops(self):
        return self._get_pieces('bishop', self.pieces.get('white', []))

    def get_white_knights(self):
        return self._get_pieces('knight', self.pieces.get('white', []))

    def get_white_queen(self):
        return self._get_pieces('queen', self.pieces.get('white', []))

    def get_white_king(self):
        return self._get_pieces('king', self.pieces.get('white', []))

    def get_black_pawns(self):
        return self._get_pieces('pawn', self.pieces.get('black', []))

    def get_black_rooks(self):
        return self._get_pieces('rook', self.pieces.get('black', []))

    def get_black_bishops(self):
        return self._get_pieces('bishop', self.pieces.get('black', []))

    def get_black_knights(self):
        return self._get_pieces('knight', self.pieces.get('black', []))

    def get_black_queen(self):
        return self._get_pieces('queen', self.pieces.get('black', []))

    def get_black_king(self):
        return self._get_pieces('king', self.pieces.get('black', []))

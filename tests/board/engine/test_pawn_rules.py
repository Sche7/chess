import pytest

from src.board.engine import Engine


def test_pawn_start_game(config_path):
    engine = Engine(config_path)
    engine.start_game()

    white_pawns = engine.get_white_pawns()

    for pawn in white_pawns:
        position = pawn.position

        expected_moves = [
            (position[0], position[1] + 1),
            (position[0], position[1] + 2),
        ]
        assert set(engine.pawn_rules(piece=pawn)) == set(expected_moves)


def test_pawn_no_blocking(config_path):
    engine = Engine(config_path)
    engine.initiate_empty_board()

    # See that board is empty
    assert len(engine.pieces["white"]) == 0
    assert len(engine.pieces["black"]) == 0

    # Spawn white pawn
    engine.spawn_piece(piece_nr=1, position=(4, 4))

    # See that one white pawn has spawned
    assert len(engine.pieces["white"]) == 1

    white_pawn = engine.pieces["white"][0]

    # See that pawn only has 1 move option
    moves = engine.apply_game_rules(white_pawn)
    assert (4, 5) in moves
    assert len(moves) == 1


def test_pawn_ally_blocking(config_path):
    engine = Engine(config_path)
    engine.initiate_empty_board()

    # See that board is empty
    assert len(engine.pieces["white"]) == 0
    assert len(engine.pieces["black"]) == 0

    # Spawn white pawn
    engine.spawn_piece(piece_nr=1, position=(4, 4))

    # Spawn another white pawn
    engine.spawn_piece(piece_nr=1, position=(4, 5))

    # See that two white pawns are spawned
    assert len(engine.pieces["white"]) == 2

    white_pawn_4_4, white_pawn_4_5 = engine.pieces["white"]

    # See that first white pawn is blocked
    moves_4_4 = engine.apply_game_rules(white_pawn_4_4)
    assert white_pawn_4_4.position == (4, 4)
    assert len(moves_4_4) == 0

    # See that second white pawn can move
    moves_4_5 = engine.apply_game_rules(white_pawn_4_5)
    assert white_pawn_4_5.position == (4, 5)
    assert len(moves_4_5) == 1
    assert (4, 6) in moves_4_5


def test_pawn_killer_move(config_path):
    engine = Engine(config_path)
    engine.initiate_empty_board()

    # See that board is empty
    assert len(engine.pieces["white"]) == 0
    assert len(engine.pieces["black"]) == 0

    # Spawn white pawn
    engine.spawn_piece(piece_nr=1, position=(4, 4))

    # Spawn black pawn
    engine.spawn_piece(piece_nr=7, position=(5, 5))
    white_pawn = engine.pieces["white"][0]
    black_pawn = engine.pieces["black"][0]
    # See that white pawn can kill black pawn
    moves = engine.apply_game_rules(white_pawn)
    assert black_pawn.position in moves

    # See that double jump is removed
    position = white_pawn.position
    assert (position[0], position[1] + 2) not in moves

    # See that other diagonal move is removed
    assert (3, 5) not in moves

    # See that forward move is there
    assert (4, 5) in moves


def test_pawn_enemy_blocking(config_path):
    """
    Test that pawn is blocked by enemy
    if enemy unit is on the straight path.
    """
    engine = Engine(config_path)
    engine.initiate_empty_board()

    # See that board is empty
    assert len(engine.pieces["white"]) == 0
    assert len(engine.pieces["black"]) == 0

    # Spawn white pawn
    engine.spawn_piece(piece_nr=1, position=(4, 4))

    # Spawn black pawn
    engine.spawn_piece(piece_nr=7, position=(4, 5))

    # See that one white pawn is spawned
    assert len(engine.pieces["white"]) == 1

    # See that black white pawn is spawned
    assert len(engine.pieces["black"]) == 1

    white_pawn_4_4 = engine.pieces["white"][0]
    black_pawn_4_5 = engine.pieces["black"][0]

    # See that first white pawn is blocked
    moves_4_4 = engine.apply_game_rules(white_pawn_4_4)
    assert white_pawn_4_4.position == (4, 4)
    assert len(moves_4_4) == 0

    # See that black pawn is also blocked
    moves_4_5 = engine.apply_game_rules(black_pawn_4_5)
    assert black_pawn_4_5.position == (4, 5)
    assert len(moves_4_5) == 0


@pytest.mark.parametrize("blocker", ["enemy", "ally"])
def test_pawn_double_jump_blocked(config_path, blocker):
    """
    Test that pawn cannot double jump
    if an enemy or ally i blocking the path
    in start position.
    """
    engine = Engine(config_path)
    engine.initiate_empty_board()

    # See that board is empty
    assert len(engine.pieces["white"]) == 0
    assert len(engine.pieces["black"]) == 0

    # Spawn white pawn
    engine.spawn_piece(piece_nr=1, position=(1, 1))

    if blocker == "ally":
        # Spawn white rook
        engine.spawn_piece(piece_nr=2, position=(1, 2))
        # See that two white chess pieces is spawned
        assert len(engine.pieces["white"]) == 2
    else:
        # Spawn black pawn
        engine.spawn_piece(piece_nr=7, position=(1, 2))
        # See that one white pawn is spawned
        assert len(engine.pieces["white"]) == 1

        # See that black white pawn is spawned
        assert len(engine.pieces["black"]) == 1

    white_pawn_1_1 = engine.get_white_pawns()[0]

    # See that first white pawn is blocked
    moves_1_1 = engine.apply_game_rules(white_pawn_1_1)

    assert white_pawn_1_1.position == (1, 1)
    assert len(moves_1_1) == 0

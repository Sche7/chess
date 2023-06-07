from src.board.engine import Engine


def test_knight_start_game(config_path):
    engine = Engine(config_path)
    engine.start_game()

    white_knights = engine.get_white_knights()

    expected_moves = [[(0, 2), (2, 2)], [(7, 2), (5, 2)]]

    for i, knight in enumerate(white_knights):
        moves = set(engine.knight_rules(piece=knight))
        assert moves == set(expected_moves[i])


def test_knight_no_blocking(config_path):
    engine = Engine(config_path)
    engine.initiate_empty_board()

    expected_moves = [
        (2, 5),
        (2, 3),  # left
        (6, 5),
        (6, 3),  # right
        (5, 6),
        (3, 6),  # up
        (5, 2),
        (3, 2),  # down
    ]
    # See that board is empty
    assert len(engine.pieces["white"]) == 0
    assert len(engine.pieces["black"]) == 0

    # Spawn white knight
    engine.spawn_piece(piece_nr=3, position=(4, 4))

    # See that one white knight has spawned
    assert len(engine.pieces["white"]) == 1

    white_knight = engine.pieces["white"][0]

    # See that knight has 8 move options
    moves = engine.apply_game_rules(white_knight)
    for move in moves:
        assert move in expected_moves
    assert len(moves) == 8


def test_knight_ally_blocking(config_path):
    engine = Engine(config_path)
    engine.initiate_empty_board()

    engine = Engine(config_path)
    engine.initiate_empty_board()

    expected_moves = [
        (2, 3),  # left
        (6, 5),
        (6, 3),  # right
        (3, 6),  # up
        (5, 2),
        (3, 2),  # down
    ]
    # See that board is empty
    assert len(engine.pieces["white"]) == 0
    assert len(engine.pieces["black"]) == 0

    # Spawn white knight
    engine.spawn_piece(piece_nr=3, position=(4, 4))

    # Spawn white pawn at (2, 5)
    engine.spawn_piece(piece_nr=1, position=(2, 5))

    # Spawn white pawn at (5, 6)
    engine.spawn_piece(piece_nr=1, position=(5, 6))

    # See that three white pieces are spawned
    assert len(engine.pieces["white"]) == 3

    white_knight = engine.pieces["white"][0]

    # See that knight has 8 move options
    moves = engine.apply_game_rules(white_knight)
    for move in moves:
        assert move in expected_moves
    assert len(moves) == 6


def test_knight_killer_move(config_path):
    engine = Engine(config_path)
    engine.initiate_empty_board()

    expected_moves = [
        (2, 5),
        (2, 3),  # left
        (6, 5),
        (6, 3),  # right
        (5, 6),
        (3, 6),  # up
        (5, 2),
        (3, 2),  # down
    ]
    # See that board is empty
    assert len(engine.pieces["white"]) == 0
    assert len(engine.pieces["black"]) == 0

    # Spawn white knight
    engine.spawn_piece(piece_nr=3, position=(4, 4))

    # Spawn black pawn at (2, 5)
    engine.spawn_piece(piece_nr=7, position=(2, 5))

    # Spawn black pawn at (5, 6)
    engine.spawn_piece(piece_nr=7, position=(5, 6))

    white_knight = engine.pieces["white"][0]
    black_pawns = engine.pieces["black"]
    # See that white knight can kill black pawns
    moves = engine.apply_game_rules(white_knight)
    for pawn in black_pawns:
        assert pawn.position in moves

    # See that knight has 8 move options
    for move in moves:
        assert move in expected_moves
    assert len(moves) == 8

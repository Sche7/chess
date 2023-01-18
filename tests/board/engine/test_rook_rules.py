from board.engine import Engine


def test_rook_start_game(config_path):
    engine = Engine(config_path)
    engine.start_game()

    white_rooks = engine.get_white_rooks()

    for rook in white_rooks:
        assert len(engine.apply_game_rules(piece=rook)) == 0


def test_rook_no_blocking(config_path):
    engine = Engine(config_path)
    engine.initiate_empty_board()

    # See that board is empty
    assert len(engine.pieces["white"]) == 0
    assert len(engine.pieces["black"]) == 0

    # Spawn white rook
    engine.spawn_piece(piece_nr=2, position=(4, 4))
    expected_moves = [
        (0, 4),
        (1, 4),
        (2, 4),
        (3, 4),
        (5, 4),
        (6, 4),
        (7, 4),
        (4, 0),
        (4, 1),
        (4, 2),
        (4, 3),
        (4, 5),
        (4, 6),
        (4, 7),
    ]

    # See that one white rook has spawned
    assert len(engine.pieces["white"]) == 1

    white_rook = engine.pieces["white"][0]

    moves = engine.apply_game_rules(white_rook)
    for move in moves:
        assert move in expected_moves
    assert len(expected_moves) == len(moves)


def test_rook_ally_blocking(config_path):
    engine = Engine(config_path)
    engine.initiate_empty_board()

    # See that board is empty
    assert len(engine.pieces["white"]) == 0
    assert len(engine.pieces["black"]) == 0

    # Spawn white rook
    engine.spawn_piece(piece_nr=2, position=(4, 4))

    # Spawn another white pawn
    engine.spawn_piece(piece_nr=1, position=(4, 3))

    expected_moves = [
        (0, 4),
        (1, 4),
        (2, 4),
        (3, 4),
        (5, 4),
        (6, 4),
        (7, 4),
        (4, 5),
        (4, 6),
        (4, 7),
    ]

    # See that two white pieces are spawned
    assert len(engine.pieces["white"]) == 2

    white_rook = engine.pieces["white"][0]

    # See that pawn only has 1 move option
    moves = engine.apply_game_rules(white_rook)
    for move in moves:
        assert move in expected_moves
    assert len(expected_moves) == len(moves)


def test_rook_killer_move(config_path):
    engine = Engine(config_path)
    engine.initiate_empty_board()

    # See that board is empty
    assert len(engine.pieces["white"]) == 0
    assert len(engine.pieces["black"]) == 0

    # Spawn white rook
    engine.spawn_piece(piece_nr=2, position=(4, 4))

    # Spawn black pawn
    engine.spawn_piece(piece_nr=7, position=(4, 3))

    expected_moves = [
        (0, 4),
        (1, 4),
        (2, 4),
        (3, 4),
        (5, 4),
        (6, 4),
        (7, 4),
        (4, 3),
        (4, 5),
        (4, 6),
        (4, 7),
    ]

    # See that one white piece is spawned
    assert len(engine.pieces["white"]) == 1
    # See that one black piece is spawned
    assert len(engine.pieces["black"]) == 1

    white_rook = engine.pieces["white"][0]

    # See that pawn only has 1 move option
    moves = engine.apply_game_rules(white_rook)
    for move in moves:
        assert move in expected_moves
    assert len(expected_moves) == len(moves)

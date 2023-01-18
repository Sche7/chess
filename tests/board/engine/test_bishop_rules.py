from board.engine import Engine


def test_bishop_start_game(config_path):
    engine = Engine(config_path)
    engine.start_game()

    white_bishops = engine.get_white_bishops()

    for bishop in white_bishops:
        assert len(engine.apply_game_rules(piece=bishop)) == 0


def test_bishop_no_blocking(config_path):
    engine = Engine(config_path)
    engine.initiate_empty_board()

    # See that board is empty
    assert len(engine.pieces["white"]) == 0
    assert len(engine.pieces["black"]) == 0

    # Spawn white bishop
    engine.spawn_piece(piece_nr=4, position=(4, 4))
    expected_moves = [
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3),
        (5, 5),
        (6, 6),
        (7, 7),
        (5, 3),
        (6, 2),
        (7, 1),
        (3, 5),
        (2, 6),
        (1, 7),
    ]

    # See that one white bishop has spawned
    assert len(engine.pieces["white"]) == 1

    white_bishop = engine.pieces["white"][0]

    # See that pawn only has 1 move option
    moves = engine.apply_game_rules(white_bishop)
    for move in moves:
        assert move in expected_moves
    assert len(expected_moves) == len(moves)


def test_bishop_ally_blocking(config_path):
    engine = Engine(config_path)
    engine.initiate_empty_board()

    # See that board is empty
    assert len(engine.pieces["white"]) == 0
    assert len(engine.pieces["black"]) == 0

    # Spawn white bishop
    engine.spawn_piece(piece_nr=4, position=(4, 4))

    # Spawn another white pawn
    engine.spawn_piece(piece_nr=1, position=(5, 3))

    expected_moves = [
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3),
        (5, 5),
        (6, 6),
        (7, 7),
        (3, 5),
        (2, 6),
        (1, 7),
    ]

    # See that two white pieces are spawned
    assert len(engine.pieces["white"]) == 2

    white_bishop = engine.pieces["white"][0]

    moves = engine.apply_game_rules(white_bishop)
    for move in moves:
        assert move in expected_moves
    assert len(expected_moves) == len(moves)


def test_bishop_killer_move(config_path):
    engine = Engine(config_path)
    engine.initiate_empty_board()

    # See that board is empty
    assert len(engine.pieces["white"]) == 0
    assert len(engine.pieces["black"]) == 0

    # Spawn white bishop
    engine.spawn_piece(piece_nr=4, position=(4, 4))

    # Spawn black pawn
    engine.spawn_piece(piece_nr=7, position=(5, 3))

    expected_moves = [
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3),
        (5, 5),
        (6, 6),
        (7, 7),
        (5, 3),
        (3, 5),
        (2, 6),
        (1, 7),
    ]

    # See that one white piece is spawned
    assert len(engine.pieces["white"]) == 1
    # See that one black piece is spawned
    assert len(engine.pieces["black"]) == 1

    white_bishop = engine.pieces["white"][0]

    # See that pawn only has 1 move option
    moves = engine.apply_game_rules(white_bishop)
    for move in moves:
        assert move in expected_moves
    assert len(expected_moves) == len(moves)

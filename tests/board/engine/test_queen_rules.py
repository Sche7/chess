from board.engine import Engine


def test_queen_start_game(config_path):
    """
    See that queen starts with no available moves
    """
    engine = Engine(config_path)
    engine.start_game()

    white_queen = engine.get_white_queen()[-1]
    assert len(engine.queen_rules(piece=white_queen)) == 0


def test_queen_ally_blocking_straight(config_path):
    """
    Test that queen is blocked by ally pieces
    as expected.
    """
    engine = Engine(config_path)
    engine.initiate_empty_board()

    # See that board is empty
    assert len(engine.pieces["white"]) == 0
    assert len(engine.pieces["black"]) == 0

    # Spawn white queen
    engine.spawn_piece(piece_nr=5, position=(0, 0))

    # Spawn a pawn beside queen
    engine.spawn_piece(piece_nr=1, position=(0, 1))

    # See that two white pieces are spawned
    assert len(engine.pieces["white"]) == 2

    white_queen, _ = engine.pieces["white"]

    # See that first white pawn is blocked
    queen_moves = engine.apply_game_rules(white_queen)
    expected_queen_moves = [(i, 0) for i in range(1, 8)] + [(i, i) for i in range(1, 8)]

    assert white_queen.position == (0, 0)
    assert set(queen_moves) == set(expected_queen_moves)


def test_queen_ally_blocking_diagonal(config_path):
    """
    Test that queen is blocked by ally pieces
    as expected.
    """
    engine = Engine(config_path)
    engine.initiate_empty_board()

    # See that board is empty
    assert len(engine.pieces["white"]) == 0
    assert len(engine.pieces["black"]) == 0

    # Spawn white queen
    engine.spawn_piece(piece_nr=5, position=(0, 0))

    # Spawn a pawn beside queen
    engine.spawn_piece(piece_nr=1, position=(1, 1))

    # See that two white pieces are spawned
    assert len(engine.pieces["white"]) == 2

    white_queen, _ = engine.pieces["white"]

    # See that first white pawn is blocked
    queen_moves = engine.apply_game_rules(white_queen)
    expected_queen_moves = [(i, 0) for i in range(1, 8)] + [(0, i) for i in range(1, 8)]

    assert white_queen.position == (0, 0)
    assert set(queen_moves) == set(expected_queen_moves)


def test_queen_enemy_blocking_straight(config_path):
    """
    Test that queen is blocked by ally pieces
    as expected.
    """
    engine = Engine(config_path)
    engine.initiate_empty_board()

    # See that board is empty
    assert len(engine.pieces["white"]) == 0
    assert len(engine.pieces["black"]) == 0

    # Spawn white queen
    engine.spawn_piece(piece_nr=5, position=(0, 0))

    # Spawn an enemy pawn beside queen
    engine.spawn_piece(piece_nr=7, position=(0, 1))

    # See that one white piece has spawned
    assert len(engine.pieces["white"]) == 1

    # See that one black piece has spawned
    assert len(engine.pieces["black"]) == 1

    white_queen = engine.pieces["white"][-1]

    # See that first white pawn is blocked
    queen_moves = engine.apply_game_rules(white_queen)
    expected_queen_moves = (
        [(0, 1)] + [(i, 0) for i in range(1, 8)] + [(i, i) for i in range(1, 8)]
    )

    assert white_queen.position == (0, 0)
    assert set(queen_moves) == set(expected_queen_moves)


def test_queen_enemy_blocking_diagonal(config_path):
    """
    Test that queen is blocked by ally pieces
    as expected.
    """
    engine = Engine(config_path)
    engine.initiate_empty_board()

    # See that board is empty
    assert len(engine.pieces["white"]) == 0
    assert len(engine.pieces["black"]) == 0

    # Spawn white queen
    engine.spawn_piece(piece_nr=5, position=(0, 0))

    # Spawn an enemy pawn beside queen
    engine.spawn_piece(piece_nr=7, position=(1, 1))

    # See that one white piece has spawned
    assert len(engine.pieces["white"]) == 1

    # See that one black piece has spawned
    assert len(engine.pieces["black"]) == 1

    white_queen = engine.pieces["white"][-1]

    # See that first white pawn is blocked
    queen_moves = engine.apply_game_rules(white_queen)
    expected_queen_moves = (
        [(1, 1)] + [(i, 0) for i in range(1, 8)] + [(0, i) for i in range(1, 8)]
    )

    assert white_queen.position == (0, 0)
    assert set(queen_moves) == set(expected_queen_moves)

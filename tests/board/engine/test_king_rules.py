from board.engine import Engine


def test_king_start_game(config_path):
    """
    See that king starts with no available moves
    """
    engine = Engine(config_path)
    engine.start_game()

    white_king = engine.get_white_king()[-1]
    assert len(engine.king_rules(piece=white_king)) == 0


def test_king_ally_blocking(config_path):
    """
    Test that king is blocked by ally pieces
    as expected.
    """
    engine = Engine(config_path)
    engine.initiate_empty_board()

    # See that board is empty
    assert len(engine.pieces["white"]) == 0
    assert len(engine.pieces["black"]) == 0

    # Spawn white king
    engine.spawn_piece(piece_nr=6, position=(0, 0))

    # Spawn a pawn beside king
    engine.spawn_piece(piece_nr=1, position=(0, 1))

    # See that two white pieces are spawned
    assert len(engine.pieces["white"]) == 2

    white_king, _ = engine.pieces["white"]

    # See that white king is blocked
    king_moves = engine.apply_game_rules(white_king)
    expected_king_moves = [(1, 0), (1, 1)]

    assert white_king.position == (0, 0)
    assert set(king_moves) == set(expected_king_moves)


def test_king_suicidal_moves_are_blocked(config_path):
    """
    Test that king cannot move to positions where
    death is certain.
    """
    engine = Engine(config_path)
    engine.initiate_empty_board()

    # See that board is empty
    assert len(engine.pieces["white"]) == 0
    assert len(engine.pieces["black"]) == 0

    # Spawn white king
    engine.spawn_piece(piece_nr=6, position=(0, 0))

    # Spawn an enemy pawn beside king
    engine.spawn_piece(piece_nr=7, position=(2, 2))

    # See that one white piece has spawned
    assert len(engine.pieces["white"]) == 1

    # See that one black piece has spawned
    assert len(engine.pieces["black"]) == 1

    white_king = engine.pieces["white"][-1]

    # See that white king cannot move to (1, 1)
    king_moves = engine.apply_game_rules(white_king)

    assert white_king.position == (0, 0)
    assert (1, 1) not in king_moves


def test_king_suicidal_moves_check(config_path):
    """
    Test that king ally pieces can 'protect'
    the king by standing between
    the enemy and the king.
    """
    engine = Engine(config_path)
    engine.initiate_empty_board()

    # See that board is empty
    assert len(engine.pieces["white"]) == 0
    assert len(engine.pieces["black"]) == 0

    # Spawn white king
    engine.spawn_piece(piece_nr=6, position=(0, 0))

    # Spawn an black rook
    engine.spawn_piece(piece_nr=8, position=(1, 7))

    # Spawn white pawn to 'protect'
    # the path for the king
    engine.spawn_piece(piece_nr=1, position=(1, 2))

    # See that two white pieces has spawned
    assert len(engine.pieces["white"]) == 2

    # See that one black piece has spawned
    assert len(engine.pieces["black"]) == 1

    white_king, white_pawn = engine.pieces["white"]

    # See that white king cannot move to (1, 1)
    king_moves = engine.apply_game_rules(white_king)

    # See that correct pieces are spawned
    assert white_king.name == "King"
    assert white_pawn.name == "Pawn"

    # See that positions are correct
    assert white_king.position == (0, 0)
    assert white_pawn.position == (1, 2)

    # See that king can move because
    # pawn is 'protecting' the path
    assert (1, 1) in king_moves
    assert (1, 0) in king_moves


def test_king_and_pawn_interaction(config_path):
    """
    Test that interaction between king and pawn
    work as expected.
    This test was created as part of a bug-fix.
    """
    engine = Engine(config_path)
    engine.initiate_empty_board()

    # See that board is empty
    assert len(engine.pieces["white"]) == 0
    assert len(engine.pieces["black"]) == 0

    # Spawn white king
    engine.spawn_piece(piece_nr=6, position=(3, 2))

    # Spawn enemy pawn
    engine.spawn_piece(piece_nr=7, position=(4, 4))

    # See that one white piece has spawned
    assert len(engine.pieces["white"]) == 1

    # See that one black piece has spawned
    assert len(engine.pieces["black"]) == 1

    white_king = engine.get_white_king()[-1]

    # See that white king cannot move to (1, 1)
    king_moves = engine.apply_game_rules(white_king)

    # See that correct pieces are spawned
    assert white_king.name == "King"

    # See that positions are correct
    assert white_king.position == (3, 2)

    # See that king can move behind pawn
    assert (4, 2) in king_moves

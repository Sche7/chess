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
    assert len(engine.pieces['white']) == 0
    assert len(engine.pieces['black']) == 0

    # Spawn white king
    engine.spawn_piece(
        piece_nr=6,
        position=(0, 0)
    )

    # Spawn a pawn beside king
    engine.spawn_piece(
        piece_nr=1,
        position=(0, 1)
    )

    # See that two white pieces are spawned
    assert len(engine.pieces['white']) == 2

    white_king, _ = engine.pieces['white']

    # See that white king is blocked
    king_moves = engine.apply_game_rules(white_king)
    expected_king_moves = [(1, 0), (1, 1)]

    assert white_king.position == (0, 0)
    assert set(king_moves) == set(expected_king_moves)


def test_king_suicidal_moves_are_block(config_path):
    """
    Test that king cannot move to positions where
    death is certain.
    """
    engine = Engine(config_path)
    engine.initiate_empty_board()

    # See that board is empty
    assert len(engine.pieces['white']) == 0
    assert len(engine.pieces['black']) == 0

    # Spawn white king
    engine.spawn_piece(
        piece_nr=6,
        position=(0, 0)
    )

    # Spawn an enemy pawn beside king
    engine.spawn_piece(
        piece_nr=7,
        position=(2, 2)
    )

    # See that one white piece has spawned
    assert len(engine.pieces['white']) == 1

    # See that one black piece has spawned
    assert len(engine.pieces['black']) == 1

    white_king = engine.pieces['white'][-1]

    # See that white king cannot move to (1, 1)
    king_moves = engine.apply_game_rules(white_king)

    assert white_king.position == (0, 0)
    assert (1, 1) not in king_moves

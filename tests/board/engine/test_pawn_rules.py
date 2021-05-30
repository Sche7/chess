from board.engine import Engine


def test_start_game(config_path):
    engine = Engine(config_path)
    engine.start_game()

    white_pawns = engine.get_white_pawns()

    for pawn in white_pawns:
        position = pawn.position
        print(position)
        expected_moves = [
            (position[0], position[1] + 1),
            (position[0], position[1] + 2)
        ]
        assert set(engine.pawn_rules(piece=pawn)) == set(expected_moves)


def test_no_blocking(config_path):
    engine = Engine(config_path)
    engine.initiate_empty_board()

    # See that board is empty
    assert len(engine.pieces['white']) == 0
    assert len(engine.pieces['black']) == 0

    # Spawn white pawn
    engine.spawn_piece(
        piece_nr=1,
        position=(4, 4)
    )

    # See that two white pawns are spawned
    assert len(engine.pieces['white']) == 1

    white_pawn = engine.pieces['white'][0]

    # See that pawn only has 1 move option
    moves = engine.apply_game_rules(white_pawn)
    assert (4, 5) in moves
    assert len(moves) == 1


def test_ally_blocking(config_path):
    engine = Engine(config_path)
    engine.initiate_empty_board()

    # See that board is empty
    assert len(engine.pieces['white']) == 0
    assert len(engine.pieces['black']) == 0

    # Spawn white pawn
    engine.spawn_piece(
        piece_nr=1,
        position=(4, 4)
    )

    # Spawn another white pawn
    engine.spawn_piece(
        piece_nr=1,
        position=(4, 5)
    )

    # See that two white pawns are spawned
    assert len(engine.pieces['white']) == 2

    white_pawn_4_4, white_pawn_4_5 = engine.pieces['white']

    # See that first white pawn is blocked
    moves_4_4 = engine.apply_game_rules(white_pawn_4_4)
    assert white_pawn_4_4.position == (4, 4)
    assert len(moves_4_4) == 0

    # See that second white pawn can move
    moves_4_5 = engine.apply_game_rules(white_pawn_4_5)
    assert white_pawn_4_5.position == (4, 5)
    assert len(moves_4_5) == 1
    assert (4, 6) in moves_4_5


def test_killer_move(config_path):
    engine = Engine(config_path)
    engine.initiate_empty_board()

    # See that board is empty
    assert len(engine.pieces['white']) == 0
    assert len(engine.pieces['black']) == 0

    # Spawn white pawn
    engine.spawn_piece(
        piece_nr=1,
        position=(4, 4)
    )

    # Spawn black pawn
    engine.spawn_piece(
        piece_nr=7,
        position=(5, 5)
    )
    white_pawn = engine.pieces['white'][0]
    black_pawn = engine.pieces['black'][0]
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

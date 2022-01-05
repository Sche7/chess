from board.engine import Engine


def test_kills(config_path):
    '''
    Test that kills are handled correctly
    '''

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

    # Mock player input for killing black pawn
    player_input = {
        'id': white_pawn.id,
        'action': black_pawn.position
    }

    # Handle game
    engine.handle_game(player_input=player_input)

    # See that black pawn is killed
    assert black_pawn.status == 0

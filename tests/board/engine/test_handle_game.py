import pytest
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
    engine.handle_game(player='white', player_input=player_input)

    # See that black pawn is killed
    assert black_pawn.status == 0


@pytest.mark.parametrize('player', ['white', 'black'])
def test_player_is_in_check(config_path, player):
    """
    Test that engine evaluate a check correctly.
    """
    engine = Engine(config_path)
    engine.initiate_empty_board()

    # See that board is empty
    assert len(engine.pieces['white']) == 0
    assert len(engine.pieces['black']) == 0

    if player == 'white':
        # Spawn white king
        engine.spawn_piece(
            piece_nr=6,
            position=(4, 4)
        )

        # Spawn black rook
        engine.spawn_piece(
            piece_nr=8,
            position=(4, 6)
        )
    else:
        # Spawn black king
        engine.spawn_piece(
            piece_nr=12,
            position=(4, 4)
        )

        # Spawn white rook
        engine.spawn_piece(
            piece_nr=2,
            position=(4, 6)
        )

    assert engine.player_is_in_check(player=player)


@pytest.mark.parametrize('player', ['white', 'black'])
def test_player_is_not_in_check(config_path, player):
    """
    Test that engine evaluate a check correctly.
    """
    engine = Engine(config_path)
    engine.initiate_empty_board()

    # See that board is empty
    assert len(engine.pieces['white']) == 0
    assert len(engine.pieces['black']) == 0

    if player == 'white':
        # Spawn white king
        engine.spawn_piece(
            piece_nr=6,
            position=(4, 4)
        )

        # Spawn white pawn between king
        # and black rook
        engine.spawn_piece(
            piece_nr=1,
            position=(4, 5)
        )

        # Spawn black rook
        engine.spawn_piece(
            piece_nr=8,
            position=(4, 6)
        )
    else:
        # Spawn black king
        engine.spawn_piece(
            piece_nr=12,
            position=(4, 4)
        )

        # Spawn black pawn between king
        # and white rook
        engine.spawn_piece(
            piece_nr=7,
            position=(4, 5)
        )

        # Spawn white rook
        engine.spawn_piece(
            piece_nr=2,
            position=(4, 6)
        )

    assert not engine.player_is_in_check(player=player)

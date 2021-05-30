import pytest
from board.engine import Engine


def test_start_game(config_path):
    engine = Engine(config_path)
    engine.start_game()
    # See that 16 pieces are created for each player
    for color, pieces in engine.pieces.items():
        assert len(pieces) == 16, f'16 pieces were not created for {color}'

    # See that white and black each has 8 pawns
    for color, pieces in engine.pieces.items():
        pawns = engine._get_pieces(name='pawn', pieces=pieces)
        assert len(pawns) == 8, f'8 pawn pieces were not created for {color}'

    # See that white and black each has 2 rooks
    for color, pieces in engine.pieces.items():
        rooks = engine._get_pieces(name='rook', pieces=pieces)
        assert len(rooks) == 2, f'2 rook pieces were not created for {color}'

    # See that white and black each has 2 knights
    for color, pieces in engine.pieces.items():
        knights = engine._get_pieces(name='knight', pieces=pieces)
        assert len(knights) == 2, (
            f'2 knight pieces were not created for {color}'
        )

    # See that white and black each has has 2 bishops
    for color, pieces in engine.pieces.items():
        bishops = engine._get_pieces(name='bishop', pieces=pieces)
        assert len(bishops) == 2, (
            f'2 bishop pieces were not created for {color}'
        )

    # See that white and black each has 1 queen
    for color, pieces in engine.pieces.items():
        queen = engine._get_pieces(name='queen', pieces=pieces)
        assert len(queen) == 1, f'1 queen pieces were not created for {color}'

    # See that white and black each has 1 king
    for color, pieces in engine.pieces.items():
        king = engine._get_pieces(name='king', pieces=pieces)
        assert len(king) == 1, f'1 king piece were not created for {color}'

    # See that game is not over
    assert engine.game_over is False


def test_switch_turn(config_path):
    engine = Engine(config_path)
    engine.start_game()

    # See that white starts
    assert engine.player_turn == 'white'
    engine.switch_turn()

    # See that now its blacks turn
    assert engine.player_turn == 'black'


def test_create_piece(config_path):
    engine = Engine(config_path)

    # Supposedly white pawn created
    created_piece_1 = engine.create_piece(piece_nr=1, position=(1, 4))
    # See that a white Pawn is created
    assert created_piece_1.color.name == 'white'

    # Supposedly black pawn created
    created_piece_7 = engine.create_piece(piece_nr=7, position=(1, 4))
    # See that a black Pawn is created
    assert created_piece_7.color.name == 'black'


def test_create_piece_none(config_path):
    engine = Engine(config_path)

    # Supposedly non-piece number
    # 15 is not a piece in the system
    created_piece_none = engine.create_piece(piece_nr=15, position=(1, 4))
    # See that nothing was created
    assert created_piece_none is None


def test_get_possible_actions(config_path):
    engine = Engine(config_path)
    engine.start_game()

    king = engine.get_white_king()[0]

    possibe_actions = engine.get_possible_actions(king.id)

    # King should not have any possible moves
    # at start of the game
    assert len(possibe_actions) == 0


def test_get_possible_actions_invalid_id(config_path):
    engine = Engine(config_path)
    engine.start_game()

    # Apply method with invalid id
    with pytest.raises(ValueError) as e:
        engine.get_possible_actions(12345)
        assert 'ID [12345] does not exist' == str(e.value)


def test_pawn_positions_game_start(config_path):
    engine = Engine(config_path)
    engine.start_game()
    start_positions = {
        'white': [
            (0, 1), (1, 1), (2, 1),
            (3, 1), (4, 1), (5, 1),
            (6, 1), (7, 1)
        ],
        'black': [
            (0, 6), (1, 6), (2, 6),
            (3, 6), (4, 6), (5, 6),
            (6, 6), (7, 6)
        ]
    }
    white_pawns = engine.get_white_pawns()
    black_pawns = engine.get_black_pawns()

    for pawn in white_pawns:
        position = pawn.position
        assert position in start_positions['white']

    for pawn in black_pawns:
        position = pawn.position
        assert position in start_positions['black']

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

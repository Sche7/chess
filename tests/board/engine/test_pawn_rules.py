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

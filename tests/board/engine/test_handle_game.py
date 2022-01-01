import pytest
from board.engine import Engine


@pytest.fixture
def player_input(engine, piece_id):
    return {
        'id': 123,
        'action': (0, 2)
    }


def test_update_board(config_path):
    engine = Engine(config_path)
    engine.start_game()

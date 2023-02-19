import pytest
from src.board.files import read_yaml


@pytest.fixture
def config_path():
    return "tests/test_config.yml"


@pytest.fixture
def config(config_path):
    return read_yaml(config_path)

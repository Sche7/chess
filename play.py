"""
Simple py.file to run chess game
"""

from src.board.game import Chess
from src.board.engine import Engine
from src.board.view.displayer_factory import displayer_factory, Displayer


if __name__ == "__main__":
    config_path = "config.yml"
    view = displayer_factory(displayer=Displayer.terminal, config_path=config_path)
    engine = Engine(config_path=config_path)
    chess = Chess(engine=engine, displayer=view)
    chess.run()

"""
Simple py.file to run chess game
"""

from board.game import Chess
from board.engine import Engine
from board.view.displayer_factory import displayer_factory, Displayer


config_path = "config.yml"
view = displayer_factory(displayer=Displayer.terminal, config_path=config_path)
engine = Engine(config_path=config_path)
chess = Chess(engine=engine, displayer=view)


if __name__ == "__main__":
    chess.run()

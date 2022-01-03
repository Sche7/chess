"""
Simple py.file to run chess game
"""

from board.game import Chess
from board.view.displayer_factory import displayer_factory, Displayer


config_path = 'config.yml'
view = displayer_factory(displayer=Displayer.terminal, config_path=config_path)
chess = Chess(config_path=config_path, displayer=view)


if __name__ == '__main__':
    chess.run()

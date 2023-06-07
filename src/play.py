"""
Simple py.file to run chess game
"""
import argparse

from src.board.game import Chess
from src.board.engine import Engine
from src.board.view.displayer_factory import displayer_factory, Displayer


def main():
    parser = argparse.ArgumentParser(description="Start Chess game.")
    parser.add_argument("--c", help="Chess game configuration-file")
    args = parser.parse_args()
    config_path = args.c

    view = displayer_factory(displayer=Displayer.terminal, config_path=config_path)
    engine = Engine(config_path=config_path)
    chess = Chess(engine=engine, displayer=view)
    chess.run()

from typing import TypeVar, Generic

from src.board.view.terminal_view import TerminalView
from src.board.view.pygame_view import PygameView
from enum import Enum


View = TypeVar("View", TerminalView, PygameView)


class Displayer(Enum):
    terminal: str = "terminal"
    pygame: str = "pygame"


def displayer_factory(displayer: Displayer, config_path: str) -> Generic[View]:
    if displayer.name == "terminal":
        return TerminalView(config_path)
    elif displayer.name == "pygame":
        return PygameView(config_path)
    else:
        raise ValueError(f"Displayer {displayer} is not supported.")

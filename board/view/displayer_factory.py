from typing import Type

from board.view import View
from board.view.terminal_view import TerminalView
from enum import Enum


class Displayer(Enum):
    terminal: str = 'terminal'
    pygame: str = 'pygame'


def displayer_factory(displayer: Displayer, config_path: str) -> Type[View]:
    if displayer.name == 'terminal':
        return TerminalView(config_path)

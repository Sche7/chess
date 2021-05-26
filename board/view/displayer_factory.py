from typing import Type

from board.view import View
from board.view.terminal_view import TerminalView
from board.view.pygame_view import PygameView
from enum import Enum


class Displayer(Enum):
    terminal: str = 'terminal'
    pygame: str = 'pygame'


def displayer_factory(displayer: Displayer, config_path: str) -> Type[View]:
    if displayer.name == 'terminal':
        return TerminalView(config_path)
    elif displayer.name == 'pygame':
        return PygameView(config_path)
    else:
        raise ValueError(f'Displayer {displayer} is not supported.')

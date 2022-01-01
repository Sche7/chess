from board.game import Chess
from board.view.terminal_view import TerminalView


config_path = 'config.yml'
view = TerminalView(config_path=config_path)
chess = Chess(config_path=config_path, displayer=view)

chess.run()

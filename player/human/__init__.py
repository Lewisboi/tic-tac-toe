from models import Board, Play, Alignment
from display import Display
from control import Control
from player import Player


class HumanPlayer(Player):
    def __init__(self, display: Display, control: Control) -> None:
        self._display = display
        self._control = control

    def get_play(self, board: Board, alignment: Alignment) -> Play:
        self._display.display(board, alignment)
        position = self._control.get_position()
        return Play(position=position, alignment=alignment)

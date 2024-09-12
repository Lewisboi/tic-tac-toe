from abc import ABC, abstractmethod
from models import Board, Play, Alignment


class Player(ABC):
    @abstractmethod
    def get_play(self, board: Board, alignment: Alignment) -> Play: ...

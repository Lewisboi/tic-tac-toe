from abc import ABC, abstractmethod
from models import Board, Alignment


class Display(ABC):
    @abstractmethod
    def display(self, board: Board, alignment: Alignment) -> None: ...

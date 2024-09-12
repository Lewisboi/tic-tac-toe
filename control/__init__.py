from abc import ABC, abstractmethod
from models import Position


class Control(ABC):
    @abstractmethod
    def get_position(self) -> Position: ...

from models import Position
from control import Control


class TerminalControl(Control):
    def get_position(self) -> Position:
        try:
            row = int(input("row: "))
            col = int(input("col: "))
            return Position(row=row, col=col)
        except Exception:
            return self.get_position()

from models import Alignment, Board
from display import Display


class TerminalDisplay(Display):
    def display(self, board: Board, alignment: Alignment) -> None:
        print("\nBoard:")
        print(str(board))
        print(f"Alignment: {alignment}\n")

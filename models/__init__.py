from enum import Enum
from pydantic import BaseModel, model_validator


class BoardState(str, Enum):
    ONGOING = "ongoing"
    TIE = "tie"
    WON = "won"


class Alignment(str, Enum):
    X = "X"
    O = "O"

    def other(self) -> "Alignment":
        match self:
            case Alignment.X:
                return Alignment.O
            case Alignment.O:
                return Alignment.X

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return str(self)


class Position(BaseModel):
    row: int
    col: int


class Play(BaseModel):
    position: Position
    alignment: Alignment


BOARD_SIZE = 3


class Board(BaseModel):
    board: list[list[Alignment | None]]

    def register_play(self, play: Play) -> None:
        self.board[play.position.row][play.position.col] = play.alignment

    def undo_play(self, play: Play) -> None:
        self.board[play.position.row][play.position.col] = None

    def state(self) -> BoardState:
        if self.winner():
            return BoardState.WON
        if self.full():
            return BoardState.TIE
        return BoardState.ONGOING

    def _sequences(self) -> list[list[Alignment | None]]:
        rows = self.board
        cols = []
        diag_1 = []
        diag_2 = []
        for i in range(len(self.board[0])):
            col = [row[i] for row in self.board]
            cols.append(col)
            diag_1_elem = self.board[i][i]
            diag_2_elem = self.board[len(self.board) - 1 - i][i]
            diag_1.append(diag_1_elem)
            diag_2.append(diag_2_elem)
        diags = [diag_1, diag_2]
        return rows + cols + diags

    def winner(self) -> Alignment | None:
        for sequence in self._sequences():
            if winner := Board.check_sequence(sequence):
                return winner

    def full(self) -> bool:
        for row in self.board:
            for elem in row:
                if elem is None:
                    return False
        return True

    @staticmethod
    def check_sequence(sequence: list[Alignment | None]) -> Alignment | None:
        if None in sequence:
            return None
        first, *rest = sequence
        for elem in rest:
            if elem != first:
                return None
        return first

    @staticmethod
    def empty() -> "Board":
        return Board(board=[[None] * BOARD_SIZE] * BOARD_SIZE)

    def __str__(self) -> str:
        horizontal_line = "-" * ((2 * BOARD_SIZE) - 1)
        wall = "|"
        rows = []
        for row in self.board:
            rows.append(wall.join((str(elem) if elem else " " for elem in row)))
        return f"\n{horizontal_line}\n".join(rows)

    def validate_dimensions(self) -> None:
        number_of_rows = len(self.board)
        number_of_cols = len(self.board[0])
        if number_of_rows != number_of_cols:
            raise ValueError("board must be a square")

    def validate_uniform_rows(self) -> None:
        if len(set((len(row) for row in self.board))) != 1:
            raise ValueError("All rows must be of the same size")

    def moves_by_alignment(self) -> dict[Alignment, int]:
        move_counts = {alignment: 0 for alignment in Alignment}

        for row in self.board:
            for cell in row:
                if cell is not None:
                    move_counts[cell] += 1

        return move_counts

    def alignment_ahead(self) -> Alignment | None:
        moves = self.moves_by_alignment()
        if moves[Alignment.X] == moves[Alignment.O]:
            return
        return max(moves.items(), key=lambda x: x[1])[0]

    def validate_valid_move_sequence(self) -> None:
        moves = self.moves_by_alignment()
        if abs(moves[Alignment.X] - moves[Alignment.O]) > 1:
            raise ValueError(
                "The number of moves made by each alignment diverges by more than one"
            )

    @model_validator(mode="after")
    def validate_board(self) -> "Board":
        try:
            self.validate_dimensions()
            self.validate_uniform_rows()
            self.validate_valid_move_sequence()
        except ValueError as e:
            raise ValueError(f"Invalid board state: {str(e)}")
        return self

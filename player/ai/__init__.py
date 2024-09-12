from models import Board, Play, Alignment, Position, BoardState
from player import Player


class AIPlayer(Player):
    def get_play(self, board: Board, alignment: Alignment) -> Play:
        play, _ = _get_play_minmax(board, alignment)
        return play


WIN_REWARD = 1
TIE_REWARD = 0
LOSS_REWARD = -1


def _get_play_minmax(
    board: Board, alignment: Alignment, previous_play: Play | None = None
) -> tuple[Play, int]:
    match board.state():
        case BoardState.WON:
            return (previous_play, LOSS_REWARD)
        case BoardState.TIE:
            return (previous_play, TIE_REWARD)
    available_positions = _get_available_positions(board)
    plays = []
    for pos in available_positions:
        play = Play(position=pos, alignment=alignment)
        board.register_play(play)
        if board.winner():
            board.undo_play(play)
            return (play, WIN_REWARD)
        _, score = _get_play_minmax(board, alignment.other(), play)
        plays.append((play, score))
        board.undo_play(play)
    play, other_score = min(plays, key=lambda x: x[1])
    return (play, other_score * -1)


def _get_available_positions(board: Board) -> list[Position]:
    positions = []
    for r, row in enumerate(board.board):
        for c, elem in enumerate(row):
            if not elem:
                positions.append(Position(row=r, col=c))
    return positions

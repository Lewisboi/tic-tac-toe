from player.ai import _get_play_minmax
from models import Board, Alignment, Play

if __name__ == "__main__":
    board = Board(
        board=[
            [Alignment.O, None, Alignment.O],
            [None, Alignment.X, None],
            [None, None, Alignment.X],
        ]
    )

    play = _get_play_minmax(board, Alignment.O)
    print(play)

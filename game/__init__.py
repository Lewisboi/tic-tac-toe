from models import Board, Alignment, BoardState
from player import Player


class Game:
    def __init__(self, player_1: Player, player_2: Player) -> None:
        self._board = Board.empty()
        self._players = [(player_1, Alignment.X), (player_2, Alignment.O)]
        self._turn = 0

    def play(self) -> Alignment | None:
        while self._board.state() == BoardState.ONGOING:
            current_player, current_alignment = self.next_player()
            play = current_player.get_play(self._board, current_alignment)
            self._board.register_play(play)
        return self._board.winner()

    def next_player(self) -> tuple[Player, Alignment]:
        player, alignment = self._players[self._turn]
        self._turn = (self._turn + 1) % len(self._players)
        return player, alignment

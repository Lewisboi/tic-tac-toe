from game import Game
from display.terminal import TerminalDisplay
from control.terminal import TerminalControl
from player.human import HumanPlayer
from player.ai import AIPlayer


def main() -> None:
    display = TerminalDisplay()
    control = TerminalControl()
    human_player = HumanPlayer(display, control)
    ai_player = AIPlayer()
    game = Game(human_player, ai_player)
    winner = game.play()
    print(f"The winner is {winner}")


main()

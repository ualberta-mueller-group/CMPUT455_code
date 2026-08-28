# Cmput 455 sample code
# A game with three outcomes - win, loss, draw...
# ...but solved with two calls to negamax_boolean
# draw_winner decides whether draws count as wins for one player
# Written by Martin Mueller

import time
from game_basics import is_empty_black_white, EMPTY, WinnerColor
from game import Game

class Game3Outcome(Game):

    def reset_game(self) -> None:
        super().reset_game()
        self.draw_winner: WinnerColor = EMPTY

    def set_draw_winner(self, color: WinnerColor) -> None:
        assert is_empty_black_white(color)
        self.draw_winner = color

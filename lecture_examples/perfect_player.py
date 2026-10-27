# Cmput 455 sample code
# Perfect player, calls alphabeta to solve
# If there is a win, this player will find it
# Otherwise, if there is a draw this player will find it
# Written by Martin Mueller

from game import Game
from player import Player
from alphabeta_with_move import call_alphabeta

class PerfectPlayer(Player):
    def __init__(self) -> None:
        pass

    def name(self) -> str:
        return "Perfect Player"

    def genmove(self, state: Game) -> int:
        assert not state.end_of_game()
        ignore_winner, move = call_alphabeta(state)
        #print(ignore_winner, move)
        return move

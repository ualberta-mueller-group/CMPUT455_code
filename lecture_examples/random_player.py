# Cmput 455 sample code
# Written by Martin Mueller
# Random game player, selects move uniformly at random
# from among all legal moves

import random
from game import Game
from player import Player

class RandomPlayer(Player):
    def __init__(self) -> None:
        pass

    def name(self) -> str:
        return "Random Player"

    def genmove(self, state: Game) -> int:
        assert not state.end_of_game()
        return random.choice(state.legal_moves())

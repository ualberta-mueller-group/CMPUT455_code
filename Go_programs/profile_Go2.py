#!/usr/local/bin/python3
# /usr/bin/python3
# Set the path to your python3 above

import cProfile
import cProfile
import numpy as np
import random
from Go2 import Go2
from play_games import play_games

def play_Go2_games() -> None:
    player = Go2()
    play_games(player)

random.seed(1)
np.random.seed(1)
cProfile.run("play_Go2_games()")

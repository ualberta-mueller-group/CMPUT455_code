#!/usr/local/bin/python3
# /usr/bin/python3
# Set the path to your python3 above

import cProfile
import numpy as np
import random
from Go1 import Go1
from play_games import play_games

def play_Go1_games() -> None:
    player = Go1()
    play_games(player)

random.seed(1)
np.random.seed(1)
cProfile.run("play_Go1_games()")

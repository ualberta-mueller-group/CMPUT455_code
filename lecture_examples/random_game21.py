# Cmput 455 sample code
# Implementing a simple game
# Use the RandomPlayer to play a game of Game21 against itself
# First demo for using classes based on Game and Player
# Written by Martin Mueller.


from game_basics import COLOR_STR, WINNER_STR
from random_player import RandomPlayer
from game21 import Game21

g = Game21()
p = RandomPlayer()
while not g.end_of_game():
    print(f"Game state {g}, {COLOR_STR[g.to_play]} to play")
    move = p.genmove(g)
    print(f"Move {move}")
    g.play(move)
print(f"End of game, state {g}, winner {WINNER_STR[g.winner()]}")
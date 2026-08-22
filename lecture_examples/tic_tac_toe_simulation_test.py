# Cmput 455 sample code
# Run random simulations on empty TicTacToe board and report win statistics
# Written by Martin Mueller

from game_basics import BLACK, WHITE, EMPTY
from tic_tac_toe import TicTacToe

def random_TTT(num_simulations: int) -> None:
    print("Playing {} random TicTacToe games ...".format(num_simulations))
    t = TicTacToe()
    winner_stats = [0] * 3
    game_length = [0] * 10
    for _ in range(num_simulations):
        t.reset_game()
        winner, length = t.simulate()
        winner_stats[winner] += 1
        game_length[length] += 1
    print("{} wins for X, {} wins for O, {} draws".format(
        winner_stats[BLACK],  winner_stats[WHITE], winner_stats[EMPTY]))
    print("Game length:")
    for length in range(10):
        if game_length[length] > 0:
            print("Length {} : {}".format(length, game_length[length]))

if __name__ == "__main__":
    random_TTT(10000)

# Cmput 455 sample code
# Run random simulations on empty TicTacToe board and report win statistics
# Written by Martin Mueller

from game_basics import BLACK, WHITE, DRAW
from tic_tac_toe import TicTacToe

def test_tic_tac_toe_simulation(num_simulations: int) -> None:
    print(f"Playing {num_simulations} random TicTacToe games ...")
    t = TicTacToe()
    winner_stats = [0] * 3
    game_length = [0] * 10
    for _ in range(num_simulations):
        t.reset_game()
        winner, length = t.simulate()
        winner_stats[winner] += 1
        game_length[length] += 1
    print(f"{winner_stats[BLACK]} wins for X, "
          f"{winner_stats[WHITE]} wins for O, "
          f"{winner_stats[DRAW]} draws")
    print("Game length:")
    for length, count in enumerate(game_length):
        if count > 0:
            print(f"Length {length} : {count}")

if __name__ == "__main__":
    test_tic_tac_toe_simulation(10000)

from game21 import Game21
from game_basics import win_str
from negamax_boolean import negamax_boolean_timed

def test_solve_game21(max_size: int) -> None:
    for i in range(max_size + 1):
        game = Game21(i)
        is_win: bool
        time_used: float
        is_win, time_used = negamax_boolean_timed(game)
        print(f"Game {i} solved as {win_str(is_win)} in {time_used:.2e} seconds")

if __name__ == "__main__":
    test_solve_game21(21)

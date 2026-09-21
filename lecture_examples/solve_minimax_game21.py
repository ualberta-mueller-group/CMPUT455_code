from game21 import Game21
from game_basics import win_str
from minimax_boolean import minimax_boolean_timed

def run_solve_minimax_game21(max_size: int) -> None:
    for size in range(max_size + 1):
        game = Game21(size)
        is_win: bool
        time_used: float
        is_win, time_used = minimax_boolean_timed(game)
        print(f"Game {size} solved as {win_str(is_win)} "
              f"in {time_used:.2e} seconds")

def test_solve_minimax_game21(max_size: int) -> None:
    for size in range(max_size + 1):
        game = Game21(size)
        is_win: bool
        is_win, _ = minimax_boolean_timed(game)
        assert is_win == (size % 4 != 0) # losing iff multiple of 4

if __name__ == "__main__":
    run_solve_minimax_game21(21)
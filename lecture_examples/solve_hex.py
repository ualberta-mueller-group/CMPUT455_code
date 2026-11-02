from hex import Hex
from game_basics import win_str
from negamax_boolean_tt_id import negamax_timed

def solve_hex(size: int) -> None:
    game = Hex(size)
    is_win: bool
    time_used: float
    is_win, time_used = negamax_timed(game)
    print(f"Game size {size} solved as {win_str(is_win)} in {time_used:.2e} seconds")

if __name__ == "__main__":
    solve_hex(2)
    solve_hex(3)
    solve_hex(4)
    solve_hex(5)
    
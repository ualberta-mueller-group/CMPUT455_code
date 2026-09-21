from game_basics import BLACK, WHITE, color_as_string
from game import Game
from typing import Callable, Tuple

MinimaxTimedFunction = Callable[[Game], Tuple[bool, float]]

def solve_boolean(state: Game, solver: MinimaxTimedFunction, verbose: bool, negamax: bool, correct_result_black: bool): 
    if verbose:
        print(f"Board:\n{state}")
        print(f"{color_as_string(state.to_play)} to play")
    is_win: bool
    time_used: float
    is_win, time_used = solver(state)
    
    # flip results for white to play in negamax solvers
    is_win_for_black: bool = not is_win if negamax and state.to_play == WHITE else is_win 

    if verbose:
        print(f"Win for Black: {is_win_for_black}\n"
              f"Time used: {time_used:.4f}\n")
    assert is_win_for_black == correct_result_black


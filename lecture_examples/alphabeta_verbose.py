# Cmput 455 sample code
# Alphabeta algorithm with text output at each step
# Written by Martin Mueller

from search_basics import INFINITY
from game import Game

SPACES_PER_DEPTH: int = 4
def indent_str(depth: int) -> str:
    return ' ' * (SPACES_PER_DEPTH * depth)

verbose: bool = True # True False

def pr(depth: int, fstr: str) -> None:
    if verbose:
        indent = indent_str(depth)
        print(f"{indent}{fstr}")

def bound_str(score: int) -> str:
    return (
        "INFINITY" if score == INFINITY
        else "-INFINITY" if score == -INFINITY
        else str(score)
    )

def window_str(alpha: int, beta: int) -> str:
    return f"window ({bound_str(alpha)}, {bound_str(beta)})"
        
def alphabeta(state: Game, alpha: int, beta: int, depth: int) -> int:
    pr(depth, f"Call alphabeta with {window_str(alpha, beta)}")
    if state.end_of_game():
        v = state.int_eval() 
        pr(depth, f"Leaf node value {v}")
        return v
    for m in state.legal_moves():
        pr(depth, f"Play {m}")
        state.play(m)
        value: int = -alphabeta(state, -beta, -alpha, depth + 1)
        if value > alpha:
            alpha = value
            pr(depth, f"New best value {value}, new {window_str(alpha, beta)}")
        pr(depth, f"undo {m}")
        state.undo_move()
        if value >= beta: 
            pr(depth, f"beta cut {value} >= {beta}, return {beta}")
            return beta   # or value in failsoft
    pr(depth, f"tried all moves, return best value {alpha}")
    return alpha

# initial call with full window
def call_alphabeta(root_state: Game) -> int:
    return alphabeta(root_state, -INFINITY, INFINITY, depth = 0)


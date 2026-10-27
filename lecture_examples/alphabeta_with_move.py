# Cmput 455 sample code
# Alphabeta algorithm, plus remembering the move at the root
# Written by Martin Mueller

from typing import Tuple
from game import Game
from game_basics import NO_MOVE
from search_basics import INFINITY
from alphabeta import alphabeta

def alphabeta_with_move(state: Game, alpha: int, beta: int)\
 -> Tuple[int, int]:
    assert alpha == -INFINITY
    assert beta == INFINITY
    if state.end_of_game():
        return state.int_eval(), NO_MOVE
    best_move: int = NO_MOVE
    for m in state.legal_moves():
        state.play(m)
        value: int = -alphabeta(state, -beta, -alpha)
        if value > alpha:
            alpha = value
            best_move = m
        state.undo_move()
        if value >= beta: 
            return beta, best_move
    return alpha, best_move


# initial call with full window
def call_alphabeta(root: Game) -> Tuple[int, int]:
    return alphabeta_with_move(root, -INFINITY, INFINITY)

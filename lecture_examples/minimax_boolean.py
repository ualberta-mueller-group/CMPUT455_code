# Cmput 455 sample code
# Boolean Minimax
# Written by Martin Mueller

import time
from typing import Tuple
from game import Game
from game_basics import BLACK, WHITE

def minimax_boolean_or(state):
    """Can BLACK can force a win? (OR node)"""
    assert state.to_play == BLACK
    if state.end_of_game():
        return state.boolean_eval_black()
    for m in state.legal_moves():
        state.play(m)
        is_win: bool = minimax_boolean_and(state)
        state.undo_move()
        if is_win:
            return True
    return False

def minimax_boolean_and(state):
    """Can BLACK can force a win against all white moves? (AND node)"""
    assert state.to_play == WHITE
    if state.end_of_game():
        return state.boolean_eval_black()
    for m in state.legal_moves():
        state.play(m)
        is_loss: bool = not minimax_boolean_or(state)
        state.undo_move()
        if is_loss:
            return False
    return True

def minimax_boolean_timed(state: Game) -> Tuple[bool, float]: 
    """Can BLACK force a win from state?"""
    start: float = time.process_time() # does NOT account for system overhead
    if state.to_play == BLACK:
        win: bool = minimax_boolean_or(state)
    else:
        win: bool = minimax_boolean_and(state)
    time_used: float = time.process_time() - start
    return win, time_used

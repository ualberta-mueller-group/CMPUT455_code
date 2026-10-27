# Cmput 455 sample code
# Boolean Negamax
# Written by Martin Mueller

import time
from typing import List, Tuple, Optional
from game import Game
from transposition_table_simple import TranspositionTable
from game_basics import WinnerColor

TT = TranspositionTable[int, bool]

def store_result(tt: TT, state: Game, result: bool) -> bool:
    global num_store
    tt.store(state.code(), result)
    print(f"store {state} result {result}")
    num_store += 1
    return result

num_store: int = 0
num_lookup: int = 0
num_lookup_win: int = 0
num_lookup_loss: int = 0

def negamax_it(state: Game, depth: int, tt: TT) -> Optional[bool]:
    global num_lookup, num_lookup_win, num_lookup_loss
    result: Optional[bool] = tt.lookup(state.code())
    num_lookup += 1
    if result != None:
        if result: num_lookup_win += 1
        else: num_lookup_loss += 1
        return result
    if state.end_of_game():
        result = state.boolean_eval()
        #assert result is not None
        return store_result(tt, state, result)
    if depth == 0:
        return None
    has_unsolved: bool = False
    for m in state.legal_moves():
        state.play(m)
        result = negamax_it(state, depth - 1, tt)
        if result is None:
            has_unsolved = True
        else:
            result = not result
        state.undo_move()
        if result:
            return store_result(tt, state, True)
    if has_unsolved:
        return None
    else:
        return store_result(tt, state, False)

def reset_stats() -> None:
    global num_store, num_lookup, num_lookup_win, num_lookup_loss
    num_store = 0
    num_lookup = 0
    num_lookup_win = 0
    num_lookup_loss = 0

def print_stats() -> None:
    print(f"num_store = {num_store}, num_lookup = {num_lookup}: {num_lookup_win} wins, {num_lookup_loss} losses")

def negamax(state: Game, tt: TT) -> bool:
    depth: int = 0
    while True:
        print(f"depth {depth}")
        reset_stats()
        result: Optional[bool] = negamax_it(state, depth, tt)
        print_stats()
        if result is not None:
            return result
        depth += 1

def negamax_timed(game: Game) -> Tuple[bool, float]:
    start: float = time.process_time()
    tt = TT()
    is_win: bool = negamax(game, tt)
    time_used: float = time.process_time() - start
    return is_win, time_used

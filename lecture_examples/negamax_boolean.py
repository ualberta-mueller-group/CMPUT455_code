# Cmput 455 sample code
# Boolean Negamax
# Written by Martin Mueller

import time
from typing import List, Tuple
from game import Game

def negamax_boolean(game: Game) -> bool:
    """Does the current player (game.to_play) win with best play by both?"""
    if game.end_of_game():
        return game.boolean_eval()
    for m in game.legal_moves():
        game.play(m)
        success: bool = not negamax_boolean(game)
        game.undo_move()
        if success:
            return True
    return False

def negamax_boolean_timed(game: Game) -> Tuple[bool, float]:
    start: float = time.process_time()
    is_win: bool = negamax_boolean(game)
    time_used: float = time.process_time() - start
    return is_win, time_used

def find_all_winning_moves(game: Game) -> list[int]:
    if game.end_of_game():
        return []
    wins: List[int] = []
    for m in game.legal_moves():
        game.play(m)
        success: bool = not negamax_boolean(game)
        game.undo_move()
        if success:
            wins.append(m)
    return wins

def solve_all_timed(game: Game) -> Tuple[List[int], float]: 
    """Finds all winning moves and measures total solving time."""
    start: float = time.process_time()
    wins: List[int] = find_all_winning_moves(game)
    time_used: float = time.process_time() - start
    return wins, time_used

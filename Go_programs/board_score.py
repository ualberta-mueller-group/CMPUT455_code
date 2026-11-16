"""
board_score.py
Implements functions to:
- compute the final score on a Go board
- determine the winner.
"""

from typing import List
from board_base import BORDER, BLACK, EMPTY, WHITE, GO_COLOR, GO_POINT, NO_POINT, full_bool, BoardBoolArray
from board import GoBoard

def count_empty_area(board: GoBoard, point: GO_POINT, counted: BoardBoolArray) -> int:
    black_adj = False
    white_adj = False
    empty_points: List[GO_POINT] = [
        GO_POINT(p) for p in board.connected_component(point)
    ]
    for p in empty_points:
        counted[p] = True
        if not black_adj and board.has_neighbor_of_color(p, BLACK):
            black_adj = True
        if not white_adj and board.has_neighbor_of_color(p, WHITE):
            white_adj = True
        if black_adj and white_adj:
            return 0
    if black_adj or white_adj:
        area = len(empty_points) 
        return area if black_adj else -area
    else:
        return 0

def score_board(board: GoBoard, komi: float) -> float:
    """Score board from Black's point of view."""
    score: float = -komi
    counted = full_bool(board.maxpoint, False)
    for pt in range(board.maxpoint):
        point = GO_POINT(pt)
        color = board.get_color(point)
        if color == BORDER or counted[point]:
            continue
        if color == BLACK:
            score += 1
        elif color == WHITE:
            score -= 1
        else:
            score += count_empty_area(board, point, counted)
    return score

def winner(board: GoBoard, komi: float) -> GO_COLOR:
    """Determines the winning color or EMPTY for a tie."""
    score: float = score_board(board, komi)
    if score > 0:
        return BLACK
    elif score < 0:
        return WHITE
    else:
        return EMPTY

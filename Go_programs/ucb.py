# Cmput 455 sample code
# UCB algorithm
# Written by Martin Mueller

from board_base import GO_COLOR, GO_POINT, NO_POINT, PASS
from board import GoBoard
from gtp_connection import point_to_coord, format_point
from simulation_engine import GoSimulationEngine

import sys
from math import log, sqrt
from typing import List, Tuple

INFINITY = float("inf")

STATS = List[List[int]]
# tuple = (move, percentage, wins, pulls)
TUPLE = Tuple[str, float, int, int]

def mean(stats: STATS, i: int) -> float:
    return stats[i][0] / stats[i][1]


def ucb(stats: STATS, C: float, i: int, n: int) -> float:
    if stats[i][1] == 0:
        return INFINITY
    return mean(stats, i) + C * sqrt(log(n) / stats[i][1])


def find_best(stats: STATS, C: float, n: int) -> int:
    best = -1
    best_score = -INFINITY
    for i in range(len(stats)):
        score = ucb(stats, C, i, n)
        if score > best_score:
            best_score = score
            best = i
    assert best != -1
    return best


def best_arm(stats: STATS) -> int:  # Most-pulled arm
    best = -1
    best_score = -INFINITY
    for i in range(len(stats)):
        if stats[i][1] > best_score:
            best_score = stats[i][1]
            best = i
    assert best != -1
    return best


def by_percentage(tuple: TUPLE) -> float:
    return tuple[1]

def by_pulls(tuple: TUPLE) -> float:
    return tuple[3]

def write_moves(board: GoBoard, moves: List[GO_POINT], stats: STATS) -> None:
    gtp_moves = []
    for i in range(len(moves)):
        if moves[i] != PASS:
            x, y = point_to_coord(moves[i], board.size)
            point_string = format_point((x, y))
        else:
            point_string = "Pass"
        if stats[i][1] != 0:
            gtp_moves.append(
                (point_string, stats[i][0] / stats[i][1], stats[i][0], stats[i][1])
            )
        else:
            gtp_moves.append((point_string, 0.0, stats[i][0], stats[i][1]))
    sys.stderr.write(
        f"Statistics: {sorted(gtp_moves, key=by_pulls, reverse=True)}\n")
    sys.stderr.flush()


def run_UCB(player: GoSimulationEngine, board: GoBoard, C: float, 
           moves: List[GO_POINT], toplay: GO_COLOR) -> GO_POINT:
    stats = [[0, 0] for _ in moves]
    num_simulation = len(moves) * player.args.sim
    for n in range(num_simulation):
        move_index = find_best(stats, C, n)
        result = player.simulate(board, moves[move_index], toplay)
        if result == toplay:
            stats[move_index][0] += 1  # win
        stats[move_index][1] += 1
    best_index = best_arm(stats)
    best = moves[best_index]
    write_moves(board, moves, stats)
    return best

#!/usr/local/bin/python3
# /usr/bin/python3
# Set the path to your python3 above

from board_base import DEFAULT_SIZE, GO_POINT, GO_COLOR, PASS, opponent
from board import GoBoard
from board_abstract import GoBoardAbstractBase
from board_score import winner
from gtp_connection_go3 import GtpConnectionGo3
from pattern_util import PatternUtil
from simulation_engine import GoSimulationEngine, Go3Args
from simulation_util import write_moves, select_best_move
from ucb import run_UCB

import numpy as np
import argparse
import sys
from typing import Tuple

class Go3(GoSimulationEngine):
    def __init__(self, board: GoBoard, sim: int, move_select: str, sim_rule: str, 
                 check_selfatari: bool, limit: int = 100) -> None:
        """
        Go player that selects moves by simulation.
        """
        GoSimulationEngine.__init__(self, "Go3", 1.0,
                                    sim, move_select, sim_rule, 
                                    check_selfatari, limit)
        self.go_board = board

    def simulate(self, board: GoBoard, move: GO_POINT, toplay: GO_COLOR) -> GO_COLOR:
        """
        Run a simulated game for a given move.
        """
        cboard: GoBoard = board.copy()
        cboard.play_move(move, toplay)
        opp: GO_COLOR = opponent(toplay)
        return self.play_game(cboard, opp)

    def get_move(self, ignore_board: GoBoardAbstractBase, color: GO_COLOR) -> GO_POINT:
        """
        Run one-ply MC simulations to get a move to play.
        """
        bd = self.go_board
        cboard = bd.copy()
        empty_points = bd.get_empty_points()
        moves = []
        for p in empty_points:
            if bd.is_legal(p, color):
                moves.append(p)
        if not moves:
            return PASS
        moves.append(PASS)
        if self.args.use_ucb:
            C = 0.4  # sqrt(2) is safe, this is more aggressive
            best = run_UCB(self, cboard, C, moves, color)
            return best
        else:
            move_wins = []
            for move in moves:
                wins = self.simulate_move(cboard, move, color)
                move_wins.append(wins)
            write_moves(cboard, moves, move_wins, self.args.sim)
            return select_best_move(self.go_board, moves, move_wins)

    def play_game(self, board: GoBoard, color: GO_COLOR) -> GO_COLOR:
        """
        Run a simulation game.
        """
        nuPasses = 0
        for _ in range(self.args.limit):
            color = board.current_player
            if self.args.random_simulation:
                move = board.generate_random_move(color, True)
            else:
                move = PatternUtil.generate_move_with_filter(
                    board, self.args.use_pattern, self.args.check_selfatari
                )
            board.play_move(move, color)
            if move == PASS:
                nuPasses += 1
            else:
                nuPasses = 0
            if nuPasses >= 2:
                break
        return winner(board, self.komi)

def parse_args() -> Tuple[int, str, str, bool]:
    """
    Parse the arguments of the program.
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--sim",
        type=int,
        default=10,
        help="number of simulations per move, so total playouts=sim*legal_moves",
    )
    parser.add_argument(
        "--moveselect",
        type=str,
        default="simple",
        help="type of move selection: simple or ucb",
    )
    parser.add_argument(
        "--simrule",
        type=str,
        default="random",
        help="type of simulation policy: random or rulebased",
    )
    parser.add_argument(
        "--movefilter",
        action="store_true",
        default=False,
        help="whether use move filter or not",
    )

    args = parser.parse_args()
    sim = args.sim
    move_select = args.moveselect
    sim_rule = args.simrule
    check_selfatari = args.movefilter

    if move_select != "simple" and move_select != "ucb":
        print("moveselect must be simple or ucb")
        sys.exit(0)
    if sim_rule != "random" and sim_rule != "rulebased":
        print("simrule must be random or rulebased")
        sys.exit(0)

    return sim, move_select, sim_rule, check_selfatari

def run(sim: int, move_select: str, sim_rule: str, check_selfatari: bool) -> None:
    """
    Start the gtp connection and wait for commands.
    """
    board = GoBoard(DEFAULT_SIZE)
    engine: Go3 = Go3(board, sim, move_select, sim_rule, check_selfatari)
    con = GtpConnectionGo3(engine, board)
    con.start_connection()

if __name__ == "__main__":
    sim, move_select, sim_rule, check_selfatari = parse_args()
    run(sim, move_select, sim_rule, check_selfatari)

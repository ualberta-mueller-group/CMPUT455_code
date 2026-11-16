#!/usr/local/bin/python3
# /usr/bin/python3
# Set the path to your python3 above

from board_base import DEFAULT_SIZE, GO_POINT, GO_COLOR, PASS, opponent
from board import GoBoard
from board_abstract import GoBoardAbstractBase
from feature import Feature
from feature_moves import FeatureMoves
from gtp_connection_go3 import GtpConnectionGo3
from simulation_engine import GoSimulationEngine
from simulation_util import write_moves, select_best_move
from ucb import run_UCB

import argparse
import numpy as np
import sys
from typing import Tuple

class Go4(GoSimulationEngine):
    def __init__(self, board: GoBoard, sim: int, move_select: str, sim_rule: str, 
                 check_selfatari: bool, limit: int = 100):
        """
        Go player that selects moves by simulation.
        """
        GoSimulationEngine.__init__(self, "Go4", 1.0,
                                    sim, move_select, sim_rule, 
                                    check_selfatari, limit)
        self.go_board = board
        self.use_ucb = (move_select != "simple")
        self.use_pattern = (sim_rule == "rulebased")

    def simulate(self, board: GoBoard, move: GO_POINT, toplay: GO_COLOR) -> GO_COLOR:
        """
        Run a simulated game for a given move.
        """
        cboard = board.copy()
        cboard.play_move(move, toplay)
        opp = opponent(toplay)
        return FeatureMoves.playGame(
            cboard,
            opp,
            komi=self.komi,
            limit=self.args.limit,
            random_simulation=self.args.sim_rule,
            use_pattern=self.use_pattern,
            check_selfatari=self.args.check_selfatari,
        )


    def get_move(self, ignore_board: GoBoardAbstractBase, color: GO_COLOR) -> GO_POINT:
        """
        Run one-ply MC simulations to get a move to play.
        """
        board = self.go_board
        cboard = board.copy()
        emptyPoints = board.get_empty_points()
        moves = []
        for p in emptyPoints:
            if board.is_legal(p, color):
                moves.append(p)
        if not moves:
            return PASS
        moves.append(PASS)
        if self.use_ucb:
            C = 0.4  # sqrt(2) is safe, this is more aggressive
            best = run_UCB(self, cboard, C, moves, color)
            return best
        else:
            moveWins = []
            for move in moves:
                wins = self.simulate_move(cboard, move, color)
                moveWins.append(wins)
            write_moves(cboard, moves, moveWins, self.args.sim)
            return select_best_move(board, moves, moveWins)


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
        help="type of simulation policy: random or rulebased or prob",
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
    move_filter = args.movefilter

    if move_select != "simple" and move_select != "ucb":
        print("moveselect must be simple or ucb")
        sys.exit(0)
    if sim_rule != "random" and sim_rule != "rulebased" and sim_rule != "prob":
        print("simrule must be random or rulebased or prob")
        sys.exit(0)

    return sim, move_select, sim_rule, move_filter

def run(sim: int, move_select: str, sim_rule: str, check_selfatari: bool) -> None:
    """
    Start the gtp connection and wait for commands.
    """
    board: GoBoard = GoBoard(DEFAULT_SIZE)
    go_engine: Go4 = Go4(board, sim, move_select, sim_rule, check_selfatari)
    Feature.init_features(board)

    con: GtpConnectionGo3 = GtpConnectionGo3(go_engine, board)
    con.start_connection()


if __name__ == "__main__":
    sim, move_select, sim_rule, move_filter = parse_args()
    run(sim, move_select, sim_rule, move_filter)

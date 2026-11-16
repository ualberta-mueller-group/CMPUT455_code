#!/usr/local/bin/python3
# /usr/bin/python3
# Set the path to your python3 above

from board_base import DEFAULT_SIZE, GO_POINT, GO_COLOR
from board import GoBoard
from board_abstract import GoBoardAbstractBase
from gtp_connection_go3 import GtpConnectionGo3
from pattern_util import PatternUtil
from simulation_engine import GoSimulationEngine, Go3Args

import argparse
import numpy as np
import sys
from typing import Tuple


class PolicyPlayer(GoSimulationEngine):
    """
    The policy player chooses randomly among all policy moves.
    """

    def __init__(self, bd: GoBoard, sim_rule: str, check_selfatari: bool) -> None:
        sim: int = 0 # not used by this player
        move_select: str = ""  # not used by this player
        limit: int = 0  # not used by this player
        GoSimulationEngine.__init__(self, "PolicyPlayer", 1.0,
                                    sim, move_select, sim_rule, 
                                    check_selfatari, limit)
        self.go_board = bd
        
    def get_move(self, ignore_board: GoBoardAbstractBase, color: GO_COLOR) -> GO_POINT:
        return PatternUtil.generate_move_with_filter(
            self.go_board, self.args.use_pattern, self.args.check_selfatari
        )

def parse_args() -> Tuple[str, bool]:
    """
    Parse the arguments of the program.
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--simrule",
        type=str,
        default="rulebased",
        help="type of simulation policy: random or rulebased",
    )
    parser.add_argument(
        "--movefilter",
        action="store_true",
        default=False,
        help="whether use move filter or not",
    )
    args = parser.parse_args()
    if args.simrule != "random" and args.simrule != "rulebased":
        print("simrule must be random or rulebased")
        sys.exit(0)

    return args.simrule, args.movefilter

def run(sim_rule: str, check_selfatari: bool) -> None:
    """
    Start the gtp connection and wait for commands.
    """
    board = GoBoard(DEFAULT_SIZE)
    engine: PolicyPlayer = PolicyPlayer(board, sim_rule, check_selfatari)
    con = GtpConnectionGo3(engine, board)
    con.start_connection()

if __name__ == "__main__":
    sim_rule, move_filter = parse_args()
    run(sim_rule, move_filter)

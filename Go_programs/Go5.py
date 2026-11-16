#!/usr/local/bin/python3
# /usr/bin/python3
# Set the path to your python3 above

"""
Go5 MCTS Go player
Cmput 455 sample code
Written by Cmput 455 TA
"""
from board_base import DEFAULT_SIZE, GO_POINT, GO_COLOR
from board import GoBoard
from board_abstract import GoBoardAbstractBase
from feature_moves import FeatureMoves
from gtp_connection import point_to_coord, format_point
from gtp_connection_go5 import GtpConnectionGo5
from mcts import MCTS, TreeNode
from simulation_engine import GoSimulationEngine

import numpy as np
import argparse
import sys
from typing import List, Tuple

def count_at_depth(node: TreeNode, depth: int, nodesAtDepth: List[int]) -> None:
    if not node.expanded:
        return
    nodesAtDepth[depth] += 1
    for _, child in node.children.items():
        count_at_depth(child, depth + 1, nodesAtDepth)


class Go5(GoSimulationEngine):
    def __init__(
        self, board: GoBoard,
        sim: int,
        sim_rule: str,
        check_selfatari: bool,
        in_tree_knowledge: bool,
        limit: int = 100,
        exploration: float = 0.4,
    ) -> None:
        """
        Player that selects a move based on MCTS from the set of legal moves
        """
        move_select = "" # TODO not used in Go5?
        GoSimulationEngine.__init__(self, "Go5", 1.0,
                                    sim, move_select, sim_rule, 
                                    check_selfatari, limit)
        self.go_board = board
        self.MCTS = MCTS()
        self.exploration = exploration
        self.simulation_policy = sim_rule
        self.use_pattern = True
        self.in_tree_knowledge = in_tree_knowledge
        #self.parent = None

    def reset(self) -> None:
        self.MCTS = MCTS()

    def update(self, move: GO_POINT) -> None:
        self.parent = self.MCTS.root
        self.MCTS.update_with_move(move)

    def get_move(self, ignore_board: GoBoardAbstractBase, color: GO_COLOR) -> GO_POINT:
        board = self.go_board
        move = self.MCTS.get_move(
            board,
            color,
            komi=self.komi,
            limit=self.args.limit,
            check_selfatari=self.args.check_selfatari,
            use_pattern=self.use_pattern,
            num_simulation=self.args.sim,
            exploration=self.exploration,
            simulation_policy=self.simulation_policy,
            in_tree_knowledge=self.in_tree_knowledge,
        )
        self.MCTS.print_pi(board)
        self.update(move)
        return move

    def get_node_depth(self, root: TreeNode) -> List[int]:
        MAX_DEPTH = 100
        nodesAtDepth = [0] * MAX_DEPTH
        count_at_depth(root, 0, nodesAtDepth)
        prev_nodes = 1
        return nodesAtDepth

def parse_args() -> Tuple[int, str, bool, bool]:
    """
    Parse the arguments of the program.
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--sim",
        type=int,
        default=100,
        help="number of simulations per move, so total playouts=sim*legal_moves",
    )
    parser.add_argument(
        "--simrule",
        type=str,
        default="random",
        help="type of simulation policy: random or rulebased or probabilistic",
    )
    parser.add_argument(
        "--movefilter",
        action="store_true",
        default=False,
        help="whether use move filter or not",
    )
    parser.add_argument(
        "--in_tree_knowledge",
        type=str,
        default="None",
        help="whether use move knowledge to initial a new node or not",
    )
    args = parser.parse_args()

    num_sim = args.sim
    sim_rule = args.simrule
    move_filter = args.movefilter
    in_tree_knowledge = args.in_tree_knowledge

    if sim_rule != "random" and sim_rule != "rulebased" and sim_rule != "prob":
        print("simrule must be random or rulebased or prob")
        sys.exit(0)

    return num_sim, sim_rule, move_filter, in_tree_knowledge

def run(sim: int, sim_rule: str, check_selfatari: bool, in_tree_knowledge: bool) -> None:
    """
    Start the gtp connection and wait for commands.
    """
    board: GoBoard = GoBoard(DEFAULT_SIZE)
    go_engine: Go5 = Go5(board, sim, sim_rule, check_selfatari, in_tree_knowledge)
    con: GtpConnectionGo5 = GtpConnectionGo5(go_engine, board)
    con.start_connection()

if __name__ == "__main__":
    num_sim, sim_rule, move_filter, in_tree_knowledge = parse_args()
    run(num_sim, sim_rule, move_filter, in_tree_knowledge)

"""
mcts.py
Cmput 455 sample code
Written by Henry Du, partially based on older sample codes

Implements a game tree for MCTS in class TreeNode,
and the search itself in class MCTS
"""

from board_base import opponent, BLACK, WHITE, PASS, GO_COLOR, GO_POINT, NO_POINT, coord_to_point
from board import GoBoard
from feature_moves import FeatureMoves
from gtp_connection import point_to_coord, format_point

import sys
from typing import Dict, List, Tuple
from math import log, sqrt

def uct(child_wins: int, child_visits: int, parent_visits: int, exploration: float) -> float:
    assert parent_visits > 0
    assert child_visits > 0
    return child_wins / child_visits + exploration * sqrt(log(parent_visits) / child_visits)

class TreeNode:
    """
    A node in the MCTS tree
    """

    def __init__(self, color: GO_COLOR) -> None:
        self.move: GO_POINT = NO_POINT
        self.color: GO_COLOR = color
        self.n_visits: int = 0
        self.n_opp_wins: int = 0
        self.parent: 'TreeNode' = self
        self.children: Dict[int, TreeNode] = {}
        self.expanded: bool = False
    
    def set_parent(self, parent: 'TreeNode') -> None:
        self.parent = parent

    def expand(self, board: GoBoard, color: GO_COLOR) -> None:
        """
        Expands tree by creating new children.
        """
        opp_color = opponent(board.current_player)
        moves = board.get_empty_points()
        for move in moves:
            if board.is_legal(move, color) and not board.is_eye(move, color):
                node = TreeNode(opp_color)
                node.move = move
                node.set_parent(self)
                self.children[move] = node
        node = TreeNode(opp_color)
        node.move = PASS
        node.set_parent(self)
        self.children[PASS] = node
        self.expanded = True
    
    def select_in_tree(self, exploration: float) -> Tuple[GO_POINT, 'TreeNode']:
        """
        Select move among children that gives maximizes UCT. 
        If number of visits are zero for a node, value for that node is infinite, so definitely will get selected

        It uses: argmax(child_num_wins/child_num_vists + C * sqrt( ln(parent_num_vists) / child_num_visits )
        Returns:
        A tuple of (move, next_node)
        """
        _child = None
        _uct_val: float = -1.
        for move, child in self.children.items():
            if child.n_visits == 0:
                return child.move, child
            uct_val = uct(child.n_opp_wins, child.n_visits, self.n_visits, exploration)
            if uct_val > _uct_val:
                _uct_val = uct_val
                _child = child
        assert _child is not None
        return _child.move, _child
    
    def select_best_child(self) -> Tuple[GO_POINT, 'TreeNode']:
        _n_visits = -1
        best_child = None
        for move, child in self.children.items():
            if child.n_visits > _n_visits:
                _n_visits = child.n_visits
                best_child = child
        assert best_child is not None
        return best_child.move, best_child
    
    def update(self, winner: GO_COLOR) -> None:
        self.n_opp_wins += self.color != winner
        self.n_visits += 1
        if not self.is_root():
            self.parent.update(winner)
    
    def is_leaf(self) -> bool:
        """
        Check if leaf node (i.e. no nodes below this have been expanded).
        """
        return len(self.children) == 0
    
    def is_root(self) -> bool:
        return self.parent == self
    

class MCTS:

    def __init__(self) -> None:
        self.root: 'TreeNode' = TreeNode(BLACK)
        self.root.set_parent(self.root)
        self.toplay: GO_COLOR = BLACK
    
    def search(self, board: GoBoard, color: GO_COLOR) -> None:
        """
        Run a single playout from the root to the given depth, getting a value at the leaf and
        propagating it back through its parents. State is modified in-place, so a copy must be
        provided.
        Arguments:
        board -- a copy of the board.
        color -- color to play
        """
        node = self.root
        # This will be True olny once for the root
        if not node.expanded:
            node.expand(board, color)
        while not node.is_leaf():
            move, next_node = node.select_in_tree(self.exploration)
            assert board.play_move(move, color)
            color = opponent(color)
            node = next_node
        if not node.expanded:
            node.expand(board, color)
        
        assert board.current_player == color
        winner = self.rollout(board, color)
        node.update(winner)
    
    def rollout(self, board: GoBoard, color: GO_COLOR) -> GO_COLOR:
        """
        Use the rollout policy to play until the end of the game, returning the winner of the game
        +1 if black wins, +2 if white wins, 0 if it is a tie.
        """
        winner = FeatureMoves.playGame(
            board,
            color,
            komi=self.komi,
            limit=self.limit,
            random_simulation=self.simulation_policy,
            use_pattern=self.use_pattern,
            check_selfatari=self.check_selfatari,
        )
        return winner
    
    def get_move(
        self,
        board: GoBoard,
        color: GO_COLOR,
        komi: float,
        limit: int,
        check_selfatari: bool,
        use_pattern: bool,
        num_simulation: int,
        exploration: float,
        simulation_policy: str,
        in_tree_knowledge: bool,
    ) -> GO_POINT:
        """
        Runs all playouts sequentially and returns the most visited move.
        """
        if self.toplay != color:
            sys.stderr.write("Tree is for wrong color to play. Deleting.\n")
            sys.stderr.flush()
            self.toplay = color
            self.root = TreeNode(color)
        self.komi = komi
        self.limit = limit
        self.check_selfatari = check_selfatari
        self.use_pattern = use_pattern
        self.exploration = exploration
        self.simulation_policy = simulation_policy
        self.in_tree_knowledge = in_tree_knowledge

        if not self.root.expanded:
            self.root.expand(board, color)

        for _ in range(num_simulation*len(self.root.children)):
            cboard = board.copy()
            self.search(cboard, color)
        # choose a move that has the most visit
        best_move, best_child = self.root.select_best_child()
        return best_move
    
    def update_with_move(self, last_move: GO_POINT) -> None:
        """
        Step forward in the tree, keeping everything we already know about the subtree, assuming
        that get_move() has been called already. Siblings of the new root will be garbage-collected.
        """
        if last_move in self.root.children:
            self.root = self.root.children[last_move]
        else:
            self.root = TreeNode(opponent(self.toplay))
        self.root.parent = self.root
        self.toplay = opponent(self.toplay)
    
    def print_pi(self, board: GoBoard) -> None:
        # TODO print PASS
        empty_points: List[GO_POINT] = board.get_empty_points()
        for p in empty_points:
            if p in self.root.children:
                pi = self.root.children[p].n_visits
        #TODO formatting as 2-d board
                sys.stderr.write(f"point {p} pi {pi:5}")
            sys.stderr.write("\n")
        sys.stderr.flush()

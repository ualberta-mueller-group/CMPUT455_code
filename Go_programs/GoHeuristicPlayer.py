"""
GoHeuristicPlayer Simple heuristic-based Go player
Cmput 455 sample code
Written by Henry Du, based on Fuego AveragePlayer
The strongest of the simple players in Fuego
Maximises the difference of average liberties, own vs opponent
Tends to build long chains, and also likes to reduce opponent liberties
"""

import random
from typing import List, Tuple, Set, Optional

from board import GoBoard
from board_abstract import GoBoardAbstractBase
from board_base import GO_COLOR, GO_POINT, PASS, opponent
from engine import GoEngine
import gtp_connection


class GoHeuristicPlayer(GoEngine):
    def __init__(self, board: GoBoard, generator: "AverageMoveGenerator") -> None:
        self.board: GoBoard = board
        self.generator: AverageMoveGenerator = generator
        self.name: str = "HeuristicPlayer"
        self.version: float = 1.1

    def get_move(self, ignore_board: GoBoardAbstractBase, color: GO_COLOR) -> GO_POINT:
        """Selects the move with the highest heuristic evaluation score."""
        moves_scores: List[Tuple[GO_POINT, float]] = \
            self.generator.generate_moves(self.board, color)
        if not moves_scores:
            return PASS

        best_moves: List[GO_POINT] = []
        best_score: float = -float("inf")

        for move, score in moves_scores:
            if score > best_score:
                best_score = score
                best_moves = [move]
            elif score == best_score:
                best_moves.append(move)

        return random.choice(best_moves) if best_moves else PASS


class AverageMoveGenerator:
    def __init__(self, board: GoBoard) -> None:
        self.board: GoBoard = board

    def generate_moves(
        self, board: GoBoard, color: GO_COLOR
    ) -> List[Tuple[GO_POINT, float]]:
        """
        Performs 1-ply search and
        returns a list of (move, score) tuples
        """
        self.board = board
        empty_points: List[GO_POINT] = self.board.get_empty_points()
        moves_scores: List[Tuple[GO_POINT, float]] = []

        for point in empty_points:
            # filter out eye-filling moves
            if self.board.is_eye(point, color):
                continue
            score: float = self.evaluate_move(point, color)
            if score > -float("inf"):
                moves_scores.append((point, score))

        return moves_scores

    def evaluate_move(self, point: GO_POINT, color: GO_COLOR) -> float:
        """Plays the move on a board copy and returns the score evaluation."""
        cboard: GoBoard = self.board.copy()
        if cboard.play_move(point, color):
            return self.evaluate(cboard)
        return -float("inf")

    def evaluate(self, board: GoBoard) -> float:
        """Evaluates the input board state and returns its relative liberty score."""
        color: GO_COLOR = board.current_player
        opp_color: GO_COLOR = opponent(color)
        score: float = self.liberty_average(board, opp_color) \
                     - self.liberty_average(board, color)
        return score

    def liberty_average(self, board: GoBoard, color: GO_COLOR) -> float:
        """
        Calculates the score of the input board w.r.t. color
        score = total_liberties(color) / number_of_blocks(color)
        """
        num_libs: int = 0
        num_blocks: int = 0
        met_points: Set[GO_POINT] = set()
        color_points: List[GO_POINT] = board.get_color_points(color)

        for point in color_points:
            if point not in met_points:
                liberty_count, block = board.get_block_liberty(point, color)
                met_points.update(block)
                num_libs += liberty_count
                num_blocks += 1

        if num_blocks == 0:
            return 0.0
        return num_libs / num_blocks


def run() -> None:
    """Start the gtp connection and wait for commands."""
    size: int = 7
    board: GoBoard = GoBoard(size)
    move_generator: AverageMoveGenerator = AverageMoveGenerator(board)
    player: GoHeuristicPlayer = GoHeuristicPlayer(board, move_generator)
    con: gtp_connection.GtpConnection = gtp_connection.GtpConnection(player, board)
    con.start_connection()


if __name__ == "__main__":
    run()
"""
feature_moves.py
Move generation based on simple features.
"""
from board_base import GO_COLOR, GO_POINT, NO_POINT, PASS
from board import GoBoard
from board_score import winner
from feature import Features_weight
from feature import Feature
from pattern_util import PatternUtil

import numpy as np
import random
from typing import Any, Tuple, List
import sys

MOVES_PROBS_LIST = Tuple[List[GO_POINT], np.ndarray]

class FeatureMoves(object):
    @staticmethod
    def generate_moves(board: GoBoard) -> MOVES_PROBS_LIST:

        assert len(Features_weight) != 0
        moves = []
        gamma_sum = 0.0
        empty_points = board.get_empty_points()
        color = board.current_player
        probs = np.zeros(board.maxpoint)
        all_board_features = Feature.find_all_features(board)
        for move in empty_points:
            if board.is_legal(move, color) and not board.is_eye(move, color):
                moves.append(move)
                probs[move] = Feature.compute_move_gamma(
                    Features_weight, all_board_features[move]
                )
                gamma_sum += probs[move]
        if len(moves) != 0:
            assert gamma_sum != 0.0
            for m in moves:
                probs[m] = probs[m] / gamma_sum
        return moves, probs

    @staticmethod
    def generate_move(board: GoBoard) -> GO_POINT:
        moves, probs = FeatureMoves.generate_moves(board)
        if len(moves) == 0:
            return NO_POINT
        return np.random.choice(board.maxpoint, 1, p=probs)[0] # type: ignore
        # TODO need to figure out type conversions from Go code to numpy

    @staticmethod
    def generate_move_with_feature_based_probs_max(board: GoBoard) -> GO_POINT:
        """Used for UI"""
        moves, probs = FeatureMoves.generate_moves(board)
        move_prob_tuple = []
        for m in moves:
            move_prob_tuple.append((m, probs[m]))
        return sorted(move_prob_tuple, key=lambda i: i[1], reverse=True)[0][0]

    @staticmethod
    def playGame(board: GoBoard, color: GO_COLOR, **kwargs: Any) -> GO_COLOR:
    # TODO is Any OK here? See discussion in
    # https://stackoverflow.com/questions/37031928/type-annotations-for-args-and-kwargs
        """
        Run a simulation game according to given parameters.
        """
        komi = kwargs.pop("komi", 0)
        limit = kwargs.pop("limit", 1000)
        simulation_policy = kwargs.pop("random_simulation", "random")
        use_pattern = kwargs.pop("use_pattern", True)
        check_selfatari = kwargs.pop("check_selfatari", True)
        if kwargs:
            raise TypeError("Unexpected **kwargs: %r" % kwargs)
        nuPasses = 0
        for _ in range(limit):
            color = board.current_player
            if simulation_policy == "random":
                move = board.generate_random_move(color, True)
            elif simulation_policy == "rulebased":
                move = PatternUtil.generate_move_with_filter(
                    board, use_pattern, check_selfatari
                )
            else:
                assert simulation_policy == "prob"
                move = FeatureMoves.generate_move(board)
            if move == NO_POINT: move = PASS
            board.play_move(move, color)
            if move == PASS:
                nuPasses += 1
            else:
                nuPasses = 0
            if nuPasses >= 2:
                break
        return winner(board, komi)

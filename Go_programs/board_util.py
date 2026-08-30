"""
board_util.py
Utility functions for Go board.
"""

import numpy as np
import random
from typing import List
from board_base import GO_COLOR, GO_POINT, PASS
from board import GoBoard

class GoBoardUtil(object):
    @staticmethod
    def is_legal_non_eye(board: GoBoard, move: GO_POINT, color: GO_COLOR, \
                         use_eye_filter: bool) -> bool:
        """
        Check if a move is legal and optionally passes the simple eye filter.
        """
        if use_eye_filter and board.is_eye(move, color):
            return False
        return board.is_legal(move, color)

    @staticmethod
    def generate_legal_moves(board: GoBoard, color: GO_COLOR) -> List[GO_POINT]:
        """
        generate a list of all legal moves on the board.
        Does not include the Pass move.

        Arguments
        ---------
        board:
            a GoBoard, a 1-d array representing the board
        color:
            the color to generate the move for.
        """
        moves: np.ndarray = board.get_empty_points()
        legal_moves: List[GO_POINT] = []
        for move in moves:
            if board.is_legal(move, color):
                legal_moves.append(move)
        return legal_moves

    @staticmethod
    def generate_random_move(board: GoBoard, color: GO_COLOR, 
                             use_eye_filter: bool) -> GO_POINT:
        """
        Generate a random move.
        Return PASS if no move found

        Arguments
        ---------
        board : GoBoard
        color : BLACK, WHITE
            the color to generate the move for.
        use_eye_filter : bool
            whether to filter out moves that fill a simple eye
        """
        moves: np.ndarray = board.get_empty_points()
        np.random.shuffle(moves)
        for move in moves:
            if GoBoardUtil.is_legal_non_eye(board, move, color, \
               use_eye_filter):
                return move
        return PASS

    @staticmethod
    def generate_random_moves(board: GoBoard, use_eye_filter: bool) \
        -> List[GO_POINT]:
        """
        Return a list of random (legal) moves with optional eye-filtering.
        """
        empty_points: np.ndarray = board.get_empty_points()
        color: GO_COLOR = board.current_player
        moves: List[GO_POINT] = []
        for move in empty_points:
            if GoBoardUtil.is_legal_non_eye(board, move, color, \
               use_eye_filter):
                moves.append(move)
        return moves

    @staticmethod
    def get_twoD_board(go_board: GoBoard) -> np.ndarray:
        """
        Return: numpy array
        a two dimensional numpy array with the goboard.
        Shows stones and empty points as numbers, encoded as in board_base.py.
        Result is not padded with BORDER points.
        Rows 1..size of goboard are copied into rows 0..size - 1 of board2d
        Then the board is flipped up-down to be consistent with the GoGui
        coordinate system, with row 1 at the bottom.
        """
        size: int = go_board.size
        board2d: np.ndarray = np.zeros((size, size), dtype=GO_POINT)
        for row in range(size):
            start: int = go_board.row_start(row + 1)
            board2d[row, :] = go_board.board[start : start + size]
        board2d = np.flipud(board2d)
        return board2d
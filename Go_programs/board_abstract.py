import random
from abc import ABC, abstractmethod
from typing import List, Tuple
from board_base import BoardArray, BoardBoolArray, board_array_size,\
    coord_to_point, is_black_white,\
    is_black_white_empty, opponent, where_value, BLACK, WHITE, EMPTY, BORDER,\
    MAXSIZE, NO_POINT, PASS, GO_COLOR, GO_POINT, full, full_bool

class GoBoardAbstractBase(ABC):
    """
    Abstract base class for 1D padded array Go board.
    Board state management, coordinate conversions,
    and basic Go rules.
    """

    def __init__(self, size: int) -> None:
        assert 2 <= size <= MAXSIZE
        self.reset(size)

    @abstractmethod
    def copy(self) -> "GoBoardAbstractBase":
        """Returns an independent copy of the board state."""
        pass
    
    def reset(self, size: int) -> None:
        """Resets board to initial empty state of given size."""
        self.size: int = size
        self.NS: int = size + 1
        self.WE: int = 1
        self.ko_recapture: GO_POINT = NO_POINT
        self.last_move: GO_POINT = NO_POINT
        self.last2_move: GO_POINT = NO_POINT
        self.current_player: GO_COLOR = BLACK
        self.maxpoint: int = board_array_size(size)
        self.board: BoardArray = full(self.maxpoint, BORDER)
        self._initialize_empty_points(self.board)

    @abstractmethod
    def is_legal(self, point: GO_POINT, color: GO_COLOR) -> bool:
        """Check whether move on point is legal for color."""
        pass

    @abstractmethod
    def play_move(self, point: GO_POINT, color: GO_COLOR) -> bool:
        """Play a move on point for color. Returns True if legal and applied."""
        pass

    def get_color(self, point: GO_POINT) -> GO_COLOR:
        return self.board[point]

    def pt(self, row: int, col: int) -> GO_POINT:
        return coord_to_point(row, col, self.size)

    def row_start(self, row: int) -> int:
        assert 1 <= row <= self.size
        return row * self.NS + 1

    def _initialize_empty_points(self, board_array: BoardArray) -> None:
        for row in range(1, self.size + 1):
            start: int = self.row_start(row)
            board_array[start : start + self.size] = [EMPTY] * self.size
        
    def end_of_game(self) -> bool:
        return self.last_move == PASS and self.last2_move == PASS

    def get_empty_points(self) -> BoardArray:
        return where_value(self.board, EMPTY)

    def get_color_points(self, color: GO_COLOR) -> BoardArray:
        assert is_black_white_empty(color)
        return where_value(self.board, color)

    def _is_legal_check_simple_cases(self, point: GO_POINT, color: GO_COLOR) -> bool:
        assert is_black_white(color)
        if point == PASS:
            return True
        assert self.pt(1, 1) <= point <= self.pt(self.size, self.size)
        assert is_black_white_empty(self.board[point])
        if self.board[point] != EMPTY:
            return False
        if point == self.ko_recapture:
            return False
        return True

    def _neighbors(self, point: GO_POINT) -> List[GO_POINT]:
        return [point - 1, point + 1, point - self.NS, point + self.NS]

    def _diag_neighbors(self, p: GO_POINT) -> List[GO_POINT]:
        up = self.NS
        return [p - up - 1, p - up + 1, p + up - 1, p + up + 1]

    def is_eye(self, point: GO_POINT, color: GO_COLOR) -> bool:
        if not self._is_surrounded(point, color):
            return False
        opp_color = opponent(color)
        false_count = 0
        at_edge = 0
        for d in self._diag_neighbors(point):
            if self.board[d] == BORDER:
                at_edge = 1
            elif self.board[d] == opp_color:
                false_count += 1
        return false_count <= 1 - at_edge

    def _is_surrounded(self, point: GO_POINT, color: GO_COLOR) -> bool:
        for nb in self._neighbors(point):
            nb_color = self.board[nb]
            if nb_color != BORDER and nb_color != color:
                return False
        return True

    def _block_of(self, stone: GO_POINT) -> BoardBoolArray:
        color: GO_COLOR = self.get_color(stone)
        assert is_black_white(color)
        return self.connected_component(stone)

    def connected_component(self, point: GO_POINT) -> BoardBoolArray:
        marker = full_bool(self.maxpoint, False)
        pointstack = [point]
        color: GO_COLOR = self.get_color(point)
        assert is_black_white_empty(color)
        marker[point] = True
        while pointstack:
            p = pointstack.pop()
            neighbors = self.neighbors_of_color(p, color)
            for nb in neighbors:
                if not marker[nb]:
                    marker[nb] = True
                    pointstack.append(nb)
        return marker

    def neighbors_of_color(self, point: GO_POINT, color: GO_COLOR) -> List[GO_POINT]:
        nbc: List[GO_POINT] = []
        for nb in self._neighbors(point):
            if self.get_color(nb) == color:
                nbc.append(nb)
        return nbc

    def last_board_moves(self) -> List[GO_POINT]:
        board_moves: List[GO_POINT] = []
        if self.last_move != NO_POINT and self.last_move != PASS:
            board_moves.append(self.last_move)
        if self.last2_move != NO_POINT and self.last2_move != PASS:
            board_moves.append(self.last2_move)
        return board_moves

    def is_legal_non_eye(self, move: GO_POINT, color: GO_COLOR, \
                         use_eye_filter: bool) -> bool:
        """
        Check if a move is legal and optionally passes the simple eye filter.
        """
        if use_eye_filter and self.is_eye(move, color):
            return False
        return self.is_legal(move, color)

    def generate_legal_moves(self, color: GO_COLOR) -> List[GO_POINT]:
        """
        generate a list of all legal moves of color on the board.
        Does not include the Pass move.
        """
        moves: BoardArray = self.get_empty_points()
        legal_moves: List[GO_POINT] = []
        for move in moves:
            if self.is_legal(move, color):
                legal_moves.append(move)
        return legal_moves

    def generate_random_move(self, color: GO_COLOR, 
                             use_eye_filter: bool) -> GO_POINT:
        """
        Generate a random move.
        Return PASS if no move found

        Arguments
        ---------
        color : BLACK, WHITE
            the color to generate the move for.
        use_eye_filter : bool
            whether to filter out moves that fill a simple eye
        """
        moves: BoardArray = self.get_empty_points()
        random.shuffle(moves)
        for move in moves:
            if self.is_legal_non_eye(move, color, use_eye_filter):
                return move
        return PASS

    def generate_random_moves(self, use_eye_filter: bool) \
        -> List[GO_POINT]:
        """
        Return a list of random (legal) moves with optional eye-filtering.
        """
        empty_points: BoardArray = self.get_empty_points()
        color: GO_COLOR = self.current_player
        moves: List[GO_POINT] = []
        for move in empty_points:
            if self.is_legal_non_eye(move, color, use_eye_filter):
                moves.append(move)
        return moves

    def get_twoD_board(self) -> List[List[int]]:
        """
        Return:
        A two-dimensional Python list representing the GoBoard.
        Shows stones and empty points as numbers, encoded as in board_base.py.
        Result is not padded with BORDER points.
        Rows 1..size of goboard are copied into rows 0..size - 1 of board2d.
        Then the board is flipped up-down to be consistent with the GoGui
        coordinate system, with row 1 at the bottom.
        """
        size: int = self.size
        board2d: List[List[int]] = []

        # Copy row by row from row_start(row + 1)
        for row in range(size):
            start: int = self.row_start(row + 1)
            row_slice = list(self.board[start : start + size])
            board2d.append(row_slice)

        # Flip up-down in pure Python
        board2d.reverse()
        return board2d
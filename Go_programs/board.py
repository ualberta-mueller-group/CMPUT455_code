"""
board.py
Cmput 455 sample code
Written by Cmput 455 TA and Martin Mueller

Defines GoBoardBase (abstract base class), SimpleGoBoard (naive copy-based board),
and GoBoard (optimized board with precomputed neighbor lists and liberty caching).
"""

from abc import ABC, abstractmethod
from typing import List, Tuple
from board_abstract import GoBoardAbstractBase

from board_base import (
    BoardArray, BoardBoolArray, board_array_size,
    coord_to_point,
    is_black_white,
    is_black_white_empty,
    opponent,
    where_bool,
    BLACK,
    WHITE,
    EMPTY,
    BORDER,
    MAXSIZE,
    NO_POINT,
    PASS,
    GO_COLOR,
    GO_POINT, full
)

class GoBoard(GoBoardAbstractBase):
    """
    Optimized GoBoard using precomputed neighbor lists, fast liberty checks,
    and cached block liberties (`liberty_of`).
    """

    def reset(self, size: int) -> None:
        super().reset(size)
        self.liberty_of: BoardArray = full(self.maxpoint, NO_POINT)
        self._initialize_neighbors()

    def copy(self) -> "GoBoard":
        """
         copy the GoBoard state.
        Immutable/structural data like `neighbors` are shared with the source board,
        while state arrays (`board`, `liberty_of`) are sliced/copied.
        DO NOT DELETE the source.
        TODO extract shared data into new object
        """
        b = GoBoard.__new__(GoBoard)
        b.size = self.size
        b.NS = self.NS
        b.WE = self.WE
        b.maxpoint = self.maxpoint
        b.ko_recapture = self.ko_recapture
        b.last_move = self.last_move
        b.last2_move = self.last2_move
        b.current_player = self.current_player

        b.board = self.board.copy()
        b.liberty_of = self.liberty_of.copy()

        # Shared reference to precomputed immutable neighbor structure
        b.neighbors = self.neighbors

        return b
    
    def _on_board_neighbors(self, point: GO_POINT) -> List[GO_POINT]:
        return [nb for nb in self._neighbors(point) if self.board[nb] != BORDER]

    def _initialize_neighbors(self) -> None:
        self.neighbors: List[List[GO_POINT]] = []
        for point in range(self.maxpoint):
            if self.board[point] == BORDER:
                self.neighbors.append([])
            else:
                self.neighbors.append(self._on_board_neighbors(GO_POINT(point)))

    def is_legal(self, point: GO_POINT, color: GO_COLOR) -> bool:
        if point == PASS:
            return True
        if not self._is_legal_check_simple_cases(point, color):
            return False

        opp_color = opponent(color)
        self.board[point] = color
        legal = True
        has_capture = self._detect_captures(point, opp_color)
        if not has_capture and not self._stone_has_liberty(point):
            block = self._block_of(point)
            if not self._has_liberty(block, readOnly=True):
                legal = False
        self.board[point] = EMPTY
        return legal

    def _detect_captures(self, point: GO_POINT, opp_color: GO_COLOR) -> bool:
        for nb in self.neighbors_of_color(point, opp_color):
            if self._detect_capture(nb):
                return True
        return False

    def _is_surrounded(self, point: GO_POINT, color: GO_COLOR) -> bool:
        for nb in self.neighbors[point]:
            if self.board[nb] != color:
                return False
        return True

    def _stone_has_liberty(self, stone: GO_POINT) -> bool:
        return self.find_neighbor_of_color(stone, EMPTY) != NO_POINT

    def _get_liberty(self, block: BoardBoolArray) -> GO_POINT:
        for stone in where_bool(block):
            lib = self.find_neighbor_of_color(stone, EMPTY)
            if lib != NO_POINT:
                return lib
        return NO_POINT

    def _has_liberty(self, block: BoardBoolArray, readOnly: bool = False) -> bool:
        lib = self._get_liberty(block)
        if lib == NO_POINT:
            return False
        assert self.get_color(lib) == EMPTY
        if not readOnly:
            for stone in where_bool(block):
                self.liberty_of[stone] = lib
        return True

    def _liberty(self, point: GO_POINT, color: GO_COLOR) -> int:
        num_lib, _ = self._liberty_point(point, color)
        return num_lib

    def _liberty_point(self, point: GO_POINT, color: GO_COLOR) -> Tuple[int, GO_POINT]:
        assert color == self.get_color(point)
        group_points = [point]
        liberty = 0
        met_points = [point]
        single_lib_point = NO_POINT
        while group_points:
            p = group_points.pop()
            met_points.append(p)
            for n in self.neighbors[p]:
                if n not in met_points:
                    assert self.board[n] != BORDER
                    if self.board[n] == color:
                        group_points.append(n)
                    elif self.board[n] == EMPTY:
                        liberty += 1
                        single_lib_point = n
                    met_points.append(n)
        if liberty == 1:
            return liberty, single_lib_point
        return liberty, NO_POINT

    def get_block_liberty(self, point: GO_POINT, color: GO_COLOR) -> Tuple[int, List[GO_POINT]]:
        assert color == self.get_color(point)
        group_points = [point]
        liberty = 0
        met_points = [point]
        while group_points:
            p = group_points.pop()
            met_points.append(p)
            for n in self.neighbors[p]:
                if n not in met_points:
                    assert self.board[n] != BORDER
                    if self.board[n] == color:
                        group_points.append(n)
                    elif self.board[n] == EMPTY:
                        liberty += 1
                    met_points.append(n)
        return liberty, met_points

    def _fast_liberty_check(self, nb_point: GO_POINT) -> bool:
        lib = self.liberty_of[nb_point]
        if lib != NO_POINT and self.get_color(lib) == EMPTY:
            return True
        return self._stone_has_liberty(nb_point)

    def _detect_capture(self, nb_point: GO_POINT) -> bool:
        if self._fast_liberty_check(nb_point):
            return False
        opp_block = self._block_of(nb_point)
        return not self._has_liberty(opp_block)

    def _detect_and_process_capture(self, nb_point: GO_POINT) -> GO_POINT:
        if self._fast_liberty_check(nb_point):
            return NO_POINT
        opp_block = self._block_of(nb_point)
        if self._has_liberty(opp_block):
            return NO_POINT
        captures = where_bool(opp_block)
        for point in captures:
            self.board[point] = EMPTY
            self.liberty_of[point] = NO_POINT
        return nb_point if len(captures) == 1 else NO_POINT

    def play_move(self, point: GO_POINT, color: GO_COLOR) -> bool:
        if point == PASS:
            self.ko_recapture = NO_POINT
            self.current_player = opponent(color)
            self.last2_move = self.last_move
            self.last_move = point
            return True
        if not self._is_legal_check_simple_cases(point, color):
            return False

        opp_color = opponent(color)
        in_enemy_eye = self._is_surrounded(point, opp_color)
        self.board[point] = color
        single_captures = []
        for nb in self.neighbors[point]:
            if self.board[nb] == opp_color:
                single_capture = self._detect_and_process_capture(nb)
                if single_capture != NO_POINT:
                    single_captures.append(single_capture)
        if not self._stone_has_liberty(point):
            block = self._block_of(point)
            if not self._has_liberty(block):
                self.board[point] = EMPTY
                return False
        self.ko_recapture = NO_POINT
        if in_enemy_eye and len(single_captures) == 1:
            self.ko_recapture = single_captures[0]
        self.current_player = opponent(color)
        self.last2_move = self.last_move
        self.last_move = point
        return True

    def neighbors_of_color(self, point: GO_POINT, color: GO_COLOR) -> List[GO_POINT]:
        return [nb for nb in self.neighbors[point] if self.get_color(nb) == color]

    def find_neighbor_of_color(self, point: GO_POINT, color: GO_COLOR) -> GO_POINT:
        return next(
            (nb for nb in self.neighbors[point] if self.get_color(nb) == color),
            NO_POINT)
            
    def has_neighbor_of_color(self, point: GO_POINT, color: GO_COLOR) -> bool:
        return any(self.get_color(nb) == color for nb in self.neighbors[point])
    
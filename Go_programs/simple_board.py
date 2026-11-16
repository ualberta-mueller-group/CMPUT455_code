from board_abstract import GoBoardAbstractBase
from board_base import BoardArray, BoardBoolArray, GO_POINT, GO_COLOR, PASS, EMPTY, NO_POINT, opponent, where_bool

class GoBoard(GoBoardAbstractBase):
    """
    Naive implementation of GoBoard.
    Checks legality by copying the board and trying to play the move.
    """

    def copy(self) -> "GoBoard":
        b = GoBoard(self.size)
        assert b.NS == self.NS
        assert b.WE == self.WE
        b.ko_recapture = self.ko_recapture
        b.last_move = self.last_move
        b.last2_move = self.last2_move
        b.current_player = self.current_player
        assert b.maxpoint == self.maxpoint
        b.board = self.board.copy()
        return b

    def is_legal(self, point: GO_POINT, color: GO_COLOR) -> bool:
        if point == PASS:
            return True
        board_copy: GoBoard = self.copy()
        return board_copy.play_move(point, color)

    def _has_liberty(self, block: BoardBoolArray) -> bool:
        for stone in where_bool(block):
            if self.neighbors_of_color(stone, EMPTY):
                return True
        return False

    def _detect_and_process_capture(self, nb_point: GO_POINT) -> GO_POINT:
        single_capture: GO_POINT = NO_POINT
        opp_block = self._block_of(nb_point)
        if not self._has_liberty(opp_block):
            captures = where_bool(opp_block)
            for point in captures:
                self.board[point] = EMPTY
            if len(captures) == 1:
                single_capture = nb_point
        return single_capture

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
        for nb in self._neighbors(point):
            if self.board[nb] == opp_color:
                single_capture = self._detect_and_process_capture(nb)
                if single_capture != NO_POINT:
                    single_captures.append(single_capture)
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

#!/usr/local/bin/python3
# /usr/bin/python3
# Set the path to your python3 above

import unittest
from typing import List
from board_base import BLACK, WHITE, EMPTY, BORDER, NO_POINT, PASS, where_value, MAXSIZE
from board import GoBoard


class SimpleGoBoardTestCase(unittest.TestCase):
    """Tests for board.py"""

    def test_size_2(self) -> None:
        goboard = GoBoard(2)
        self.assertEqual(goboard.size, 2)
        self.assertEqual(goboard.NS, 3)
        self.assertEqual(goboard.WE, 1)
        self.assertEqual(goboard.ko_recapture, NO_POINT)
        self.assertEqual(goboard.current_player, BLACK)
        self.assertEqual(goboard.maxpoint, 13)
        self.assertEqual(goboard.board[0], BORDER)
        self.assertEqual(goboard.board[goboard.pt(1, 1)], EMPTY)
        self.assertEqual(goboard.board[goboard.pt(1, 2)], EMPTY)
        self.assertEqual(goboard.board[goboard.pt(2, 1)], EMPTY)
        self.assertEqual(goboard.board[goboard.pt(2, 2)], EMPTY)

    def do_test_pointsets(self, size: int) -> None:
        goboard = GoBoard(size)
        count = count_colors(goboard)
        self.assertEqual(count[EMPTY], size * size)
        self.assertEqual(count[BLACK], 0)
        self.assertEqual(count[WHITE], 0)
        num_border = 3 * (size + 1)
        self.assertEqual(count[BORDER], num_border)

    def test_size_2_pointsets(self) -> None:
        self.do_test_pointsets(2)

    def test_size_7_pointsets(self) -> None:
        self.do_test_pointsets(7)

    def test_size_19_pointsets(self) -> None:
        self.do_test_pointsets(19)

    def test_size_2_play_move(self) -> None:
        size = 2
        goboard = GoBoard(size)
        goboard.play_move(goboard.pt(1, 1), BLACK)
        count = count_colors(goboard)
        self.assertEqual(count, [1, 0, size * size - 1, 3 * (size + 1)])

    def test_size_2_legal_moves(self) -> None:
        size = 2
        goboard = GoBoard(size)
        moves = goboard.generate_legal_moves(BLACK)
        self.assertEqual(moves,
            [goboard.pt(1, 1), goboard.pt(1, 2), 
             goboard.pt(2, 1), goboard.pt(2, 2)])

    def test_get_twoD_board(self) -> None:
        for size in range(2, MAXSIZE + 1):
            goboard = GoBoard(size)
            two_d_board = goboard.get_twoD_board()
            empty_array = [[EMPTY] * size for _ in range(size)]
            self.assertEqual(two_d_board, empty_array)


"""Utility"""
def count_colors(goboard: GoBoard) -> List[int]:
    count = []
    for color in range(BORDER + 1):
        points_in_color = where_value(goboard.board, color)
        count.append(len(points_in_color))
    return count


"""Main"""
if __name__ == "__main__":
    unittest.main()

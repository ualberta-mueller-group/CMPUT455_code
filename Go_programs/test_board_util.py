#!/usr/local/bin/python3
# /usr/bin/python3
# Set the path to your python3 above

import numpy as np
import unittest
from board_base import BLACK
from board import GoBoard
from board_util import GoBoardUtil


class GoBoardUtilTestCase(unittest.TestCase):
    """Tests for board_util.py"""

    def test_size_2_legal_moves(self) -> None:
        size = 2
        goboard = GoBoard(size)
        moves = GoBoardUtil.generate_legal_moves(goboard, BLACK)
        self.assertEqual(
            moves,
            [goboard.pt(1, 1), goboard.pt(1, 2), goboard.pt(2, 1), goboard.pt(2, 2)],
        )

    def test_get_twoD_board(self) -> None:
        size = 2
        goboard = GoBoard(size)
        two_d_board = GoBoardUtil.get_twoD_board(goboard)
        #print(two_d_board)
        #print(type(two_d_board))
        zero_array = np.zeros((2, 2))
        compare = (two_d_board == zero_array)
        self.assertTrue(compare.all())


"""Main"""
if __name__ == "__main__":
    unittest.main()

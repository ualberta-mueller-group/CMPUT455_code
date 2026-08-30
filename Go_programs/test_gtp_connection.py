#!/usr/local/bin/python3
# /usr/bin/python3
# Set the path to your python3 above

import unittest
from unittest.mock import patch
import numpy as np
from board_base import BLACK, WHITE, EMPTY, BORDER, PASS, GO_POINT, GO_COLOR, where1d
from board import GoBoard
from engine import GoEngine
from gtp_connection import GtpConnection

class MockGoEngine(GoEngine):
    def __init__(self) -> None:
        self.name = "Mock"
        self.version = 1.234

    def get_move(self, board: GoBoard, color: GO_COLOR) -> GO_POINT:
        return board.pt(1, 1)


class GtpConnectionTestCase(unittest.TestCase):
    """Tests for board.py"""

    def test_size_2(self) -> None:
        board = GoBoard(2)
        con = GtpConnection(MockGoEngine(), board)


#         con.start_connection()
#     To do: This test does not do much.
#     I started researching how to mock the stdin to put some gtp commands in
#     a string for testing. But I did not find a working solution.
#     We could make GtpConnection take input/output streams as arguments
#     but it makes to code messier.

"""Main"""
if __name__ == "__main__":
    unittest.main()

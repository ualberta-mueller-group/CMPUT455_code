"""
Go2 almost-random Go player
Cmput 455 sample code
Same almost-random play as Go1, but about 4x faster
Uses board.py instead of simple_board.py
Written by Cmput 455 TA and Martin Mueller
"""

from board_base import DEFAULT_SIZE, GO_POINT, GO_COLOR
from board_abstract import GoBoardAbstractBase
from board import GoBoard
from engine import GoEngine
from gtp_connection_go2 import GtpConnectionGo2


class Go2(GoEngine):
    def __init__(self) -> None:
        """
        Go player that selects moves randomly from the set of legal moves.
        However, it filters eye-filling moves.
        Passes only if there is no other legal move.
        """
        GoEngine.__init__(self, name="Go2", version=1.0)

    def get_move(self, board: GoBoardAbstractBase, color: GO_COLOR) -> GO_POINT:
        return board.generate_random_move(color, use_eye_filter=True)


def run() -> None:
    """
    start the gtp connection and wait for commands.
    """
    board = GoBoard(DEFAULT_SIZE)
    con = GtpConnectionGo2(Go2(), board)
    con.start_connection()


if __name__ == "__main__":
    run()

"""
Go1 almost-random Go player
Cmput 455 sample code
Written by Cmput 455 TA and Martin Mueller
"""

from gtp_connection_go1 import GtpConnectionGo1
from board_base import DEFAULT_SIZE, GO_POINT, GO_COLOR
from board import GoBoard
from board_util import GoBoardUtil
from engine import GoEngine


class Go1(GoEngine):
    def __init__(self) -> None:
        """
        Go player that selects moves randomly from the set of legal moves.
        However, it filters eye-filling moves.
        Passes only if there is no other legal move.
        """
        GoEngine.__init__(self, name="Go1", version=1.0)

    def get_move(self, board: GoBoard, color: GO_COLOR) -> GO_POINT:
        return GoBoardUtil.generate_random_move(board, color, 
                                                use_eye_filter=True)


def run() -> None:
    """
    start the gtp connection and wait for commands.
    """
    board: GoBoard = GoBoard(DEFAULT_SIZE)
    con: GtpConnectionGo1 = GtpConnectionGo1(Go1(), board)
    con.start_connection()


if __name__ == "__main__":
    run()

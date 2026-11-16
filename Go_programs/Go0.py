"""
Go0 random Go player
Cmput 455 sample code
Written by Cmput 455 TA and Martin Mueller
"""

from gtp_connection import GtpConnection
from board_base import DEFAULT_SIZE, GO_POINT, GO_COLOR
from board_abstract import GoBoardAbstractBase
from simple_board import GoBoard
from engine import GoEngine


class Go0(GoEngine):
    def __init__(self) -> None:
        """
        Go player that selects moves randomly from the set of legal moves.
        Does not use the fill-eye filter.
        Passes only if there is no other legal move.
        """
        GoEngine.__init__(self, name="Go0", version=1.0)

    def get_move(self, board: GoBoardAbstractBase, color: GO_COLOR) -> GO_POINT:
        return board.generate_random_move(color, use_eye_filter=False)


def run() -> None:
    """
    start the gtp connection and wait for commands.
    """
    board: GoBoard = GoBoard(DEFAULT_SIZE)
    con: GtpConnection = GtpConnection(Go0(), board)
    con.start_connection()


if __name__ == "__main__":
    run()

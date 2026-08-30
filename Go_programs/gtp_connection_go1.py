"""
gtp_connection_go1.py
Example for extending a GTP engine with extra commands
"""
from board import GoBoard
from engine import GoEngine
from gtp_connection import GtpConnection
from typing import List


class GtpConnectionGo1(GtpConnection):
    def __init__(self, go_engine: GoEngine, board: GoBoard, debug_mode: bool=False) -> None:
        """
        GTP connection of Go1
        """
        GtpConnection.__init__(self, go_engine, board, debug_mode)
        self.commands["hello"] = self.hello_cmd
        self.argmap["hello"] = (0, "Usage: hello")

    def hello_cmd(self, args: List[str]) -> None:
        """ Dummy Hello Command """
        self.respond("Hello! " + self.go_engine.name)

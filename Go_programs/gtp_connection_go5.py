"""
gtp_connection_go5.py
Cmput 455 sample code
Written by Henry Du

Overwrites several commands in GtpConnectionGo3 such as play_cmd.
It also keeps the self.go_engine in sync.
"""
from board_base import GO_POINT, opponent, coord_to_point, PASS
from board import GoBoard
from simulation_engine import GoSimulationEngine
from gtp_connection import point_to_coord, format_point, color_to_int, move_to_coord
from gtp_connection_go3 import GtpConnectionGo3

from typing import List


class GtpConnectionGo5(GtpConnectionGo3):
    def __init__(self, go_engine: GoSimulationEngine, 
                 board: GoBoard, debug_mode: bool = False) -> None:
        """
        GTP connection of GoSimulationEngine
        """
        GtpConnectionGo3.__init__(self, go_engine, board, debug_mode)
        self.go_engine: GoSimulationEngine = go_engine
        # Note: this overrides the type of go_engine defined in GtpConnection.
        # mypy seems happy with this.
        
        self.commands["clear_board"] = self.clear_board_cmd
        self.commands["boardsize"] = self.boardsize_cmd
        self.commands["play"] = self.play_cmd

    def clear_board_cmd(self, args: List[str]) -> None:
        """ clear the board """
        self.reset(self.board.size)
        self.go_engine.reset()  # reset search tree
        self.respond()

    def boardsize_cmd(self, args: List[str]) -> None:
        """
        Reset the game with new boardsize args[0]
        """
        self.reset(int(args[0]))
        self.go_engine.reset()  # reset search tree
        self.respond()
    
    def play_cmd(self, args: List[str]) -> None:
        """
        play a move args[1] for given color args[0] in {'b','w'}
        """
        try:
            board_color = args[0].lower()
            board_move = args[1]
            color = color_to_int(board_color)
            if args[1].lower() == "pass":
                self.board.play_move(PASS, color)
                self.board.current_player = opponent(color)
                self.go_engine.update(PASS)
                self.respond()
                return
            coord = move_to_coord(args[1], self.board.size)
            move = coord_to_point(coord[0], coord[1], self.board.size)
            if not self.board.play_move(move, color):
                self.respond(f"Illegal Move: {board_move}")
                return
            else:
                self.go_engine.update(move)
                self.debug_msg(
                f"Move: {board_move}\nBoard:\n{self.board2d()}\n")
            self.respond()
        except Exception as e:
            self.respond(f"Error: {str(e)}")

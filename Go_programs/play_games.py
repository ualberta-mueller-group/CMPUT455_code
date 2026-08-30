#!/usr/local/bin/python3
# /usr/bin/python3
# Set the path to your python3 above

from board import GoBoard

def play_games(player) -> None:
    """
    play 100 self-play games on 7x7 for profiling.
    """
    size = 7
    board = GoBoard(size)
    for _ in range(100):  # play 100 games
        board.reset(size)
        while not board.end_of_game():
            color = board.current_player
            move = player.get_move(board, color)
            board.play_move(move, color)


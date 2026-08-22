# Cmput 455 sample code
# TicTacToe game board, rules, and a random game simulator
# Includes the code() method to compute a "hash code" for 
# use in a transposition table (This is actually a perfect code, 
# not a lossy hash code, since the state space is so small)
# Written by Martin Mueller

import random
from game_basics import Color, WinnerColor, EMPTY, BLACK, \
                        WHITE, is_empty_black_white, opponent
from game import Game

class TicTacToe(Game):
# Board is stored in array of size 9 as follows:
# 0 1 2
# 3 4 5
# 6 7 8

    def reset_game(self) -> None:
        super().reset_game()
        self.board = [EMPTY] * 9
        self.draw_winner = EMPTY

    def reset_to_move_number(self, move_nr: int) -> None:
        num_undos = self.move_number() - move_nr
        assert num_undos >= 0
        for _ in range(num_undos):
            self.undo_move()
        assert self.move_number() == move_nr

    def end_of_game(self) -> bool:
        return (   len(self.moves) == 9
                or self.winner() != EMPTY
               )

    def play(self, move: int) -> bool:
        assert not self.end_of_game()
        assert self.board[move] == EMPTY
        self.board[move] = self.to_play
        self.moves.append(move)
        self.switch_to_play()
        return True

    def undo_move(self) -> None:
        move = self.moves.pop()
        self.board[move] = EMPTY
        self.switch_to_play()
    
    def has_three(self, color: Color, p1: int, p2: int, p3: int) -> bool:
        return all(self.board[p] == color for p in (p1, p2, p3))

    def has_row(self, color: Color, start: int) -> bool:
        return self.has_three(color, start, start+1, start+2)

    def has_col(self, color: Color, start: int) -> bool:
        return self.has_three(color, start, start+3, start+6)
    
    def has_diag(self, color: Color) -> bool:
        return self.has_three(color, 0, 4, 8) \
            or self.has_three(color, 2, 4, 6)

    def is_winner(self, color: Color) -> bool:
        return (   self.has_row(color, start = 0)
                or self.has_row(color, start = 3)
                or self.has_row(color, start = 6)
                or self.has_col(color, start = 0)
                or self.has_col(color, start = 1)
                or self.has_col(color, start = 2)
                or self.has_diag(color)
               )

    def winner(self) -> WinnerColor:
        if self.is_winner(BLACK):
            return BLACK
        if self.is_winner(WHITE):
            return WHITE
        return EMPTY

    def set_draw_winner(self, color: WinnerColor) -> None:
        assert is_empty_black_white(color)
        self.draw_winner = color

    def static_eval_for_to_play(self) -> bool:
        win_color = self.winner()
        if (win_color == EMPTY) and (self.draw_winner != EMPTY):
            win_color = self.draw_winner
        if win_color == self.to_play:
            return True
        assert win_color == opponent(self.to_play)
        return False
    
    def legal_moves(self) -> list[int]:
        assert not self.end_of_game()
        moves = []
        for i in range(9):
            if self.board[i] == EMPTY:
                moves.append(i)
        return moves
        
    def code(self) -> int:
        c = 0
        for i in range(9):
            c = 3*c + self.board[i]
        return c

    # simulate one game from the current state until the end
    def simulate(self) -> tuple[WinnerColor, int]:
        num_moves = 0
        while not self.end_of_game():
            all_moves = self.legal_moves()
            move: int = random.choice(all_moves)
            self.play(move)
            num_moves += 1
        return self.winner(), num_moves

    def print(self) -> None:
        print(self.board[0:3])
        print(self.board[3:6])
        print(self.board[6:9])

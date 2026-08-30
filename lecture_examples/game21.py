# Cmput 455 sample code
# Implementing a simple game
# Start with a number (say 21) of tokens
# Move: a player can take 1, 2, or 3 tokens
# Win: a player who takes the last token wins
# Written by Martin Mueller.

from game import Game
from game_basics import EMPTY, opponent, WinnerColor

class Game21(Game):
    
    def __init__(self, num_tokens: int = 21) -> None:
        self.num_tokens = num_tokens
        self.reset_game()

    def end_of_game(self) -> bool:
        return self.num_tokens == 0

    def winner(self) -> WinnerColor:
        if self.end_of_game():
            return opponent(self.to_play)
        else: return EMPTY # no winner yet
    
    def __str__(self) -> str:
        return str(self.num_tokens)

    def legal_moves(self) -> list[int]:
        moves = []
        if self.num_tokens >= 3: moves.append(3)
        if self.num_tokens >= 2: moves.append(2)
        if self.num_tokens >= 1: moves.append(1)
        return moves

    def play(self, move: int)-> bool:
        assert(self.num_tokens >= move)
        self.num_tokens -= move
        super().play(move)
        return True
        
    def undo_move(self) -> None:
        move = self.last_move()
        self.num_tokens += move
        super().undo_move()

    def boolean_eval(self) -> bool:
        """Implement if your game allows a boolean evaluation.
           Evaluate from to_play's point of view.
        """
        assert self.end_of_game()
        return False

    def int_eval(self) -> int:
        assert False # not implemented

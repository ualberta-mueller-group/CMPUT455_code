# Cmput 455 sample code
# Abstract Base Class (ABC) - interface for two player game
# board, rules, and a random game simulator
# A specific game class needs to inherit from Game and implement all 
# methods marked as @abstractmethod.
# See game21.py for an example.
# Written by Martin Mueller.

from abc import ABC, abstractmethod
from typing import List
from game_basics import BLACK, opponent, Color, WinnerColor

class Game(ABC):
    
    def __init__(self) -> None:
        self.reset_game()

    def reset_game(self) -> None:
        self.to_play: Color = BLACK
        self.moves: List[int] = []

    def switch_to_play(self) -> None:
        self.to_play = opponent(self.to_play)

    @abstractmethod
    def end_of_game(self) -> bool:
        pass

    @abstractmethod
    def winner(self) -> WinnerColor:
        pass

    def move_number(self) -> int:
        return len(self.moves)
    
    @abstractmethod
    def __str__(self) -> str:
        """ Print game as str."""
        pass

    @abstractmethod
    def legal_moves(self) -> List[int]:
        pass

    def play(self, move: int) -> bool:
        """Returns True if the move was legal and could be played.
            If it returns False, the game state is unchanged.
        """
        self.moves.append(move)
        self.switch_to_play()
        return True
    
    def undo_move(self) -> None:
        """Override and call super().undo_move() at the end 
           if your implementation supports to undo a move.
        """
        self.moves.pop()
        self.switch_to_play()

    def reset_to_move_number(self, move_nr: int) -> None:
        """Override if your game supports a more efficient way,
           or does not allow to undo a move.
        """
        num_undos = self.move_number() - move_nr
        assert num_undos >= 0
        for _ in range(num_undos):
            self.undo_move()
        assert self.move_number() == move_nr

    def last_move(self) -> int:
        assert self.moves != []
        return self.moves[-1]
    
    @abstractmethod
    def boolean_eval(self) -> bool:
        """Implement if your game allows a boolean evaluation.
           Evaluate from to_play's point of view (negamax).
        """
        pass

    def boolean_eval_black(self) -> bool:
        """
           Evaluate from black player's point of view.
           Used only in plain boolean minimax.
        """
        return self.boolean_eval() == (self.to_play == BLACK)

    @abstractmethod
    def int_eval(self) -> int:
        """Implement if your game allows an integer evaluation.
           Evaluate from to_play's point of view.
        """
        pass
    
    def int_eval_for_color(self, color: Color) -> int:
        """
           Evaluate from black player's point of view.
           Used only in plain boolean minimax.
        """
        return self.int_eval() if self.to_play == BLACK else -self.int_eval()

    @abstractmethod
    def code(self) -> int:
        """Heuristic or exact hash code.
        """
        pass

    def simulate(self) -> tuple[WinnerColor, int]:
        """Simulate one game. Must override to use.
        """
        assert False

# Cmput 455 sample code
# Abstract Base Class (ABC) - interface for two player game
# board, rules, and a random game simulator
# A specific game class needs to inherit from Game and implement all 
# methods marked as @abstractmethod.
# See tic_tac_toe.py for an example.
# Written by Martin Mueller with help from Gemini.

from abc import ABC, abstractmethod
from game_basics import EMPTY, BLACK, WHITE, is_empty_black_white, opponent, \
     Color, WinnerColor

class Game(ABC):
    
    def __init__(self) -> None:
        self.reset_game()

    def reset_game(self) -> None:
        self.to_play: Color = BLACK
        self.moves: list[int] = []

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
    def legal_moves(self) -> list[int]:
        pass

    @abstractmethod
    def play(self, move: int)-> bool:
        """Returns True if the move was legal and could be played.
            If it returns False, the game state is unchanged.
        """
        pass
    

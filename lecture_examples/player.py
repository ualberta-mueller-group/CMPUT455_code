# Cmput 455 sample code
# Abstract Base Class for Game Player

from abc import ABC, abstractmethod
from game import Game

class Player(ABC):
    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def genmove(self, game_state: Game) -> int:
        pass

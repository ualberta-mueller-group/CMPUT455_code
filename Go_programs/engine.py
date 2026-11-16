from abc import ABC, abstractmethod
from board_base import GO_POINT, NO_POINT
from board_abstract import GoBoardAbstractBase

DEFAULT_KOMI = 6.5

class GoEngine(ABC):
    def __init__(self, name: str, version: float) -> None:
        """
        name : name of the player used by the GTP interface
        version : version number used by the GTP interface
        """
        self.name: str = name
        self.version: float = version
        self.komi: float = DEFAULT_KOMI

    @abstractmethod
    def get_move(self, board: GoBoardAbstractBase, color: int) -> GO_POINT:
        """
        name : name of the player used by the GTP interface
        version : version number used by the GTP interface
        """
        pass
        
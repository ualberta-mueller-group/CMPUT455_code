# Cmput 455 sample code
# game_basics.py: Game basics - constants and definitions for two player games
# Written by Martin Mueller. Cleaned up with help from Gemini.

from typing import Final, Literal, Tuple, Optional

# Ranges for different color types
Color = Literal[0, 1]
WinnerColor = Literal[0, 1, 2]
BoardColor = Literal[0, 1, 2, 3]

# Constants encoding the color of a point on the board
BLACK: Final[Color] = 0  # Also: 'X', 'B', "The first of the two colors"
WHITE: Final[Color] = 1  # Also: 'O', 'W', "The second of the two colors"
EMPTY: Final[WinnerColor] = 2  # Also: neutral, "not one of the players"
BORDER: Final[BoardColor] = 3 # Used for padding, "off the board"

COLOR_STR: Final[Tuple[str, str]] = ("Black", "White")
WINNER_STR: Final[Tuple[str, str, str]] = ("Black", "White", "Draw")
COLOR_CHAR: Final[Tuple[str, str]] = ('b', 'w')
sign: Final[Tuple[int, int]] = (1, -1)  # black  = positive, white = negative
opp: Final[Tuple[Color, Color]] = (WHITE, BLACK)  # opponent

def is_black_white(color: int) -> bool:
    return (color == BLACK) or (color == WHITE)
    
def is_empty_black_white(color: int) -> bool:
    return color in (EMPTY, BLACK, WHITE)

def opponent(color: Color) -> Color:
    assert is_black_white(color)
    return WHITE if color == BLACK else BLACK

def color_as_string(color: Color) -> str:
    assert is_black_white(color)
    return COLOR_STR[color]

def winner_as_string(color: WinnerColor) -> str:
    assert is_empty_black_white(color)
    return WINNER_STR[color]


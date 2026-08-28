# Cmput 455 unit tests for sample code
# game_basics.py: Game basics - constants and definitions for two player games
# Written by Martin Mueller

from game_basics import EMPTY, BLACK, WHITE, BORDER, is_black_white, \
is_empty_black_white, opponent, color_as_string, winner_as_string

def test_game_basics() -> None:
    assert(BLACK == 0)
    assert(WHITE == 1)
    assert(EMPTY == 2)
    assert(BORDER == 3)

    assert(is_black_white(BLACK))
    assert(is_black_white(WHITE))
    assert(not is_black_white(EMPTY))

    assert(is_empty_black_white(BLACK))
    assert(is_empty_black_white(WHITE))
    assert(is_empty_black_white(EMPTY))
    assert(not is_empty_black_white(4))
    assert(not is_empty_black_white(-1))

    assert(opponent(BLACK) == WHITE)
    assert(opponent(WHITE) == BLACK)

    assert(color_as_string(BLACK) == "Black")
    assert(color_as_string(WHITE) == "White")

    assert(winner_as_string(BLACK) == "Black")
    assert(winner_as_string(WHITE) == "White")
    assert(winner_as_string(EMPTY) == "Draw")

if __name__ == "__main__":
    test_game_basics()
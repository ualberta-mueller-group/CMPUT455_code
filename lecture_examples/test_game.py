# dummy game for testing of abstract game class.
# Minimal example of a working Game class
# Allows player to play one move.

from game_basics import EMPTY, BLACK, WHITE, opponent, \
     Color, WinnerColor
from game import Game

class Game0(Game):
# can play one move (any move) then game is over
    
    def end_of_game(self) -> bool:
        return self.move_number() > 0

    def winner(self) -> WinnerColor:
        return opponent(self.to_play) if self.end_of_game() else EMPTY
    
    def __str__(self) -> str:
        return str(self.moves)

    def legal_moves(self) -> list[int]:
        return [] if self.end_of_game() else [42]

    def boolean_eval(self) -> bool:
        raise NotImplementedError

    def int_eval(self) -> int:
        raise NotImplementedError
#----------------------------------------------------------

def assert_is_initial_state(game: Game0) -> None:
    assert game.to_play == BLACK
    assert game.moves == []
    assert game.winner() == EMPTY
    assert game.move_number() == 0

def test_initial_state() -> None:
    game = Game0()
    assert_is_initial_state(game)
    
def test_switch_to_play() -> None:
    game = Game0()
    game.switch_to_play()
    assert game.to_play == WHITE
    game.switch_to_play()
    assert game.to_play == BLACK
    assert_is_initial_state(game)

def test_str() -> None:
    game = Game0()
    text = str(game)
    print(game)
    print(text)
    assert text == "[]"
    game.play(42)
    text = str(game)
    assert text == "[42]"

def test_legal_moves() -> None:
    game = Game0()
    assert game.legal_moves() == [42]
    game.play(42)
    assert game.legal_moves() == []

def test_play_undo() -> None:
    game = Game0()
    game.play(42)
    assert game.moves == [42]
    assert game.to_play == WHITE    
    assert game.move_number() == 1
    assert game.last_move() == 42

    game.undo_move()
    assert_is_initial_state(game)
    
def test_winner() -> None:
    game = Game0()
    assert game.winner() == EMPTY
    game.play(42)
    assert game.winner() == BLACK
    game.undo_move()
    assert game.winner() == EMPTY
    game.switch_to_play()
    game.play(23)
    assert game.winner() == WHITE

def test_game() -> None:
    test_initial_state()
    test_switch_to_play()
    test_str()
    test_legal_moves()
    test_play_undo()
    test_winner()


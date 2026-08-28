from game_basics import EMPTY, BLACK, WHITE
from game21 import Game21

def test1() -> None:
    game = Game21(1)
    assert not game.end_of_game()
    assert game.winner() == EMPTY
    assert game.to_play == BLACK
    assert game.num_tokens == 1
    moves = game.legal_moves()
    assert len(moves) == 1
    assert moves[0] == 1

    game.play(1)
    assert game.end_of_game()
    assert game.winner() == BLACK
    assert game.to_play == WHITE
    assert game.num_tokens == 0

    game.undo_move()
    assert not game.end_of_game()
    assert game.winner() == EMPTY
    assert game.to_play == BLACK

def test21() -> None:
    game = Game21(21)
    assert not game.end_of_game()
    assert game.winner() == EMPTY
    assert game.to_play == BLACK
    assert game.num_tokens == 21
    moves = game.legal_moves()
    assert len(moves) == 3
    assert moves == [3, 2, 1]

    game.play(3)
    assert not game.end_of_game()
    assert game.winner() == EMPTY
    assert game.to_play == WHITE
    assert game.num_tokens == 18

    game.undo_move()
    assert not game.end_of_game()
    assert game.winner() == EMPTY
    assert game.to_play == BLACK
    assert game.num_tokens == 21

def test_game21() -> None:
    test1()
    test21()
    
if __name__ == "__main__":
    test_game21()
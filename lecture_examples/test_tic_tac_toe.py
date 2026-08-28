from game_basics import EMPTY, BLACK, WHITE
from tic_tac_toe import TicTacToe

def assert_is_initial_state(game: TicTacToe) -> None:
    assert game.board == [EMPTY] * 9
    assert game.legal_moves() == list(range(9))
    assert not game.end_of_game()
    assert game.winner() == EMPTY
    assert game.move_number() == 0

def test_initial_state() -> None:
    game = TicTacToe()
    assert_is_initial_state(game)

def test_play_and_undo() -> None:
    game = TicTacToe()
    game.play(4)
    assert game.board[4] == BLACK
    assert 4 not in game.legal_moves()

    game.undo_move()
    assert game.board[4] == EMPTY
    assert_is_initial_state(game)

def test_row_win() -> None:
    game = TicTacToe()
    # BLACK: 0, 1, 2 (Top row)
    for move in [0, 3, 1, 4, 2]:
        game.play(move)
    assert game.is_winner(BLACK)
    assert game.winner() == BLACK
    assert game.end_of_game()

def test_col_win() -> None:
    game = TicTacToe()
    # WHITE: 1, 4, 7 (Middle col)
    for move in [0, 1, 3, 4, 8, 7]:
        game.play(move)
    assert game.is_winner(WHITE)
    assert game.winner() == WHITE

def test_diag_win() -> None:
    game = TicTacToe()
    # BLACK: 0, 4, 8 (Main diagonal)
    for move in [0, 1, 4, 2, 8]:
        game.play(move)
    assert game.is_winner(BLACK)

def test_draw() -> None:
    game = TicTacToe()
    # Full board draw
    for move in [0, 1, 2, 4, 3, 5, 7, 6, 8]:
        game.play(move)
    assert game.end_of_game()
    assert game.winner() == EMPTY

def test_reset_to_move_number() -> None:
    game = TicTacToe()
    for m in [0, 4, 2]:
        game.play(m)
    game.reset_to_move_number(1)
    assert game.move_number() == 1
    assert game.board[0] == BLACK
    assert game.board[2] == EMPTY
    assert game.board[4] == EMPTY

    game.reset_to_move_number(0)
    assert_is_initial_state(game)

FULL_BOARD_CODE: int = 3 ** 9 - 1 # 222222222 in base 3, 2 = EMPTY

def test_code_encoding() -> None:
    game = TicTacToe()
    initial_code = game.code()
    assert initial_code == FULL_BOARD_CODE
    game.play(0)
    assert game.code() != initial_code

def test_simulation() -> None:
    game = TicTacToe()
    winner, num_moves = game.simulate()
    assert game.end_of_game()
    assert num_moves > 0
    
def test_tic_tac_toe() -> None:
    test_initial_state()
    test_play_and_undo()
    test_row_win()
    test_col_win()
    test_diag_win()
    test_draw()
    test_reset_to_move_number()
    test_code_encoding()
    test_simulation()

if __name__ == "__main__":
    test_tic_tac_toe()
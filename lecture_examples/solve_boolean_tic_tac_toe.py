from game_basics import WHITE
from tic_tac_toe import TicTacToe
from solve_boolean import MinimaxTimedFunction, solve_boolean
from minimax_boolean import minimax_boolean_timed
from negamax_boolean import negamax_boolean_timed

# An example game, with some mistakes by both. 
# Call solve after every move to check whether Black can win
def solve_boolean_tic_tac_toe(solver: MinimaxTimedFunction, 
            verbose: bool, negamax: bool):
    t = TicTacToe()
    t.set_draw_winner(WHITE)
    solve_boolean(t, solver, verbose, negamax, False)
    t.play(0)
    solve_boolean(t, solver, verbose, negamax, False)
    t.play(3)
    solve_boolean(t, solver, verbose, negamax, True)
    t.play(1)
    solve_boolean(t, solver, verbose, negamax, True)
    t.play(4)
    solve_boolean(t, solver, verbose, negamax, True)
    t.play(5)
    solve_boolean(t, solver, verbose, negamax, False)
    t.play(2)
    solve_boolean(t, solver, verbose, negamax, False)
    t.play(6)
    solve_boolean(t, solver, verbose, negamax, False)
    t.play(7)
    solve_boolean(t, solver, verbose, negamax, False)
    t.play(8)
    solve_boolean(t, solver, verbose, negamax, False)

def test(verbose: bool = False) -> None:
    if verbose: print("Test minimax:")
    solve_boolean_tic_tac_toe(minimax_boolean_timed, verbose, negamax=False)
    if verbose: print("Test negamax:")
    solve_boolean_tic_tac_toe(negamax_boolean_timed, verbose, negamax=True)

if __name__ == "__main__":
    test(verbose = True)

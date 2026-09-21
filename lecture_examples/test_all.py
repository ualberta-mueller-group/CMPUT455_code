# Test all code that can run without user input
import demere
import fold_or_bid
import solve_minimax_game21
import solve_negamax_game21
import test_game_basics
import test_game
import test_game21
import test_tic_tac_toe
import test_tic_tac_toe_simulation
import solve_boolean_tic_tac_toe
# TODO test generate_tree, blind_search_on_tree.py, heuristic_search_on_tree.py

def test_all() -> None:
    demere.test_demere()
    fold_or_bid.run_fold_or_bid(100)
    test_game_basics.test_game_basics()
    test_game.test_game()
    test_game21.test_game21()
    test_tic_tac_toe.test_tic_tac_toe()
    test_tic_tac_toe_simulation.test_tic_tac_toe_simulation(1000)
    solve_negamax_game21.test_solve_game21(21)
    solve_minimax_game21.test_solve_minimax_game21(21)
    solve_boolean_tic_tac_toe.test()


test_all()

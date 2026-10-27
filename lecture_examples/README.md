# CMPUT455 Sample Code for Lectures and Beyond
Python 3 code for the CMPUT 455 course at University of Alberta,
Martin Mueller, 2017-2026.
Sample code used in class, and extra examples.

Some of the code builds on earlier code via `import`. For example,
`game.py` imports `game_basics.py`. 
For simplicity, it is recommended to keep all code with dependencies in one directory.

## Lecture 1 and 3 - Introduction to Games
- `game_basics.py` Some basic definitions for two player games
- `game.py` `Game` class - abstract base class for two player games
- `player.py` `Player` class - abstract base class for Game Player
- `random_player.py` `RandomPlayer` plays random legal moves
- `game21.py` `Game21` class - simple game
    - `random_game21.py` use `RandomPlayer` to play `Game21`
- `tic_tac_toe.py` `TicTacToe` class - game board and rules
    - `game_3outcome.py` abstract base class for win-loss-draw games
       such as TicTacToe
    - `test_tic_tac_toe_simulation.py` Run random simulations for TicTacToe and report statistics on results and game length
- `play_match.py` Play a match between different players

- Unit tests: `test_game_basics.py`, `test_game.py`, `test_game21.py`, `test_tic_tac_toe`, `test_`

## Lecture 2 - Game of Go and Computer Go
- `go_2d.py` Code fragment - Go board implemented as "2-dimensional" list-of-lists
- `Go0` and `Go1` Random Go players - see `Go_programs` directory

## Lecture 5 - Decision-making
- `ev.py` Expected value of a random variable
- `fold_or_bid.py` Expected value example - simulate the "fold or bid" game
- `demo_petersburg.py` Simulation of the St. Petersburg Paradox
- Helper function: `user_input.py` Get user selection from a list of choices

## Lecture 6 - Game trees, DAGs, State Spaces
- `generate_tree.py` Generate artificial trees with constant branching factor b and depth d
    - `generate_tree_examples.py` Some examples
- `count_dag.py` Count nodes at each level of a TicTacToe- or Go-like 
artificial DAG

## Lecture 7 - Introduction to Search
- `blind_search_on_tree.py` Find a treasure hidden in a tree by blind search
    - `bfs.py` Breadth-first search on tree
    - `dfs.py` Depth-first search on tree
    - `tree.py` Tree implemented as dictionary of adjacency lists
- `heuristic_search_on_tree.py` Even a weak heuristic helps to find the treasure


## Lecture 8 - Boolean Minimax
- `minimax_boolean.py` minimax with separate treatment of AND and OR nodes
- `negamax_boolean.py` negamax reformulation of minimax - from `to_play`'s point of view
- `solve_minimax_game21.py`, `solve_negamax_game21.py` Solve Game21 with minimax and negamax
- `solve_boolean.py` Call a boolean solver for a game
    - `solve_boolean_tic_tac_toe.py` - "solve" TicTacToe with a boolean question - can Black win, or can Black not win?
- **New Sep 25, from class** `shortcut_eval.py` Shows analogy between cutoffs in boolean minimax, and shortcut evaluation in programming languages

## Quiz Extras (optional) 
In `lecture_examples/quiz_extras`
- `demere_q1_simulation.py` Quiz 1, simulation of De Mere's Game with 25 throws
- `game21_random_dp.py` Quiz 2, 21 Game random player winning probability with dynamic programming

## Lectures 9 - 10, Minimax Search and Alphabeta

### Search with bounds for games with three outcomes (win-draw-loss)
`negamax_3outcome.py` Check if a given player can win, count all draws as win for opponent
`test_negamax_3outcome.py` Call `negamax_3outcome.py` solver and print results
`test_negamax_3outcome_tictactoe.py` Solve some Tic Tac Toe positions and check result

### Minimax with integer values, Alphabeta algorithm
- `sample_tree.py`, `sample_tree_data.py` artificial game tree to illustrate minimax and alphabeta
- `naive_minimax.py`, `naive_negamax.py`, `test_naive_minimax_negamax.py` minimax and negamax without any pruning, tests on sample tree
    - `search_basics.py` Constants used by minimax programs
- `alphabeta.py` Alphabeta algorithm, negamax style
    - `test_alphabeta.py` Alphabeta on artificial tree
    - `test_alphabeta_tictactoe.py` Compare alphabeta and naive negamax in Tic Tac Toe
    - `alphabeta_verbose.py`, `test_alphabeta_verbose.py` Negamax alphabeta, print each step
    - `alphabeta_depth_limited.py` Version with limited search depth
        - `test_alphabeta_depth_limited_tictactoe.py`
    - `alphabeta_with_move.py` Alphabeta algorithm, plus remembering the move at the root

### Search enhancements: transposition table
- `transposition_table_simple.py` Python dictionary as Transposition Table
- `negamax_boolean_tt.py` Boolean Negamax with Simple Transposition Table
    - `solve_with_tt_tic_tac_toe.py` Solve Tic Tac Toe as a draw with two boolean searches as in Lecture 9
    - `solve_negamax_tt_game21.py` Solve Game21 up to 1000 tokens instantly
    - `negamax_boolean_tt_id.py` Negamax with iterative deepening and TT

### Counting the size of state spaces in tree and DAG model, solution trees
- `tic_tac_toe_estimate_tree.py` Simple tree model estimate
- `tic_tac_toe_count.py` Count states in tree and DAG models
- `tic_tac_toe_solve_all.py` Solve All TicTacToe States in tree and DAG models

## Lecture 12 - Simulation Methods
- `estimate_pi.py` Estimate pi with Monte Carlo sampling
    - `demo_pi.py` Same with UI
- `numerical_integration_MC.py` Numerical Integration with Monte Carlo sampling
- `simulation\_player.py`, `perfect\_player.py` more simple players for `play_match.py`

## Lecture 14 - Probabilistic Simulations
- `prob_select.py` Probabilistic selection from a list
- `bernoulli.py` Run repeated Bernoulli experiment
- `bernoulli_mystery.py` Guess the unknown parameter p of a repeated Bernoulli experiment

## Lecture 15 - UCB
- `ucb.py`, `demo\_ucb.py` UCB algorithm and demo

## Other
- NOT UPDATED YET `test_all.py` Run all unit tests, and test some other functions

## (For future lectures)


### (Lecture Neural Nets)
- `nn.py`, `nn3.py` Small nets with one and two hidden layers; examples

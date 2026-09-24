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


## Lecture 8 - Boolean minimax
- `minimax_boolean.py` minimax with separate treatment of AND and OR nodes
- `negamax_boolean.py` negamax reformulation of minimax - from `to_play`'s point of view
- `solve_minimax_game21.py`, `solve_negamax_game21.py` Solve Game21 with minimax and negamax
- `solve_boolean.py` Call a boolean solver for a game
    - `solve_boolean_tictactoe.py` - "solve" TicTacToe with a boolean question - can Black win, or can Black not win?

## Quiz extras (optional) 
In `lecture_examples/quiz_extras`
- `demere_q1_simulation.py` Quiz 1, simulation of De Mere's Game with 25 throws
- `game21_random_dp.py` Quiz 2, 21 Game random player winning probability with dynamic programming

## NOT YET Lectures 9 - 10, Minimax Search and Alphabeta

### Minimax with integer values, Alphabeta algorithm
- `minimax_sample_tree.py`, `minimax_sample_tree_data.py` artificial game tree to illustrate minimax and alphabeta
- `naive_minimax.py`, `naive_negamax.py`, `naive_minimax_negamax_test.py` minimax and negamax without any pruning, tests on sample tree
- `alphabeta.py` Alphabeta algorithm, negamax style
    - `alphabeta_test.py`
    - `alphabeta_depth_limited.py` Version with limited search depth
        - `alphabeta_depth_limited_tictactoe_test.py`

### Search enhancements: transposition table
- `transposition_table_simple.py` Python dictionary as Transposition Table
- `boolean_negamax_tt.py` Boolean Negamax with Simple Transposition Table
    - `tic_tac_toe_solve_with_tt.py` 

### Counting the size of state spaces in tree and DAG model, solution trees
- `tic_tac_toe_estimate_tree.py` 
- `tic_tac_toe_count_tree.py` 
- `tic_tac_toe_count_dag.py` 
- `tic_tac_toe_solve_all.py` Solve All TicTacToe States

## Other
- `test_all.py` Run all unit tests. Also tests some other functions
that do not need human input


## (For future lectures)

### (Lecture Simulation Methods)
- `estimate_pi.py` Estimate pi with Monte Carlo sampling
- `numerical_integration_MC.py` Numerical Integration with Monte Carlo sampling

### (Lecture Probabilistic Simulation Policies and Bernoulli Experiments)
- `prob_select.py` Probabilistic selection from a list
- `bernoulli.py` Run repeated Bernoulli experiment
- `bernoulli_mystery.py` Guess the unknown parameter p of a repeated Bernoulli experiment


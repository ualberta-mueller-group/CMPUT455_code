# CMPUT455 Sample Code for Lectures and Beyond
Python 3 code for the CMPUT 455 course at University of Alberta,
Martin Mueller, 2017-2026.
Sample code used in class, and extra examples.

Some of the code builds on earlier code via `import`. For example,
`game.py` imports `game_basics.py`. 
For simplicity, it is recommended to keep all code with dependencies in one directory.

## Lecture 1 - Introduction to Games
- `game_basics.py` Some basic definitions for two player games
- `game.py` `Game` class - abstract base class for two player games
- `player.py` `Player` class - abstract base class for Game Player
- `random_player.py` `RandomPlayer` plays random legal moves
- `game21.py` `Game21` class - simple game
- `tic_tac_toe.py` `TicTacToe` class - game board and rules
    - `game_3outcome.py` abstract base class for win-loss-draw games
       such as TicTacToe
    - `test_tic_tac_toe_simulation.py` Run random simulations for TicTacToe and report statistics on results and game length
- `play_match.py` Play a match between different players

- Unit tests: `test_game_basics.py`, `test_game.py`, `test_game21.py`, `test_tic_tac_toe`, `test_`

## Lecture 2 - Game of Go and Computer Go
- `go_2d.py` Code fragment - Go board implemented as "2-dimensional" list-of-lists
- `Go0` and `Go1` Random Go players - see `Go_programs` directory

## Other
- `test_all.py` Run all unit tests. Also tests some other functions
that do not need human input

## (Future Lecture Formalising Decision-Making)
- `ev.py` Expected value of a random variable
- `bernoulli.py` Sampling from a Bernoulli distribution
- `bernoulli_mystery.py` Guess the unknown winrate p from a Bernoulli distribution
- `fold_or_bid.py` Expected value example - simulate the "fold or bid" game
- `demo_petersburg.py` Simulation of the St. Petersburg Paradox
- Helper function: `user_input.py` Get user selection from a list of choices

## (Future Lecture Game trees, DAGs, State Spaces)
- `generate_tree.py` Generate artificial trees with constant branching factor b and depth d
    - `generate_tree_examples.py` Some examples
- `count_dag.py` Count nodes at each level of a TicTacToe- or Go-like 
artificial DAG

## (For Minimax lectures)
- (depends on not-yet-released code) `solve_game21.py` Solve Game21 with negamax

## (Old Lecture 12) Simulation Methods
- `estimate_pi.py` Estimate pi with Monte Carlo sampling
- `numerical_integration_MC.py` Numerical Integration with Monte Carlo sampling

## (Old Lecture 14) Probabilistic Simulation Policies and Bernoulli Experiments
- `prob_select.py` Probabilistic selection from a list
- `bernoulli.py` Run repeated Bernoulli experiment
- `bernoulli_mystery.py` Guess the unknown parameter p of a repeated Bernoulli experiment


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
- `tic_tac_toe.py` `TicTacToe` class - game board and rules
- `tic_tac_toe_simulation_test.py` Run random simulations for TicTacToe and report statistics on results and game length
- `play_match.py` Play a match between different players

## Lecture 2 - Game of Go and Computer Go
- `go_2d.py` Code fragment - Go board implemented as "2-dimensional" list-of-lists
- `Go0` and `Go1` Random Go players - see `Go_programs` directory

## Lecture Formalising Decision-Making
- `ev.py` Expected value of a random variable
- `fold_or_bid.py` Expected value example - simulate the "fold or bid" game
- `demo_petersburg.py` Simulation of the St. Petersburg Paradox
    - `user_input.py` Get user selection from a list of choices

## Lecture Game trees, DAGs, State Spaces
- `generate_tree.py` Generate artificial trees with constant branching factor b and depth d
    - `generate_tree_examples.py` Some examples
- `count_dag.py` Count nodes at each level of a TicTacToe- or Go-like 
artificial DAG

# (For Later lectures)

## (Old Lecture 12) Simulation Methods
- `estimate_pi.py` Estimate pi with Monte Carlo sampling
- `numerical_integration_MC.py` Numerical Integration with Monte Carlo sampling

## (Old Lecture 14) Probabilistic Simulation Policies and Bernoulli Experiments
- `prob_select.py` Probabilistic selection from a list
- `bernoulli.py` Run repeated Bernoulli experiment
- `bernoulli_mystery.py` Guess the unknown parameter p of a repeated Bernoulli experiment


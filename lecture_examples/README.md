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
- `blind\_search\_on\_tree.py` Find a treasure hidden in a tree by blind search
    - `bfs.py` Breadth-first search on tree
    - `dfs.py` Depth-first search on tree
    - `tree.py` Tree implemented as dictionary of adjacency lists
- `heuristic\_search\_on\_tree.py` Even a weak heuristic helps to find the treasure

## NOT YET Lectures 8 - 10, Minimax Search and Alphabeta

### Boolean minimax
- `boolean\_minimax.py` minimax with separate treatment of AND and OR nodes
- `boolean\_negamax.py` negamax reformulation of minimax - from `to_play`'s point of view
- TODO `solve_game21.py` Solve Game21 with negamax

    - `boolean\_negamax\_test\_tictactoe.py` - solve TicTacToe with two searches

### Minimax with integer values, Alphabeta algorithm
- `minimax\_sample\_tree.py`, `minimax\_sample\_tree\_data.py` artificial game tree to illustrate minimax and alphabeta
- `naive\_minimax.py`, `naive\_negamax.py`, `naive\_minimax\_negamax\_test.py` minimax and negamax without any pruning, tests on sample tree
- `alphabeta.py` Alphabeta algorithm, negamax style
    - `alphabeta\_test.py`
    - `alphabeta\_depth\_limited.py` Version with limited search depth
        - `alphabeta\_depth\_limited\_tictactoe\_test.py`

### Search enhancements: transposition table
- `transposition\_table\_simple.py` Python dictionary as Transposition Table
- `boolean\_negamax\_tt.py` Boolean Negamax with Simple Transposition Table
    - `tic\_tac\_toe\_solve\_with\_tt.py` 

### Counting the size of state spaces in tree and DAG model, solution trees
- `tic\_tac\_toe\_estimate\_tree.py` 
- `tic\_tac\_toe\_count\_tree.py` 
- `tic\_tac\_toe\_count\_dag.py` 
- `tic\_tac\_toe\_solve\_all.py` Solve All TicTacToe States
- `` 
- `` 

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


# Go Programs
- Simple Go player demos for the CMPUT 455 course at University of Alberta
- Python 3 code
- By Martin Mueller and many CMPUT 455 TA, 2017-2026

#### Dependencies
- `numpy` for all code
- `unittest` for unit tests


## Go0 and Go1 Random Players
- Some documentation is in the code
- `Go0` is "pure random", cannot finish a game
- `Go1` stays clear of "simple eyes"
- Both only pass if there are no other moves

### Run from command line

`python3 Go0.py`

or

`python3 Go1.py`

### Run from GoGui or other GTP-based user interface
- Add to list of Go programs. Details depend on UI used.

### Discover and run all unit tests
`python -m unittest`

## Go2 Player
- Same algorithm as Go1, but with a faster Go board.

## Go3 Player
- Flat Monte Carlo player. Options:
- `--sim` number of simulations per move, so total playouts=sim * legal moves. default=10
- `--moveselect` type of move selection: `simple` (default) or `ucb`
- `--simrule` type of simulation policy: `random` (default) or `rulebased`
- `--movefilter` whether use move filter or not: `True` or `False` (default)

### todo
- Probably `--movefilter True` would be stronger - test it and make it the default.
- Play test games vs `GoHeuristicPlayer` on different board sizes

## GoHeuristicPlayer
- based on `Fuego AveragePlayer`.
- 1 ply search, maximises the difference of average liberties, own vs opponent
- Tends to build long chains, and also likes to reduce opponent liberties

## Go4 Player
- Flat Monte Carlo
- Uses simple MoGo-style features from the michi program `https://github.com/pasky/michi`
- Options: similar to `Go3`, see `parse_args`

## Go5 Player
- MCTS
- Options: similar to `Go3`, see `parse_args`
- New option: `--in_tree_knowledge` (default None) whether to use move knowledge to initialise a new node or not

# Cmput 455 sample code
# Estimate number of states in a DAG for games such as TicTacToe or GoMoku.
# Ignores rules of the game, just counts how many ways there are to
# place stones on the board
# Written by Martin Mueller

import math

type Row = list[int]
type Table = list[Row]

# Uses "Pascal's Triangle" to compute the choose(.,.) values
def compute_choose_table(n: int) -> Table:
    assert n > 0
    table: Table = [[1] * (r + 1) for r in range(n + 1)]
    for r in range(2, n + 1):
        for k in range(1, r):
            table[r][k] = table[r - 1][k - 1] + table[r - 1][k]
    # print(table)
    return table

# Access table entry, with error checking
def get(table: Table, n: int, k: int) -> int:
    assert 0 <= k <= n
    assert len(table) > n
    return table[n][k]
    
# Level by level number of positions in DAG
# n points total on the board, black moves first
def compute_game_DAG_size(n: int) -> None:
    choose: Table = compute_choose_table(n)
    positions_at_depth: Row = [0] * (n+1) # possible depths are 0,...,n
    for num_stones in range(n+1):
        white: int = num_stones // 2
        black: int = num_stones - white
        black_pos: int = get(choose, n, black)
        white_pos: int = get(choose, n-black, white)
        pos: int = black_pos * white_pos
        positions_at_depth[num_stones] = pos
        if num_stones > 0:
            print("Branching factor:", pos /
                                       positions_at_depth[num_stones-1])
        print(pos, "positions at depth ", num_stones)
    print("Total positions: ", sum(positions_at_depth))
    print("Compare with factorial:", math.factorial(n))

if __name__ == "__main__":
    print("Simplified TicTacToe:")
    compute_game_DAG_size(9)
    print("\nSimplified 7x7 Go:")
    compute_game_DAG_size(7*7)
#     print("\nSimplified 19x19 Go:")
#     compute_game_DAG_size(19*19)

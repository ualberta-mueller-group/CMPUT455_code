# Cmput 455 sample code
# Play match between several players
# Written by Martin Mueller

from game_basics import BLACK, WHITE, EMPTY, WinnerColor
from game import Game
from player import Player

Stats = list[int]

# Which player should play the next move?
# Alternate between even and odd number of moves
def select_player(num_moves: int, player1: Player, player2: Player) -> Player:
    if num_moves % 2 == 0:
        return player1
    else:
        return player2
    
def play_game(g: Game, player1: Player, player2: Player, verbose: bool = False) -> WinnerColor:
    num_moves: int = 0
    while not g.end_of_game():
        player = select_player(num_moves, player1, player2)
        g.play(player.genmove(g))
        num_moves += 1
    if verbose:
        print("Game winner:", g.winner(), "Moves:", g.moves)
    return g.winner()

def play_match(game: Game, player1: Player, player2: Player, num_games: int) -> Stats:
    stats: Stats = [0, 0, 0]
    for _ in range(num_games):
        winner: WinnerColor = play_game(game, player1, player2)
        stats[winner] += 1
    print_stats(stats, player1, player2)
    return stats

def print_stats(stats: Stats, player1: Player, player2: Player) -> None:
    print(f"{stats[BLACK]} wins for {player1.name()}, "
          f"{stats[WHITE]} wins for {player2.name()}, "
          f"{stats[EMPTY]} draws")

def play_match_both_colors(game: Game, player1: Player, player2: Player, num_games: int) -> None:
    # player1 is X
    stats1: Stats = play_match(game, player1, player2, num_games)
    # player1 is O
    stats2: Stats = play_match(game, player2, player1, num_games)
    # Compute combined statistics - reversed colors in second match
    stats1[BLACK] += stats2[WHITE]
    stats1[WHITE] += stats2[BLACK]
    stats1[EMPTY] += stats2[EMPTY]
    print("Total:")
    print_stats(stats1, player1, player2)
    wins: float = (stats1[BLACK] + 0.5 * stats1[EMPTY]) / (2 * num_games)
    print("Percentage for {0} = {1:.2f}".format(player1.name(), 100 * wins))


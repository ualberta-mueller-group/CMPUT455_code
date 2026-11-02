# Cmput 455 sample code
# Play match between several TicTacToe players
# Written by Martin Mueller

from game import Game
from tic_tac_toe import TicTacToe
from player import Player
from perfect_player import PerfectPlayer
from random_player import RandomPlayer
from simulation_player import SimulationPlayer
from play_match import play_match_both_colors

def round_robin_matches() -> None:
    player1 = SimulationPlayer(10)
    player2 = PerfectPlayer()
    player3 = RandomPlayer()
    play_match_both_colors(TicTacToe(), player1, player2, 100)
    play_match_both_colors(TicTacToe(), player1, player3, 100)
    play_match_both_colors(TicTacToe(), player2, player3, 100)

def self_play_matches() -> None:
    player: Player = SimulationPlayer(10)
    play_match_both_colors(TicTacToe(), player, player, 100)
    player = RandomPlayer()
    play_match_both_colors(TicTacToe(), player, player, 100)
    player = PerfectPlayer()
    play_match_both_colors(TicTacToe(), player, player, 100)

def scaling_matches() -> None:
    #player2 = PerfectPlayer()
    player2 = RandomPlayer()
    num_sim = 1
    for _ in range(4):
        player1 = SimulationPlayer(num_sim)
        play_match_both_colors(TicTacToe(), player1, player2, 100)
        num_sim *= 10
    
def sim_1000_and_perfect_vs_random() -> None:
    player1 = SimulationPlayer(1000)
    player2 = PerfectPlayer()
    player3 = RandomPlayer()
    play_match_both_colors(TicTacToe(), player1, player3, 1000)
    play_match_both_colors(TicTacToe(), player2, player3, 1000)
    
round_robin_matches()
#self_play_matches()
#scaling_matches()
#sim_1000_and_perfect_vs_random()

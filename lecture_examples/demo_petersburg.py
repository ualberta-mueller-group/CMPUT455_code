# Cmput 455 sample code
# Simulation for the St. Petersburg paradox game.
# Play the St. Petersburg Paradox. 
# Demo 1: Place one bet, then the game is simulated 1000 times.
# Written by Martin Mueller

import random
from user_input import user_input

type Histogram = dict[int, int]

def coin_flip() -> bool:
    return random.random() < 0.5

def simulate_petersburg() -> int:
    pot = 2 # The bank puts $2 in the pot originally
    while True:
        if coin_flip(): # Each round you flip a coin
            return pot # If tail, the game ends and you win the whole pot
        else:
            pot *= 2 # If head, the bank doubles the pot

def record(histogram: Histogram, value: int) -> None:
        if value in histogram:
            histogram[value] += 1
        else:
            histogram[value] = 1

def print_histogram(histogram: Histogram) -> None:
    print("\nSimulation Results:")
    for key in sorted(histogram.keys()):
        print(f"{key} occurred {histogram[key]} times")

def user_bet() -> int:
    return int(input("Your bet: "))

def print_stats(round: int, score: int, max_win: int) -> None:
    print(f"\nAverage score after {round} rounds: "
          f"{score / round:.2f}, "
          f"max. win {max_win}")

def petersburg_demo(do_bet: bool, max_rounds: int) -> None:
    bet = user_bet() if do_bet else 0
    histogram: Histogram = dict()
    max_rounds = 1000 if do_bet else 1000000000
    score: int = 0
    print_time: int = 2
    max_win: int = 0

    for round in range(1, max_rounds + 1):
        win = simulate_petersburg()
        score += win - bet
        if win > max_win:
            max_win = win
        if do_bet:
            print(f"You bet {bet} and gained {win}, "
                  f"your win/loss is {win - bet}. "
                  f"Score after {round} rounds: {score}")
        record(histogram, win)
        if (not do_bet) and round >= print_time:
            print_stats(round, score, max_win)
            print_histogram(histogram)
            print_time *= 2
    print_stats(round, score, max_win)
    print_histogram(histogram)

if __name__ == "__main__":
    random.seed() # initialize random generator
    print("Play St. Petersburg Paradox")
    sim_rounds = 1000
    print(f"Demo 1: Bet and Play {sim_rounds} rounds")
    print("Demo 2: Simulate Forever")
    choice: int = user_input([1, 2], "Choose a Demo:")
    do_bet: bool = (choice == 1)
    max_rounds = sim_rounds if do_bet else 1000000000
    petersburg_demo(do_bet, max_rounds)

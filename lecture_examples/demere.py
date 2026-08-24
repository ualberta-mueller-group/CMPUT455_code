# Cmput 455 sample code
# De Mere's games demo (Lecture 1)
# Written by Martin Mueller

import random

def throw6() -> bool:
    return random.random() < 1/6
    
def game1() -> bool:
    for _ in range(4):
        if throw6(): return True
    return False

def throw_double6() -> bool:
    return throw6() and throw6()

def game2() -> bool:
    for _ in range(24):
        if throw_double6(): return True
    return False

def analyse(game, game_name):
    num_tries = 1000
    wins = 0
    for _ in range(num_tries):
        if game():
            wins += 1
    print(f"{game_name}: {wins} wins, {num_tries - wins} losses "
          f"in {num_tries} tries, win percentage: {wins / num_tries:.4f}")

if __name__ == "__main__":
    random.seed()
    analyse(game1, "Game 1")
    analyse(game2, "Game 2")


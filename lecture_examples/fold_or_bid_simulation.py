# Cmput 455 sample code
# Simulate Fold or Bid Game
# Written by Martin Mueller

import numpy as np
from random import choices
from collections import Counter

def simulate(w, num_tries):
    print(f"\nSimulate w = {w:.2f}")
    items = ['win', 'loss']
    weights = [w, 1-w]
    result = choices(items, weights, k = num_tries)
    count = Counter(result)
    value = dict([('win', 5), ('loss', -3)])
    score = sum(count[item] * value[item] for item in items)
    return score

def simulate_and_print(w, num_tries):
    score = simulate(w, num_tries)
    score_per_try = score / num_tries
    print(f"After {num_tries} tries with winning probability {w:.2f}:")
    print(f"Total score {score}, per try: {score_per_try}:")
    fold_score = -1
    if score_per_try > fold_score:
        print("bid is better")
    else:
        print("fold is better")
    

if __name__ == "__main__":
    print("=== Example : EV for Fold or Bid Game ===\n")
    print("EV for fold: always -1\n")
    print("EV for bid: check different winning probabilities w")
    num_tries = 1000
    w_range = np.arange(0.2, 0.31, 0.01) # try 0.2, 0.21, ..., 0.3
    for w in w_range:
        simulate_and_print(w, num_tries)

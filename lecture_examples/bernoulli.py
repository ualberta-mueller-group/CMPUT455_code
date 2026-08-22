# Cmput 455 sample code
# Sampling from a Bernoulli distribution:
#   1 with probability p
#   0 with probability 1 - p
# Written by Martin Mueller

import random

def bernoulli_experiment(p: float) -> int:
    # int(boolean): int(True) = 1, int(False) = 0
    return int(random.random() < p)

def print_stats(n: int, p: float, wins: int) -> None:
    print("After {n} simulations, estimate of {p:f} = {wins / n:f}")

def bernoulli_sample(p: float, limit: int) -> float:
    print("\nRepeated Bernoulli experiment for {:f}, {} iterations".format(p, limit))
    next_print_time: int = 1
    wins: int = 0
    for n in range(1, limit + 1):
        wins += bernoulli_experiment(p)
        if n >= next_print_time:
            print_stats(n, p, wins)
            next_print_time *= 2
    print_stats(n, p, wins)
    return wins / limit

if __name__ == "__main__":
    random.seed()
    bernoulli_sample(0.5, 1000000)
    bernoulli_sample(0.1, 1000000)
    bernoulli_sample(0.9999, 1000000)
    bernoulli_sample(0.00001, 1000000)

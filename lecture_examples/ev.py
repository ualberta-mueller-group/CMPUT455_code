# Cmput 455 sample code
# Expected value (EV) for discrete probabilities and values
# Written by Martin Mueller

from operator import mul

def ev(p: list[float], values: list[int]) -> float:
    return sum(map(mul, p, values), 0.0)

if __name__ == "__main__":
    print()
    print("=== Example 1: Six-sided fair die ===")
    prob = 6 * [1 / 6]
    values = [i for i in range(1, (6 + 1))]
    print(f"EV for fair die = {ev(prob, values):.3f}\n")

    print("=== Example 2: unfair (loaded) die ===")
    p_6 = 0.3
    p_other = (1-p_6) / (6 - 1)
    prob = 5 * [p_other] + [p_6]
    values = [i for i in range(1, (6 + 1))]
    print(f"EV for unfair die = {ev(prob, values):.3f}\n")

    print("=== Example 3: 1000-sided fair die ===")
    num_sides = 1000
    prob = num_sides * [1 / num_sides]
    values = [i for i in range(1, (num_sides + 1))]
    print(f"EV for {num_sides}-sided fair die = {ev(prob, values):.3f}\n")


# Cmput 455 sample code
# Estimate pi with random sampling
# How many random points within the square (0,1) x (0,1)
# are within the quarter circle x>0, y>0, x^2 + y^2 < 1
# Prints estimates after 1, 2, 4, 8, ... samples
# Written by Martin Mueller

import random
import math

def print_estimate(num_simulations: int, in_circle: int) -> None:
    estimate = 4 * in_circle / num_simulations
    relative_error = abs(math.pi - estimate)/math.pi
    print(f"After {num_simulations} simulations, \
            estimate of pi = {estimate}, \
            relative error = {relative_error:.2e}")
    
if __name__ == "__main__":
    random.seed()
    next_print: int = 1
    num_simulations: int = 0
    in_circle: int = 0

    while True:
        if num_simulations >= next_print:
            print_estimate(num_simulations, in_circle)
            next_print *= 2
        x: float = random.random()
        y: float = random.random()
        num_simulations += 1
        if x*x + y*y < 1:
            in_circle += 1

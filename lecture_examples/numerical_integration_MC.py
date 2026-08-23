# Cmput 455 sample code
# Numerical Integration using the Monte Carlo method
# Code by Gemini based on an older example.

import math
import random
from typing import Callable

def monte_carlo_integrate(
    f: Callable[[float], float],
    xmin: float,
    xmax: float,
    num_samples: int,
) -> float:
    """Approximate the integral using Monte Carlo sampling.
       area = (xmax - xmin) * average(f(x_i)) for random x_i in [xmin, xmax]
    """
    sample_sum = sum(
        f(xmin + (xmax - xmin) * random.random())
        for _ in range(num_samples)
    )
    approx_area = (xmax - xmin) * (sample_sum / num_samples)
    print(f"Numerical integral on [{xmin}, {xmax}] = {approx_area:.6f}")
    return approx_area
  
def f(x: float) -> float:
    """Example: f(x) = x^2 - 1"""
    return x * x - 1.0

#---------------------------------------------------------
num_samples: int = 1000
print("f(x) = sin(x), true value = 2")
monte_carlo_integrate(math.sin, 0.0, math.pi, num_samples)
print("f(x) = x^2 - 1, true value = 323.33333...")
monte_carlo_integrate(f, 0.0, 10.0, num_samples)

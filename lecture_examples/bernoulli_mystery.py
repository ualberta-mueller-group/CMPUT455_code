# Cmput 455 sample code
# Guess the unknown winrate p from a Bernoulli distribution
# Written by Martin Mueller

from bernoulli import bernoulli_experiment
from user_input import user_input_int, user_input_float
import random

p = random.random()
n: int = user_input_int("I created a random p for Bernoulli experiments. How many experiments should I do? ")

wins: int = 0
for i in range(n):
    wins += bernoulli_experiment(p)
print(f"{n} runs {wins} wins, empirical winrate {wins / n}")

guessed_p: float = user_input_float("Guess the value of p: ")
print(f"You guessed {guessed_p}. The true value is {p}")

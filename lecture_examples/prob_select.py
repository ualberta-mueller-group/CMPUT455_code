# Cmput 455 sample code
# Sampling from a discrete probability distribution
# Using the random.choices function
# Written by Martin Mueller, cleaned up and generalised with Gemini

import random
from collections import Counter

def sample(weighted_items: list[tuple[str, int]], num_tries: int) -> None:
    """
    Sample from discrete distribution of (item, weight) tuples.
    """
    items, weights = zip(*weighted_items)
    total_weight = sum(weights)

    print(f"Items/Weights: {weighted_items}")
    print(f"Sum of Weights: {total_weight}")

    # Generate samples
    random.seed()
    choices = random.choices(items, weights, k = num_tries)
    print(f"{num_tries} Sample Choices: {choices}\n")

    # Count empirical frequencies
    count = Counter(choices)

    # Output empirical vs expected probabilities
    for item, weight in weighted_items:
        empirical_freq = count[item] / num_tries
        expected_freq = weight / total_weight
        print(
            f"{item:10s} weight {weight:2d}, "
            f"chosen {count[item]} times, "
            f"empirical frequency {empirical_freq:.2f}, "
            f"expected {expected_freq:.2f}"
        )
    print("-" * 60)

if __name__ == "__main__":
    print("=== Example 1: Airplane Seating ===")
    seats = [
        ("Window", 2),
        ("Aisle", 1),
    ]
    sample(seats, num_tries = 20)
    
    print("=== Example 2: Drinks ===")
    drinks = [
        ("Coffee", 30),
        ("Tea", 20),
        ("OJ", 40),
        ("Milk", 7),
        ("Root Beer", 3),
    ]
    sample(drinks, num_tries = 100)

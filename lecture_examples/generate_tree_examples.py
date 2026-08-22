# Cmput 455 sample code
# Tests for generate_tree.py
# Written by Martin Mueller

from generate_tree import generate_tree
from pprint import pprint

def print_example(b: int, d: int) -> None:
    tree, num_nodes = generate_tree(b, d)
    print(f"Tree of branching factor {b} and depth {d}"
          f" has {num_nodes} nodes:")
    pprint(tree)
    
print_example(0, 0)
print_example(2, 1)
print_example(3, 2)
print_example(1, 10)
print_example(10, 1)
print_example(2, 5)
#print_example(3, 9) # a bit big
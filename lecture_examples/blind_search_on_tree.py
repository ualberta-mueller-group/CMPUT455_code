# Cmput 455 sample code
# Treasure hunt with blind search
# builds a tree and hides the treasure in a random node.
# Then runs several blind search algorithms repeatedly
# and prints statistics about their success, and nodes searched.
# Written by Martin Mueller

import random
from typing import Dict, List, Tuple, Callable
from generate_tree import generate_tree
from bfs import bfs
from dfs import dfs
from tree import Tree

SearchFunction = Callable[[Tree, int, int], Tuple[bool, int]]

def sample_random_path(tree: Tree, start: int, treasure: int) -> Tuple[bool, int]:
    """Single random sample on tree. Follow a random path and look for treasure. Returns (found, num_nodes)"""
    num_nodes: int = 1
    current: int = start
    if current == treasure:
        return True, num_nodes
    while tree[current]: # while current has children, pick one to go next
        current = random.choice(tree[current])
        num_nodes += 1
        if current == treasure:
            return True, num_nodes
    return False, num_nodes

def sample(tree: Tree, start: int, treasure: int) -> Tuple[bool, int]:
    """Repeated random sampling on tree. Returns (found, num_nodes)"""
    total_nodes: int = 0
    num_tries: int = 1000
    for _ in range(num_tries):
        found, num_nodes = sample_random_path(tree, start, treasure)
        total_nodes += num_nodes
        if found:
            return True, total_nodes
    return False, total_nodes

def do_test(tree: Tree, name: str, search: SearchFunction, num_experiments: int) -> None:
    """Run a given search function repeatedly and prints search performance stats."""
    print("Search with", name)
    num_success: int = 0
    total_nodes: int = 0
    for _ in range(num_experiments):
        # hide treasure in random node in tree
        treasure: int = random.choice(list(tree.keys())) 
        found, num_nodes = search(tree, 0, treasure)
        if found:
            num_success += 1
        total_nodes += num_nodes
    print(f"{num_experiments} Runs "
          f"{num_success} Successes "
          f"{total_nodes / num_experiments:.2f} Average nodes searched")

tree, num_nodes = generate_tree(3, 6)
print("Tree with", num_nodes, "Nodes.")
num_experiments: int = 1000
do_test(tree, "Dfs", dfs, num_experiments)
do_test(tree, "Bfs", bfs, num_experiments)
do_test(tree, "Random sampling", sample, num_experiments)

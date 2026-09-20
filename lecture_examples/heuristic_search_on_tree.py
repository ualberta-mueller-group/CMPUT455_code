# Cmput 455 sample code
# Treasure hunt with a heuristic
# With probability p, the heuristic gives a correct move
# which stays on the precomputed path to the treasure.
# With prob. 1-p, and also in case the agent is already off the path, 
# it plays randomly.
# Written by Martin Mueller

import random
from typing import Dict, List, Tuple
from bernoulli import bernoulli_experiment
from dfs import dfs
from tree import Tree
from generate_tree import generate_tree

FAILED: int = -1 # no longer on path to treasure
ROOT_ID: int = 0
DEBUG: bool = False

# Single random sample on tree
# Each step follows the path to treasure with probability p
# returns (found, num_nodes)
def sample_random_path(
    tree: Tree, 
    start: int, 
    treasure: int, 
    path: List[int], 
    p: float
) -> Tuple[bool, int]:
    num_nodes: int = 1
    current: int = start
    if current == treasure:
        return True, num_nodes
    path_index: int = 1 # skip root
    while tree[current]: # while current has children, pick one to go next
        if path_index != FAILED and bernoulli_experiment(p):
            current = path[path_index]
        else:
            current = random.choice(tree[current])
        if DEBUG: print("searching node", current)
        num_nodes += 1
        if current == treasure:
            return True, num_nodes
        if path_index != FAILED:
            if current == path[path_index]:
                path_index += 1
            else:
                path_index = FAILED
    return False, num_nodes

# Repeated random sampling on tree
# returns (found, num_nodes)
def sample(
    tree: Tree, 
    start: int, 
    treasure: int, 
    path: List[int], 
    p: float
) -> Tuple[bool, int]:
    total_nodes_searched: int = 0
    for _ in range(1000):
        found: bool
        num_nodes: int
        found, num_nodes = sample_random_path(tree, start, treasure, path, p)
        total_nodes_searched += num_nodes
        if found:
            return True, total_nodes_searched
    return False, total_nodes_searched

def find_path_to_treasure(tree: Tree, start: int, treasure: int, path: List[int]) -> None:
    """Since our Tree does not have parent pointers, we use search here."""
    dfs(tree, start, treasure, path)

def do_test(tree: Tree, name: str, num_samples: int, p: float, verbose: bool = False) -> None:
    print ("Search with", name)
    print ("Heuristic accuracy", p)
    num_success: int = 0
    total_nodes_searched: int = 0
    for _ in range(num_samples):
        # hide treasure in random node in tree
        treasure: int = random.choice(list(tree.keys()))
        ptt: List[int] = [] # path_to_treasure
        find_path_to_treasure(tree, ROOT_ID, treasure, ptt)
        if verbose:
            print(f"treasure {treasure}, path {ptt}")
        found: bool
        num_nodes: int
        found, num_nodes = sample(tree, ROOT_ID, treasure, ptt, p)
        if found:
            num_success += 1
        total_nodes_searched += num_nodes
    print(f"{num_samples} Runs "
          f"{num_success} Successes "
          f"{total_nodes_searched / num_samples:.2f} Average nodes searched")

if __name__ == "__main__":
    tree: Tree
    num_nodes: int
    tree, num_nodes = generate_tree(3, 6)
    print("Tree with", num_nodes, "Nodes.")
    num_samples: int = 100
    p: float
    for p in [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]: 
        do_test(tree, "Random sampling", num_samples, p)

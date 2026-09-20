# Cmput 455 sample code
# Breadth-first search on a tree
# This will NOT work on general graphs
# Written by Martin Mueller

from collections import deque

# breadth-first search on tree
# returns (found, num_nodes)
def bfs(tree, start, treasure):
    num_nodes = 0
    queue = deque()
    queue.append(start)
    while len(queue) > 0:
        node = queue.popleft()
        num_nodes += 1
        if node == treasure:
            return True, num_nodes
        for child in tree[node]:
            queue.append(child)
    return False, num_nodes

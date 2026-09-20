# Cmput 455 sample code
# Depth-first search on a tree
# This will NOT work on general graphs
# Written by Martin Mueller

from typing import Dict, List, Optional, Tuple

Tree = Dict[int, List[int]]

def dfs(
    tree: Tree, 
    node: int, 
    treasure: int, 
    path: Optional[List[int]] = None
) -> Tuple[bool, int]:
    """
    Depth-first search on a tree to find a treasure node.
    
    Parameters:
        tree: Dictionary mapping nodes to lists of child nodes.
        node: Current node being evaluated.
        treasure: Target node to search for.
        path: Optional list to collect the traversal path to the treasure in-place.
        
    Returns:
        (found, num_nodes_searched)
    """
    num_nodes_searched: int = 1
    
    if path is not None:
        path.append(node)
        
    if node == treasure:
        return True, num_nodes_searched
        
    for child in tree[node]:
        found, child_nodes = dfs(tree, child, treasure, path)
        num_nodes_searched += child_nodes
        if found:
            return True, num_nodes_searched

    # Backtrack if path does not lead to treasure
    if path is not None:
        path.pop()

    return False, num_nodes_searched
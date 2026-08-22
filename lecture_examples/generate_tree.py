# Cmput 455 sample code
# Generate a tree of depth d and uniform branching factor b
# Written by Martin Mueller

type AdjList = dict[int, list[int]]
type Tree = AdjList

def generate_tree(b: int, d: int) -> tuple[Tree, int]:
    """Creates a tree of depth d and uniform branching factor b 
       in a depth-first manner.
       
       Nodes are numbered depth-first as well. The root is 0.
    
    Returns:
        A tuple containing (tree, total_node_count).
    """
    tree: Tree = {}

    def generate_recursively(level: int, node_id: int) -> tuple[int, int]:
        children: list[int] = []
        next_id = node_id + 1

        if level < d:
            for _ in range(b):
                child_id, next_id = generate_recursively(level + 1, next_id)
                children.append(child_id)

        tree[node_id] = children
        return node_id, next_id

    _, total_nodes = generate_recursively(level=0, node_id=0)
    return tree, total_nodes
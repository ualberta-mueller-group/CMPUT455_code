# Cmput 455 sample code
# Tests alphabeta on sample tree
# Written by Martin Mueller

from negamax_naive import negamax
from alphabeta_verbose import call_alphabeta
from sample_tree import SampleTree
from sample_tree_data import node_id

t = SampleTree()

result = call_alphabeta(t)
print(f"alphabeta negamax search result = {result}")
assert result == 6

def child1():
    print("child 1 loses")
    return False

def child2():
    print("child 2 loses")
    return False

def child3():
    print("child 3 wins")
    return True

def child4():
    print("child 4 who cares?")
    return False

def child5():
    print("child 5 who cares?")
    return False

print("OR node")
or_node_win = child1() or child2() or child3() or child4() or child5()
print("OR node win =", or_node_win)

print("\nAND node")
and_node_win = child1() and child2() and child3() and child4() and child5()
print("AND node win =", and_node_win)

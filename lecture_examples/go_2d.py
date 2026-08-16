# Cmput 455 sample code
# go_2d.py - sketch of simple Go board implementation
# List of lists in Python
# Outer list: list of rows
# Inner lists: one list of points for each row
# Written by Martin Mueller

EMPTY = 0
BLACK = 1
WHITE = 2   
MAXSIZE = 7

def print_board(board):
    for row in board:
        print(*row)
    print()
    
board = [[EMPTY for x in range(MAXSIZE)] 
                for y in range(MAXSIZE)]
print_board(board)
board[3][4] = BLACK
print_board(board)
board[0][6] = WHITE
print_board(board)

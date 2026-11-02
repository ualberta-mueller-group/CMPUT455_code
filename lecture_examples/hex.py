# Cmput 455 sample code
# Game of Hex implementation
# This seems to work but it still very slow.
# It does not have any game-specific knowledge

from game_basics import BLACK, WHITE, EMPTY, BORDER, BoardColor, Color, WinnerColor, WINNER_STR, opponent
from game import Game

# Board directions on a standard Hex rhombus grid (Row offset, Col offset)
HEX_DIRECTIONS = [
    (-1,  0), (-1, 1),  # Top-Left, Top-Right
    ( 0, -1), ( 0, 1),  # Left, Right
    ( 1, -1), ( 1, 0)   # Bottom-Left, Bottom-Right
]

# Todo how to make fast undo?
class UnionFind:
    """ Union Find with path compression and rank."""
    def __init__(self, size: int) -> None:
        self.parent: list[int] = list(range(size))
        self.rank: list[int] = [0] * size

    def find(self, i: int) -> int:
        if self.parent[i] == i:
            return i
        self.parent[i] = self.find(self.parent[i])  # Path compression
        return self.parent[i]

    def union(self, i: int, j: int) -> None:
        root_i = self.find(i)
        root_j = self.find(j)
        if root_i != root_j:
            if self.rank[root_i] < self.rank[root_j]:
                root_i, root_j = root_j, root_i
            self.parent[root_j] = root_i
            if self.rank[root_i] == self.rank[root_j]:
                self.rank[root_i] += 1

    def copy(self) -> "UnionFind":
        """ for undo."""
        new_uf = UnionFind.__new__(UnionFind)
        new_uf.parent = self.parent.copy()
        new_uf.rank = self.rank.copy()
        return new_uf


class Hex(Game):
    def __init__(self, size: int = 11) -> None:
        self.size: int = size
        self.num_cells: int = size * size
        self.board: list[BoardColor]
        self.init_board()
        
        # Virtual edge nodes for Union-Find
        index: int = self.num_cells
        self.TOP = index
        self.BOTTOM = index + 1
        self.LEFT = index + 2
        self.RIGHT = index + 3
        
        self.init_uf()
        super().__init__()

    def init_board(self) -> None:
        self.board = [EMPTY] * self.num_cells

    def init_uf(self) -> None:
        self.uf = UnionFind(self.num_cells + 4)
        self.uf_history: list[UnionFind] = []
    
    def reset_game(self) -> None:
        """Resets the game state, board array, and Union-Find structures."""
        super().reset_game()
        self.init_board()
        self.init_uf()

    # --- Coordinate & Edge Helper Functions ---

    def _coord_to_point(self, row: int, col: int) -> int:
        return row * self.size + col

    def _point_to_coord(self, point: int) -> tuple[int, int]:
        return point // self.size, point % self.size

    def _is_top_edge(self, point: int) -> bool:
        return point // self.size == 0

    def _is_bottom_edge(self, point: int) -> bool:
        return point // self.size == self.size - 1

    def _is_left_edge(self, point: int) -> bool:
        return point % self.size == 0

    def _is_right_edge(self, point: int) -> bool:
        return point % self.size == self.size - 1

    def _get_neighbors(self, point: int) -> list[int]:
        r, c = self._point_to_coord(point)
        neighbors = []
        for dr, dc in HEX_DIRECTIONS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.size and 0 <= nc < self.size:
                neighbors.append(self._coord_to_point(nr, nc))
        return neighbors

    # --- Interface Implementation ---

    def legal_moves(self) -> list[int]:
        """Returns list of empty cell indices on board."""
        if self.end_of_game():
            return []
        return [p for p, c in enumerate(self.board) if c == EMPTY]

    def play(self, move: int) -> bool:
        #print(f"play {move} {self.to_play}")
        assert self.board[move] == EMPTY
        
        # Save state for fast undo
        self.uf_history.append(self.uf.copy())
        
        player = self.to_play
        self.board[move] = player

        # Connect to virtual edge nodes
        if player == BLACK:
            if self._is_top_edge(move):
                self.uf.union(move, self.TOP)
            if self._is_bottom_edge(move):
                self.uf.union(move, self.BOTTOM)
        else:  # WHITE
            if self._is_left_edge(move):
                self.uf.union(move, self.LEFT)
            if self._is_right_edge(move):
                self.uf.union(move, self.RIGHT)

        # Connect to adjacent same-colored stones
        for nb in self._get_neighbors(move):
            if self.board[nb] == player:
                self.uf.union(move, nb)

        super().play(move)
        return True

    def undo_move(self) -> None:
        """Restores board and Union-Find state in O(1) time."""
        last = self.last_move()
        #print(f"undo {last}")
        self.board[last] = EMPTY
        self.uf = self.uf_history.pop()
        super().undo_move()

    def check_win(self, player: Color) -> bool:
        if player == BLACK:
            return self.uf.find(self.TOP) == self.uf.find(self.BOTTOM)
        else:
            return self.uf.find(self.LEFT) == self.uf.find(self.RIGHT)

    def winner(self) -> WinnerColor:
        opp: Color = opponent(self.to_play)
        if self.check_win(opp):
            return opp
#         if self.check_win(WHITE):
#             return WHITE
        return EMPTY

    def end_of_game(self) -> bool:
        return self.winner() != EMPTY

    def boolean_eval(self) -> bool:
        return self.winner() == self.to_play

    def int_eval(self) -> int:
        w = self.winner()
        if w == EMPTY:
            return 0
        return 1 if w == self.to_play else -1

    def __str__(self) -> str:
        """ASCII representation of Hex board."""
        symbols = {EMPTY: ".", BLACK: "B", WHITE: "W", BORDER: "#"}
        lines = []
        for r in range(self.size):
            indent = " " * r
            row_str = " ".join(symbols[self.board[self._coord_to_point(r, c)]] for c in range(self.size))
            lines.append(f"{indent}{row_str}")
        return "\n" + "\n".join(lines)

    def code(self) -> int:
        c = 0
        for i in range(self.num_cells):
            c = 3*c + self.board[i]
        return c


if __name__ == "__main__":
    game = Hex(size=3)
    print("Initial 3x3 Hex Board:\n")
    print(game)

    # Black attempts top-to-bottom connection: (0,1) -> (1,1) -> (2,1)
    moves_sequence = [
        game._coord_to_point(0, 1), # Black (Top edge)
        game._coord_to_point(0, 0), # White
        game._coord_to_point(1, 1), # Black
        game._coord_to_point(1, 0), # White
        game._coord_to_point(2, 1), # Black (Bottom edge - Winning move)
    ]

    for move in moves_sequence:
        game.play(move)

    print("\nBoard state after sequence:\n")
    print(game)
    print("\nEnd of game:", game.end_of_game())
    print("Winner:", WINNER_STR[game.winner()])
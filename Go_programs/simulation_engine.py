from board_base import EMPTY, GO_COLOR, GO_POINT
from board import GoBoard
from engine import GoEngine

class Go3Args:
    def __init__(self, sim: int, move_select: str, sim_rule: str, 
                 check_selfatari: bool, limit: int) -> None:
        self.sim: int = sim
        self.move_select: str = move_select
        self.use_ucb: bool = (move_select != "simple")
        self.sim_rule: str = sim_rule
        self.random_simulation: bool = (sim_rule == "random")
        self.check_selfatari: bool = check_selfatari
        self.use_pattern: bool = not self.random_simulation
        self.limit: int = limit

class GoSimulationEngine(GoEngine):
    def __init__(self, name: str, version: float, 
                 sim: int, move_select: str, sim_rule: str, 
                 check_selfatari: bool, limit: int = 100) -> None:
        """
        Go player that selects moves by simulation.
        """
        GoEngine.__init__(self, name, version)
        self.args: Go3Args = Go3Args(sim, move_select, sim_rule, 
                          check_selfatari, limit)

    def simulate(self, board: GoBoard, move: GO_POINT, toplay: GO_COLOR) -> GO_COLOR:
        """
        Run a simulated game for a given move.
        """
        print("ERROR: must override GoSimulationEngine.simulate in your engine")
        return EMPTY
        
    def simulate_move(self, board: GoBoard, move: GO_POINT, toplay: GO_COLOR) -> int:
        """
        Run self.sim simulations for a given move. Returns number of wins.
        """
        wins = 0
        for _ in range(self.args.sim):
            result = self.simulate(board, move, toplay)
            if result == toplay:
                wins += 1
        return wins

    def reset(self) -> None:
        raise NotImplementedError

    def update(self, move: GO_POINT) -> None:
        raise NotImplementedError

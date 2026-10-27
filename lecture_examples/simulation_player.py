# Cmput 455 sample code
# Player based on statistics of random simulations
# Written by Martin Mueller

from game_basics import EMPTY, BLACK, WHITE
from game import Game
from player import Player

class SimulationPlayer(Player):
    def __init__(self, num_simulations: int) -> None:
        self.num_simulations = num_simulations

    def name(self) -> str:
        return f"Simulation Player ({self.num_simulations} sim.)"

    def genmove(self, state: Game) -> int:
        assert not state.end_of_game()
        moves = state.legal_moves()
        num_moves = len(moves)
        score = [0.0] * num_moves
        for i in range(num_moves):
            move = moves[i]
            score[i] = self.simulate(state, move)
        #print(score)
        best_index = score.index(max(score))
        best = moves[best_index]
        #print("Best move:", best, "score", score[best])
        assert best in state.legal_moves()
        return best

    def simulate(self, state: Game, move: int) -> float:
        stats = [0] * 3
        state.play(move)
        move_nr = state.move_number()
        for _ in range(self.num_simulations):
            winner, _ = state.simulate()
            stats[winner] += 1
            state.reset_to_move_number(move_nr)
        assert sum(stats) == self.num_simulations
        assert move_nr == state.move_number()
        state.undo_move()
        eval = (stats[BLACK] + 0.5 * stats[EMPTY]) / self.num_simulations
        if state.to_play == WHITE:
            eval = 1 - eval
        return eval

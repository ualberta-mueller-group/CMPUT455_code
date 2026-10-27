# Cmput 455 sample code
# UCB algorithm
# Written by Martin Mueller, cleaned up with help from Gemini

from bernoulli import bernoulli_experiment
from math import sqrt, log
from dataclasses import dataclass

INFINITY = float('inf')

@dataclass
class UCBStatistic:
    wins: int = 0
    sims: int = 0
    def mean(self)-> float:
        assert self.sims > 0
        return self.wins / self.sims
        
    def ucb(self, C: float, n: int) -> float:
        if self.sims == 0:
            return INFINITY
        else:
            assert n >= self.sims > 0
            return self.mean() + C * sqrt(log(n) / self.sims)

def stats_as_string(stats: list[UCBStatistic]) -> str:
    return "".join(
        f"  arm {arm}: {s.wins} wins, {s.sims} sims\n"
        for arm, s in enumerate(stats)
    )

def find_best_arm(stats: list[UCBStatistic], C: float, total_sims: int) -> int:
    def get_score(i: int) -> float:
        return stats[i].ucb(C, total_sims)
    return max(range(len(stats)), key = get_score)
    

def most_pulled_arm(stats: list[UCBStatistic]) -> int:
    def get_sims(i: int) -> int:
        return stats[i].sims
    return max(range(len(stats)), key = get_sims)

def simulation_result(p: float) -> int:
    return bernoulli_experiment(p)

def run_ucb(payoffs: list[float], C: float, max_simulations: int) -> None:
    num_arms = len(payoffs)
    stats = [UCBStatistic() for _ in range(num_arms)]
    assert len(stats) == len(payoffs)
    
    for n in range(max_simulations):
        move = find_best_arm(stats, C, n)
        assert 0 <= move < len(payoffs)
        p = payoffs[move]
        stats[move].wins += simulation_result(p) # 0 or 1
        stats[move].sims += 1
    print(
         f"C = {C} Statistics from {max_simulations} simulations:\n"
         f"Payoffs {payoffs}\n"
         f"{stats_as_string(stats)}"
         f"Most pulled arm {most_pulled_arm(stats)}\n"
         )
    return stats

payoffs_twoarm: list[float] = [0.7, 0.5]
# Easy case for UCB: other payoffs well separated from best arm 0.9
payoffs_easy: list[float] = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
# Hard case for UCB: arm 1 and 2 very close, 0.61 vs 0.62. Best arm: 2
payoffs_hard: list[float] = [0.5, 0.61, 0.62, 0.55]

TEST_CASES = {
    "Basic Case (2 arms)": payoffs_twoarm,
    "Easy Case (10 arms)": payoffs_easy,
    "Hard Case (4 arms)": payoffs_hard,
}


for C in [100, 10, sqrt(2), 1, 0.1, 0.01]:
    run_ucb(payoffs_easy, C, max_simulations = 1000)
    run_ucb(payoffs_hard, C, max_simulations = 1000)
    #run_ucb(payoffs_hard, C, max_simulations = 100000)

# Who wins 21 game when both players are random?
# dp[n] holds the win probability for to_play with n tokens
# Each legal move has equal probability
# After each move, to_play is reversed (negamax), hence the 1 - dp

from fractions import Fraction

def compute_exact_fractions(n_tokens=21):
    dp = [Fraction(0)] * (n_tokens + 1)
    for n in range(1, n_tokens + 1):
        valid_moves = [m for m in [1, 2, 3] if m <= n]
        win_sum = sum(1 - dp[n - m] for m in valid_moves)
        dp[n] = win_sum / len(valid_moves)
    return dp
    
results = compute_exact_fractions(21)

for n, f in enumerate(results):
    print(f"n = {n:2d}: {str(f):>20} ≈ {float(f):.8f}")
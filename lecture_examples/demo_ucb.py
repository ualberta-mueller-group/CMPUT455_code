import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons, Button
from math import sqrt

# Import structures directly from ucb.py
from ucb import UCBStatistic, simulation_result, TEST_CASES, run_ucb


# Replace the old slider/button setup and add incremental state tracking:

class UCBDemo:
    def __init__(self):
        plt.style.use('default')
        self.fig = plt.figure(figsize=(12, 8), facecolor='white')
        self.fig.canvas.manager.set_window_title('UCB Multi-Armed Bandit Visualizer')

        self.ax_stats = plt.subplot2grid((3, 3), (0, 0), colspan=2, rowspan=2)
        self.ax_pulls = plt.subplot2grid((3, 3), (2, 0), colspan=2)

        # Persistent state for step-by-step simulations
        self.total_sims = 0
        self.stats = []

        # UI Widget Axes
        self.ax_radio = plt.axes([0.72, 0.70, 0.23, 0.18], facecolor='#f4f4f4')
        self.ax_slider_c = plt.axes([0.72, 0.58, 0.23, 0.03], facecolor='#f4f4f4')
        
        # Incremental Run & Reset Buttons
        self.ax_btn_1 = plt.axes([0.72, 0.46, 0.065, 0.05])
        self.ax_btn_10 = plt.axes([0.80, 0.46, 0.065, 0.05])
        self.ax_btn_100 = plt.axes([0.88, 0.46, 0.07, 0.05])
        self.ax_btn_reset = plt.axes([0.76, 0.36, 0.15, 0.05])

        # Instantiate UI Controls
        self.radio = RadioButtons(self.ax_radio, tuple(TEST_CASES.keys()), active=0, activecolor='#2ca02c')
        self.slider_c = Slider(self.ax_slider_c, 'C', 0.0, 5.0, valinit=sqrt(2), valstep=0.01, color='#4c72b0')
        
        self.btn_1 = Button(self.ax_btn_1, '+1', color='#e0e0e0', hovercolor='#d0d0d0')
        self.btn_10 = Button(self.ax_btn_10, '+10', color='#e0e0e0', hovercolor='#d0d0d0')
        self.btn_100 = Button(self.ax_btn_100, '+100', color='#e0e0e0', hovercolor='#d0d0d0')
        self.btn_reset = Button(self.ax_btn_reset, 'Reset', color='#ffcccc', hovercolor='#ffaaaa')

        # Attach callbacks
        self.radio.on_clicked(self.reset)
        self.slider_c.on_changed(lambda val: self.draw())
        self.btn_1.on_clicked(lambda event: self.step(1))
        self.btn_10.on_clicked(lambda event: self.step(10))
        self.btn_100.on_clicked(lambda event: self.step(100))
        self.btn_reset.on_clicked(self.reset)

        self.reset()

    def reset(self, val=None):
        payoffs = TEST_CASES[self.radio.value_selected]
        self.stats = [UCBStatistic() for _ in range(len(payoffs))]
        self.total_sims = 0
        self.draw()

    def step(self, steps: int):
        payoffs = TEST_CASES[self.radio.value_selected]
        C = self.slider_c.val
        num_arms = len(payoffs)
        
        for _ in range(steps):
            def get_score(i: int) -> float:
                return self.stats[i].ucb(C, self.total_sims)
                
            move = max(range(num_arms), key=get_score)
            p = payoffs[move]
            self.stats[move].wins += simulation_result(p)
            self.stats[move].sims += 1
            self.total_sims += 1
            
        self.draw()

    def draw(self):
        payoffs = TEST_CASES[self.radio.value_selected]
        C = self.slider_c.val
        num_arms = len(payoffs)

        means = [s.mean() if s.sims > 0 else 0.0 for s in self.stats]
        ucbs = [s.ucb(C, self.total_sims) if s.sims > 0 else float('inf') for s in self.stats]
        lcbs = [max(0.0, 2 * m - u) if u != float('inf') else 0.0 for m, u in zip(means, ucbs)]
        pulls = [s.sims for s in self.stats]

        self.ax_stats.clear()
        self.ax_pulls.clear()
        self.ax_stats.set_facecolor('white')
        self.ax_pulls.set_facecolor('white')

        x = np.arange(num_arms)
        bar_width = 0.45

        # 1. True Payoffs
        self.ax_stats.bar(x, payoffs, width=bar_width, color='#a0aec0', edgecolor='#ced4da', label='True Mean $p$')

        # 2. Confidence Interval: Thin Black Bar
        valid_indices = [i for i, u in enumerate(ucbs) if u != float('inf')]
        valid_ucbs = [ucbs[i] for i in valid_indices]

        for idx, i in enumerate(valid_indices):
            self.ax_stats.plot(
                [i, i], [lcbs[i], ucbs[i]], 
                color='black', linewidth=1.5, zorder=3,
                label='Confidence Interval' if idx == 0 else ""
            )

        # 3. Empirical Means
        self.ax_stats.scatter(
            x, means, 
            color='#ff7f0e', edgecolor='black', linewidth=0.8, s=60, zorder=4, 
            label=r'Empirical Mean ($\hat{\mu}$)'
        )

        # 4. Upper End: Green Dot
        self.ax_stats.scatter(
            valid_indices, valid_ucbs, 
            color='#2ca02c', edgecolor='black', linewidth=0.8, s=70, zorder=5, 
            label=r'UCB Upper Bound'
        )

        self.ax_stats.set_title(f'UCB Arm Statistics (C = {C:.2f}, Total Sims = {self.total_sims})', fontsize=12, pad=10)
        self.ax_stats.set_ylabel('Probability / Score')
        self.ax_stats.set_xticks(x)
        self.ax_stats.set_xticklabels([f'Arm {i}' for i in range(num_arms)])
        self.ax_stats.set_ylim(-0.05, max(1.1, max(valid_ucbs, default=1.1) + 0.1))
        self.ax_stats.grid(axis='y', linestyle=':', alpha=0.6)
        self.ax_stats.legend(loc='lower left', 
        bbox_to_anchor=(0.0, 1.02), ncol=4, framealpha=0.9)
        # Bottom Plot: Pull Distribution
        self.ax_pulls.bar(x, pulls, width=bar_width, color='#4c72b0', alpha=0.85)
        self.ax_pulls.set_ylabel('Pull Count')
        self.ax_pulls.set_xlabel('Arm Index')
        self.ax_pulls.set_xticks(x)
        self.ax_pulls.set_xticklabels([f'Arm {i}' for i in range(num_arms)])
        self.ax_pulls.grid(axis='y', linestyle=':', alpha=0.6)

        max_pull = max(pulls) if pulls else 0
        for i, count in enumerate(pulls):
            self.ax_pulls.text(i, count + (max_pull * 0.02), str(count), ha='center', va='bottom', fontsize=9)

        self.fig.canvas.draw_idle()

if __name__ == "__main__":
    app = UCBDemo()
    plt.show()
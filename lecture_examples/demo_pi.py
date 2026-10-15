# Cmput 455 sample code
# Estimate pi with random sampling
# How many random points within the square (0,1) x (0,1)
# are within the quarter circle x>0, y>0, x^2 + y^2 < 1
# Prints estimates after 1, 2, 4, 8, ... samples
# Written by Martin Mueller

import math
import random
import matplotlib.pyplot as plt
import numpy as np
from typing import List

class PiVisualizer:
    def __init__(self) -> None:
        plt.ion()
        self.fig, (self.ax_grid, self.ax_convergence) = plt.subplots(
            1, 2, figsize=(12, 5)
        )

        # Setup Left Subplot: Quarter Circle & Points
        self.ax_grid.set_xlim(0, 1)
        self.ax_grid.set_ylim(0, 1)
        self.ax_grid.set_aspect("equal")
        self.ax_grid.set_title("Monte Carlo $\pi$ Simulation")

        theta = np.linspace(0, np.pi / 2, 100)
        self.ax_grid.plot(
            np.cos(theta), np.sin(theta), color="black", linewidth=2
        )

        (self.scatter_in,) = self.ax_grid.plot(
            [], [], "go", markersize=2, label="In Circle"
        )
        (self.scatter_out,) = self.ax_grid.plot(
            [], [], "ro", markersize=2, label="Outside"
        )
        self.ax_grid.legend(loc="upper right")

        # Setup Right Subplot: Convergence to Pi
        self.ax_convergence.axhline(
            math.pi, color="black", linestyle="--", label="True $\pi$"
        )
        (self.line_est,) = self.ax_convergence.plot(
            [], [], "b-", linewidth=1.5, label="Estimate"
        )
        self.ax_convergence.set_title("$\pi$ Estimate Convergence")
        self.ax_convergence.set_xlabel("Number of Simulations")
        self.ax_convergence.set_ylabel("Estimated $\pi$")
        self.ax_convergence.set_ylim(1.0, 5.0)
        self.ax_convergence.legend(loc="upper right")
        self.ax_convergence.grid(True)

        plt.tight_layout()

        self.x_in: List[float] = []
        self.y_in: List[float] = []
        self.x_out: List[float] = []
        self.y_out: List[float] = []
        self.sim_counts: List[int] = []
        self.pi_estimates: List[float] = []

    def record_sample(self, x: float, y: float, in_circle: bool) -> None:
        if in_circle:
            self.x_in.append(x)
            self.y_in.append(y)
        else:
            self.x_out.append(x)
            self.y_out.append(y)

    def is_open(self) -> bool:
        return plt.fignum_exists(self.fig.number)

    def update(self, num_simulations: int, estimate: float) -> int:
        self.sim_counts.append(num_simulations)
        self.pi_estimates.append(estimate)

        self.scatter_in.set_data(self.x_in, self.y_in)
        self.scatter_out.set_data(self.x_out, self.y_out)
        self.line_est.set_data(self.sim_counts, self.pi_estimates)
        self.ax_convergence.set_xlim(1, max(10, num_simulations))

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

        # Pace control: slow at start, speeds up exponentially later
        if num_simulations <= 15:
            plt.pause(0.25)
            return num_simulations + 1
        elif num_simulations <= 50:
            plt.pause(0.08)
            return num_simulations + 2
        else:
            plt.pause(0.001)
            return int(num_simulations * 1.5) + 1

    def close(self) -> None:
        plt.ioff()
        plt.show()


def print_estimate(num_simulations: int, estimate: float) -> None:
    relative_error = abs(math.pi - estimate) / math.pi
    print(
        f"After {num_simulations} simulations, "
        f"estimate of pi = {estimate}, "
        f"relative error = {relative_error:.2e}"
    )

if __name__ == "__main__":
    random.seed()
    next_print: int = 1
    num_simulations: int = 0
    num_in_circle: int = 0

    ui = PiVisualizer()
    while ui.is_open():
        if num_simulations >= next_print:
            estimate: float = 4 * num_in_circle / num_simulations
            print_estimate(num_simulations, estimate)
            next_print = ui.update(num_simulations, estimate)

        x: float = random.random()
        y: float = random.random()
        in_circle = x * x + y * y < 1
        num_simulations += 1
        if in_circle:
            num_in_circle += 1
        ui.record_sample(x, y, in_circle)

    ui.close()
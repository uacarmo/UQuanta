import numpy as np
import matplotlib.pyplot as plt

from quantum.driven_hamiltonian import DrivenHamiltonian
from quantum.evolution import TimeEvolution


def rabi_experiment(
    omega=2.0 * np.pi,
    delta=0.0,
    num_points=200,
):
    """
    Rabi experiment using Hamiltonian time evolution.

    The qubit starts in |0>.

    Hamiltonian:

        H = (Delta / 2) Z + (Omega / 2) X

    On resonance:

        Delta = 0
    """

    hamiltonian = DrivenHamiltonian(
        omega=omega,
        delta=delta,
    )

    evolution = TimeEvolution(hamiltonian.hamiltonian)

    initial_state = np.array(
        [1.0, 0.0],
        dtype=complex,
    )

    times = np.linspace(
        0.0,
        2.0,
        num_points,
    )

    probabilities = []

    for time in times:
        state = evolution.evolve_state(
            initial_state,
            time,
        )

        probability_1 = abs(state[1]) ** 2

        probabilities.append(probability_1)

    return times, np.array(probabilities)


def main():
    print("--- Rabi Oscillation: Physical Model ---")

    omega = 2.0 * np.pi
    delta = 0.0

    times, probabilities = rabi_experiment(
        omega=omega,
        delta=delta,
    )

    print("\nFirst measurements:")

    for i in range(0, len(times), 20):
        print(
            f"t = {times[i]:.4f}   "
            f"P(|1>) = {probabilities[i]:.6f}"
        )

    plt.figure(figsize=(8, 5))

    plt.plot(
        times,
        probabilities,
        label="Hamiltonian P(|1>)",
    )

    plt.xlabel("Time")
    plt.ylabel("Probability P(|1>)")
    plt.title("Rabi Oscillation - Physical Model")

    plt.ylim(0, 1)

    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
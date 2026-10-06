import numpy as np

from quantum.hamiltonian import Hamiltonian
from quantum.evolution import TimeEvolution


def main():
    print("--- Single Qubit Free Evolution ---")

    omega = 2.0 * np.pi

    hamiltonian = Hamiltonian.single_qubit(omega)

    evolution = TimeEvolution(hamiltonian)

    initial_state = np.array(
        [1.0, 0.0],
        dtype=complex,
    )

    print("\nHamiltonian:")
    print(hamiltonian.matrix)

    print("\nEvolution:")

    times = np.linspace(0.0, 1.0, 6)

    for time in times:
        state = evolution.evolve_state(
            initial_state,
            time,
        )

        probabilities = np.abs(state) ** 2

        print(
            f"t = {time:.2f}   "
            f"P(|0>) = {probabilities[0]:.6f}   "
            f"P(|1>) = {probabilities[1]:.6f}"
        )


if __name__ == "__main__":
    main()
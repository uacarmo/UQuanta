import numpy as np
import matplotlib.pyplot as plt

from quantum.driven_hamiltonian import DrivenHamiltonian
from quantum.evolution import TimeEvolution


def detuned_rabi_experiment(
    omega=2.0 * np.pi,
    delta=np.pi,
    num_points=400,
):
    """
    Detuned Rabi experiment.

    Effective Hamiltonian:

        H = (Delta / 2) Z + (Omega / 2) X

    Parameters:

        Omega = drive strength
        Delta = detuning

    Expected probability:

        P1(t) =
            Omega^2 / (Omega^2 + Delta^2)
            *
            sin^2(
                sqrt(Omega^2 + Delta^2) * t / 2
            )
    """

    hamiltonian = DrivenHamiltonian(
        omega=omega,
        delta=delta,
    )

    evolution = TimeEvolution(
        hamiltonian.hamiltonian
    )

    initial_state = np.array(
        [1.0, 0.0],
        dtype=complex,
    )

    effective_omega = np.sqrt(
        omega**2 + delta**2
    )

    max_probability = (
        omega**2
        / (omega**2 + delta**2)
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

    probabilities = np.array(probabilities)

    theoretical = (
        max_probability
        * np.sin(
            effective_omega * times / 2.0
        ) ** 2
    )

    return (
        times,
        probabilities,
        theoretical,
        effective_omega,
        max_probability,
    )


def main():
    print("--- Detuned Rabi Oscillation ---")

    omega = 2.0 * np.pi
    delta = np.pi

    (
        times,
        probabilities,
        theoretical,
        effective_omega,
        max_probability,
    ) = detuned_rabi_experiment(
        omega=omega,
        delta=delta,
    )

    print("\nParameters:")
    print(f"Drive strength Ω       = {omega:.6f}")
    print(f"Detuning Δ             = {delta:.6f}")
    print(
        f"Effective frequency    = "
        f"{effective_omega:.6f}"
    )
    print(
        f"Expected maximum P1    = "
        f"{max_probability:.6f}"
    )

    print("\nFirst measurements:")

    for i in range(0, len(times), 40):
        print(
            f"t = {times[i]:.4f}   "
            f"P(|1>) = {probabilities[i]:.6f}"
        )

    plt.figure(figsize=(8, 5))

    plt.plot(
        times,
        probabilities,
        label="Simulation",
    )

    plt.plot(
        times,
        theoretical,
        linestyle="--",
        label="Theory",
    )

    plt.xlabel("Time")
    plt.ylabel("Probability P(|1>)")
    plt.title("Detuned Rabi Oscillation")

    plt.ylim(0, 1)

    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
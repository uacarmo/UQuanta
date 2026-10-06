import numpy as np
import matplotlib.pyplot as plt

from quantum import QuantumRegister


def rabi_experiment(num_points=200):
    """
    Reference Rabi experiment.

    The qubit starts in |0>.
    Rx(theta) is used as a reference for coherent driving.

    Expected:
        P(|1>) = sin^2(theta / 2)
    """

    theta_values = np.linspace(0.0, 4.0 * np.pi, num_points)

    probabilities = []

    for theta in theta_values:
        q = QuantumRegister(1)

        q.rx(theta, 0)

        probs = q.probabilities()

        probabilities.append(probs[1])

    return theta_values, np.array(probabilities)


def main():
    print("--- Rabi Oscillation: Reference Experiment ---")

    theta, probability = rabi_experiment()

    print("\nFirst measurements:")

    for i in range(0, len(theta), 20):
        print(
            f"theta = {theta[i]:8.4f}   "
            f"P(|1>) = {probability[i]:.6f}"
        )

    plt.figure(figsize=(8, 5))

    plt.plot(
        theta,
        probability,
        label="Simulated P(|1>)"
    )

    plt.xlabel("Rotation angle θ (rad)")
    plt.ylabel("Probability P(|1>)")
    plt.title("Rabi Oscillation — Reference Model")

    plt.ylim(0, 1)

    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
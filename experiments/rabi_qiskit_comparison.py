import numpy as np

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


# ============================================================
# Rabi Cross-Validation
# Our simulator vs Qiskit Aer
# ============================================================

def our_rabi_probability(theta):
    """
    Reference Rabi probability used by our simulator.

    P(|1>) = sin^2(theta / 2)
    """
    return np.sin(theta / 2) ** 2


def qiskit_rabi_probability(theta, shots=10000):
    """
    Run the equivalent Rabi rotation using Qiskit Aer.

    Rx(theta)|0> produces:

        cos(theta/2)|0> - i sin(theta/2)|1>

    Therefore:

        P(|1>) = sin^2(theta/2)
    """

    qc = QuantumCircuit(1, 1)

    qc.rx(theta, 0)
    qc.measure(0, 0)

    simulator = AerSimulator()

    result = simulator.run(
        qc,
        shots=shots,
        seed_simulator=12345,
    ).result()

    counts = result.get_counts()

    return counts.get("1", 0) / shots


def main():

    print("--- Rabi Cross-Validation: Our Simulator vs Qiskit Aer ---")
    print()

    shots = 10000

    theta_values = np.linspace(
        0,
        4 * np.pi,
        21
    )

    our_values = []
    qiskit_values = []

    for theta in theta_values:

        p_our = our_rabi_probability(theta)

        p_qiskit = qiskit_rabi_probability(
            theta,
            shots=shots
        )

        our_values.append(p_our)
        qiskit_values.append(p_qiskit)

    our_values = np.array(our_values)
    qiskit_values = np.array(qiskit_values)

    differences = np.abs(
        our_values - qiskit_values
    )

    max_difference = np.max(differences)

    rms_difference = np.sqrt(
        np.mean(differences ** 2)
    )

    print("Parameters:")
    print(f"Shots/point = {shots}")
    print()

    print("Comparison:")
    print(
        "theta       "
        "Our P(|1>)   "
        "Qiskit P(|1>)   "
        "Difference"
    )

    print("-" * 60)

    for theta, p_our, p_qiskit, difference in zip(
        theta_values,
        our_values,
        qiskit_values,
        differences
    ):

        print(
            f"{theta:8.4f}   "
            f"{p_our:10.6f}   "
            f"{p_qiskit:13.6f}   "
            f"{difference:10.6f}"
        )

    print()
    print("Validation metrics:")
    print(
        f"Maximum absolute difference = "
        f"{max_difference:.6f}"
    )

    print(
        f"RMS difference              = "
        f"{rms_difference:.6f}"
    )


if __name__ == "__main__":
    main()
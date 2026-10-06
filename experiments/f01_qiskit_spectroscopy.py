import numpy as np

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


# ============================================================
# F01 Spectroscopy using Qiskit Aer
# ============================================================

def qiskit_f01_probability(
    f01,
    f_drive,
    interaction_time=1.0,
    drive_strength=np.pi,
    shots=10000,
):
    """
    Simulate an ideal driven qubit.

    The effective detuning is:

        Delta = f_drive - f01

    The transition probability follows the driven two-level
    system response:

        P1 = (Omega^2 / (Omega^2 + Delta^2))
             * sin^2(
                 0.5 * sqrt(Omega^2 + Delta^2) * t
             )

    Qiskit is used to execute the corresponding Rx rotation.
    """

    detuning = f_drive - f01

    omega_eff = np.sqrt(
        drive_strength**2 + detuning**2
    )

    probability = (
        drive_strength**2
        / omega_eff**2
    ) * np.sin(
        0.5 * omega_eff * interaction_time
    ) ** 2

    # Convert probability into a rotation angle.
    theta = 2 * np.arcsin(
        np.sqrt(
            np.clip(probability, 0.0, 1.0)
        )
    )

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


def run_spectroscopy():

    f01 = 5.0

    interaction_time = 1.0
    drive_strength = np.pi
    shots = 10000

    frequencies = np.linspace(
        4.0,
        6.0,
        21,
    )

    probabilities = []

    for f_drive in frequencies:

        probability = qiskit_f01_probability(
            f01=f01,
            f_drive=f_drive,
            interaction_time=interaction_time,
            drive_strength=drive_strength,
            shots=shots,
        )

        probabilities.append(probability)

    probabilities = np.array(probabilities)

    index = np.argmax(probabilities)

    measured_resonance = frequencies[index]
    maximum_probability = probabilities[index]

    return (
        frequencies,
        probabilities,
        measured_resonance,
        maximum_probability,
    )


def main():

    print("--- F01 Spectroscopy: Qiskit Aer ---")
    print()

    frequencies, probabilities, resonance, maximum = (
        run_spectroscopy()
    )

    print("Parameters:")
    print("True f01              = 5.000000")
    print("Interaction time      = 1.000000")
    print(f"Shots/point           = 10000")
    print()

    print("Measured resonance:")
    print(
        f"frequency             = {resonance:.6f}"
    )
    print(
        f"Maximum P(|1>)        = {maximum:.6f}"
    )
    print()

    print("Measurements:")

    for frequency, probability in zip(
        frequencies,
        probabilities,
    ):

        print(
            f"f_drive = {frequency:.3f}   "
            f"P(|1>) = {probability:.6f}"
        )


if __name__ == "__main__":
    main()
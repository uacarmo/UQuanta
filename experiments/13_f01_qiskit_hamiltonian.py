import numpy as np

from qiskit import QuantumCircuit
from qiskit.circuit.library import UnitaryGate
from qiskit_aer import AerSimulator


# ============================================================
# F01 Spectroscopy using Qiskit Aer
# Hamiltonian -> matrix exponential -> unitary -> measurement
# ============================================================

def matrix_exponential_hermitian(H, time):
    """
    Calculate:

        U(t) = exp(-i H t)

    using eigendecomposition of the Hermitian Hamiltonian.
    """

    eigenvalues, eigenvectors = np.linalg.eigh(H)

    phases = np.exp(
        -1j * eigenvalues * time
    )

    return (
        eigenvectors
        @ np.diag(phases)
        @ eigenvectors.conj().T
    )


def qiskit_f01_probability(
    f01,
    f_drive,
    interaction_time=1.0,
    drive_strength=np.pi,
    shots=10000,
):
    """
    Simulate F01 spectroscopy using a driven
    two-level Hamiltonian.

    Hamiltonian:

        H = 1/2 * (Delta Z + Omega X)

    where:

        Delta = 2*pi*(f_drive - f01)

        Omega = drive strength
    """

    # --------------------------------------------------------
    # Pauli matrices
    # --------------------------------------------------------

    X = np.array([
        [0, 1],
        [1, 0],
    ], dtype=complex)

    Z = np.array([
        [1, 0],
        [0, -1],
    ], dtype=complex)

    # --------------------------------------------------------
    # Detuning
    # --------------------------------------------------------

    detuning = (
        2 * np.pi * (f_drive - f01)
    )

    # --------------------------------------------------------
    # Driven Hamiltonian
    # --------------------------------------------------------

    H = 0.5 * (
        detuning * Z
        + drive_strength * X
    )

    # --------------------------------------------------------
    # Hamiltonian evolution
    #
    # U = exp(-i H t)
    # --------------------------------------------------------

    U = matrix_exponential_hermitian(
        H,
        interaction_time,
    )

    # --------------------------------------------------------
    # Qiskit circuit
    # --------------------------------------------------------

    qc = QuantumCircuit(1, 1)

    unitary_gate = UnitaryGate(
        U,
        label="U(H,t)",
    )

    qc.append(
        unitary_gate,
        [0],
    )

    qc.measure(
        0,
        0,
    )

    # --------------------------------------------------------
    # Aer simulation
    # --------------------------------------------------------

    simulator = AerSimulator()

    result = simulator.run(
        qc,
        shots=shots,
        seed_simulator=12345,
    ).result()

    counts = result.get_counts()

    return counts.get("1", 0) / shots


# ============================================================
# Spectroscopy sweep
# ============================================================

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

        probabilities.append(
            probability
        )

    probabilities = np.array(
        probabilities
    )

    index = np.argmax(
        probabilities
    )

    measured_resonance = (
        frequencies[index]
    )

    maximum_probability = (
        probabilities[index]
    )

    return (
        frequencies,
        probabilities,
        measured_resonance,
        maximum_probability,
    )


# ============================================================
# Main
# ============================================================

def main():

    print(
        "--- F01 Spectroscopy: "
        "Qiskit Aer Hamiltonian Evolution ---"
    )
    print()

    (
        frequencies,
        probabilities,
        resonance,
        maximum,
    ) = run_spectroscopy()

    print("Parameters:")
    print("True f01              = 5.000000")
    print("Interaction time      = 1.000000")
    print("Drive strength Omega  = pi")
    print("Shots/point           = 10000")
    print()

    print("Measured resonance:")

    print(
        f"frequency             = "
        f"{resonance:.6f}"
    )

    print(
        f"Maximum P(|1>)        = "
        f"{maximum:.6f}"
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
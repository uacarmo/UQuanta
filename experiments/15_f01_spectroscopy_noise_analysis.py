import numpy as np
import matplotlib.pyplot as plt

from quantum.evolution import TimeEvolution


# ============================================================
# Parameters
# ============================================================

F01 = 5.0

FREQUENCIES = np.arange(
    2.0,
    10.01,
    0.05,
)

OMEGA = np.pi
INTERACTION_TIME = 1.0


# ============================================================
# Pauli matrices
# ============================================================

X = np.array(
    [
        [0, 1],
        [1, 0],
    ],
    dtype=complex,
)

Z = np.array(
    [
        [1, 0],
        [0, -1],
    ],
    dtype=complex,
)


# ============================================================
# Initial state
# ============================================================

GROUND_STATE = np.array(
    [1.0, 0.0],
    dtype=complex,
)


# ============================================================
# Analytical ideal F01 probability
# ============================================================

def ideal_f01_probability(
    f_drive,
):
    """
    Ideal driven two-level-system probability.

    P1 = Omega^2 / Omega_eff^2 *
         sin^2(Omega_eff * t / 2)
    """

    delta = (
        2.0
        * np.pi
        * (f_drive - F01)
    )

    omega_eff = np.sqrt(
        OMEGA**2 + delta**2
    )

    return (
        OMEGA**2
        / omega_eff**2
        * np.sin(
            omega_eff
            * INTERACTION_TIME
            / 2.0
        ) ** 2
    )


# ============================================================
# Driven Hamiltonian
# ============================================================

class Hamiltonian:
    """
    Minimal Hamiltonian container compatible
    with TimeEvolution.
    """

    def __init__(self, matrix):
        self.matrix = matrix


# ============================================================
# Ideal F01 spectrum
# ============================================================

def calculate_ideal_spectrum():

    probabilities = []

    for f_drive in FREQUENCIES:

        delta = (
            2.0
            * np.pi
            * (f_drive - F01)
        )

        H_matrix = (
            0.5
            * (
                delta * Z
                + OMEGA * X
            )
        )

        H = Hamiltonian(H_matrix)

        evolution = TimeEvolution(H)

        final_state = evolution.evolve_state(
            GROUND_STATE,
            INTERACTION_TIME,
        )

        p1 = abs(final_state[1]) ** 2

        probabilities.append(p1)

    return np.array(probabilities)


# ============================================================
# Decoherence model
# ============================================================

def apply_decoherence(
    p1,
    T1,
    T2,
):
    """
    Approximate decoherence correction for the
    measured excited-state population.

    Energy relaxation:
        excited-state population decays with T1.

    Dephasing:
        coherent excitation is reduced according
        to T2.

    This function is intentionally separated from
    the core unitary simulator so that this experiment
    can be evaluated independently.
    """

    if np.isinf(T1):
        relaxation_factor = 1.0

    else:
        relaxation_factor = np.exp(
            -INTERACTION_TIME / T1
        )

    if np.isinf(T2):
        coherence_factor = 1.0

    else:
        coherence_factor = np.exp(
            -INTERACTION_TIME / T2
        )

    # Preserve the physical ground-state baseline
    # while reducing the coherent excitation.
    effective_probability = (
        p1
        * relaxation_factor
        * coherence_factor
    )

    return effective_probability


# ============================================================
# Spectrum calculation
# ============================================================

def calculate_spectrum(
    T1,
    T2,
):

    ideal = calculate_ideal_spectrum()

    probabilities = np.array(
        [
            apply_decoherence(
                p,
                T1,
                T2,
            )
            for p in ideal
        ]
    )

    return probabilities


# ============================================================
# Resonance detection
# ============================================================

def find_resonance(
    probabilities,
):

    index = np.argmax(
        probabilities
    )

    return (
        FREQUENCIES[index],
        probabilities[index],
    )


# ============================================================
# FWHM calculation
# ============================================================

def calculate_fwhm(
    probabilities,
):

    maximum = np.max(
        probabilities
    )

    half_max = maximum / 2.0

    above = (
        probabilities
        >= half_max
    )

    indices = np.where(
        above
    )[0]

    if len(indices) < 2:
        return np.nan

    left_index = indices[0]
    right_index = indices[-1]

    return (
        FREQUENCIES[right_index]
        - FREQUENCIES[left_index]
    )


# ============================================================
# Main experiment
# ============================================================

def main():

    cases = {
        "Ideal": (
            np.inf,
            np.inf,
        ),
        "T1 only": (
            5.0,
            np.inf,
        ),
        "T2 only": (
            np.inf,
            3.0,
        ),
        "T1 + T2": (
            5.0,
            3.0,
        ),
    }

    spectra = {}

    print("=" * 78)
    print("           EXPERIMENT 15 - F01 SPECTROSCOPY")
    print("                 NOISE ANALYSIS")
    print("=" * 78)

    print()

    print(f"F01                 = {F01:.6f}")
    print(f"Omega               = {OMEGA:.6f} rad/time")
    print(
        f"Interaction time    = "
        f"{INTERACTION_TIME:.6f}"
    )

    print(
        f"Frequency range     = "
        f"{FREQUENCIES[0]:.2f} -> "
        f"{FREQUENCIES[-1]:.2f}"
    )

    print(
        f"Frequency step      = "
        f"{FREQUENCIES[1] - FREQUENCIES[0]:.2f}"
    )

    print()

    # --------------------------------------------------------
    # Calculate spectra
    # --------------------------------------------------------

    for name, (
        T1,
        T2,
    ) in cases.items():

        probabilities = calculate_spectrum(
            T1,
            T2,
        )

        spectra[name] = probabilities

    # --------------------------------------------------------
    # Results table
    # --------------------------------------------------------

    print("-" * 78)

    print(
        f"{'Case':<15}"
        f"{'T1':>10}"
        f"{'T2':>10}"
        f"{'Resonance':>14}"
        f"{'Max P1':>14}"
        f"{'FWHM':>12}"
    )

    print("-" * 78)

    for name, (
        T1,
        T2,
    ) in cases.items():

        probabilities = spectra[name]

        resonance, maximum = find_resonance(
            probabilities
        )

        fwhm = calculate_fwhm(
            probabilities
        )

        T1_text = (
            "inf"
            if np.isinf(T1)
            else f"{T1:.3f}"
        )

        T2_text = (
            "inf"
            if np.isinf(T2)
            else f"{T2:.3f}"
        )

        fwhm_text = (
            "undefined"
            if np.isnan(fwhm)
            else f"{fwhm:.3f}"
        )

        print(
            f"{name:<15}"
            f"{T1_text:>10}"
            f"{T2_text:>10}"
            f"{resonance:>14.6f}"
            f"{maximum:>14.6f}"
            f"{fwhm_text:>12}"
        )

    print("-" * 78)

    print()

    # --------------------------------------------------------
    # Detailed spectrum
    # --------------------------------------------------------

    print("Detailed spectrum:")
    print()

    print(
        f"{'Frequency':>12}"
        f"{'Ideal':>12}"
        f"{'T1 only':>12}"
        f"{'T2 only':>12}"
        f"{'T1 + T2':>12}"
    )

    print("-" * 60)

    for i, frequency in enumerate(
        FREQUENCIES
    ):

        print(
            f"{frequency:12.2f}"
            f"{spectra['Ideal'][i]:12.6f}"
            f"{spectra['T1 only'][i]:12.6f}"
            f"{spectra['T2 only'][i]:12.6f}"
            f"{spectra['T1 + T2'][i]:12.6f}"
        )

    # ========================================================
    # Plot
    # ========================================================

    plt.figure(
        figsize=(10, 6)
    )

    for name, probabilities in spectra.items():

        plt.plot(
            FREQUENCIES,
            probabilities,
            marker="o",
            markersize=3,
            label=name,
        )

    plt.axvline(
        F01,
        linestyle="--",
        label="True F01",
    )

    plt.xlabel(
        "Drive frequency"
    )

    plt.ylabel(
        "P(|1>)"
    )

    plt.title(
        "F01 Spectroscopy under Decoherence"
    )

    plt.grid(True)

    plt.legend()

    plt.tight_layout()

    plt.show()


if __name__ == "__main__":
    main()
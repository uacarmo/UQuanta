import numpy as np
import matplotlib.pyplot as plt


# ============================================================================
# EXPERIMENT 16 - PHYSICAL DENSITY-MATRIX F01 SPECTROSCOPY
#
# Driven two-level system with Lindblad T1 relaxation and pure dephasing.
#
# The density matrix evolves according to:
#
#   d rho / dt = -i [H, rho]
#                + D_T1(rho)
#                + D_phi(rho)
#
# where:
#
#   H = 1/2 (Delta Z + Omega X)
#
#   L1   = sqrt(1/T1) sigma_-
#   Lphi = sqrt(1/(2*Tphi)) Z
#
# and:
#
#   1/T2 = 1/(2*T1) + 1/Tphi
#
# This experiment intentionally does NOT modify any existing simulator code.
# ============================================================================


# ----------------------------------------------------------------------------
# Physical / experimental parameters
# ----------------------------------------------------------------------------

F01 = 5.0

OMEGA = np.pi

INTERACTION_TIME = 1.0

FREQUENCIES = np.arange(2.0, 10.01, 0.05)

# Numerical evolution is performed directly through the Liouvillian.
# No scipy dependency is required.


# ----------------------------------------------------------------------------
# Pauli matrices
# ----------------------------------------------------------------------------

I = np.eye(2, dtype=complex)

X = np.array(
    [
        [0, 1],
        [1, 0],
    ],
    dtype=complex,
)

Y = np.array(
    [
        [0, -1j],
        [1j, 0],
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

SIGMA_MINUS = np.array(
    [
        [0, 1],
        [0, 0],
    ],
    dtype=complex,
)


# ----------------------------------------------------------------------------
# Matrix exponential for small complex matrices
# ----------------------------------------------------------------------------

def matrix_exponential(A):
    """
    Compute exp(A) using eigendecomposition.

    This is sufficient for the 4x4 Liouvillian used in the
    single-qubit density-matrix simulation.
    """
    eigenvalues, eigenvectors = np.linalg.eig(A)

    inverse = np.linalg.inv(eigenvectors)

    return (
        eigenvectors
        @ np.diag(np.exp(eigenvalues))
        @ inverse
    )


# ----------------------------------------------------------------------------
# Vectorization helpers
# ----------------------------------------------------------------------------

def vectorize(rho):
    """
    Column-major vectorization:

        rho -> vec(rho)

    """
    return rho.reshape(-1, order="F")


def devectorize(vector):
    """
    Inverse of vectorize().
    """
    return vector.reshape((2, 2), order="F")


# ----------------------------------------------------------------------------
# Lindblad dissipator
# ----------------------------------------------------------------------------

def lindblad_superoperator(L):
    """
    Construct the Liouville-space superoperator:

        D[rho] =
            L rho L†
            - 1/2 {L†L, rho}

    Using column-major vectorization.
    """

    L_dagger_L = L.conj().T @ L

    jump = np.kron(L.conj(), L)

    left = np.kron(I, L_dagger_L)

    right = np.kron(L_dagger_L.T, I)

    return jump - 0.5 * (left + right)


# ----------------------------------------------------------------------------
# T1 / T2 rates
# ----------------------------------------------------------------------------

def relaxation_rate(T1):
    if np.isinf(T1):
        return 0.0

    return 1.0 / T1


def pure_dephasing_rate(T1, T2):
    """
    Calculate gamma_phi from:

        1/T2 = 1/(2*T1) + 1/Tphi

    Therefore:

        gamma_phi = 1/Tphi
                   = 1/T2 - 1/(2*T1)
    """

    if np.isinf(T2):
        return 0.0

    gamma_phi = 1.0 / T2

    if not np.isinf(T1):
        gamma_phi -= 1.0 / (2.0 * T1)

    if gamma_phi < -1e-12:
        raise ValueError(
            "Invalid T1/T2 combination: "
            "T2 must satisfy T2 <= 2*T1."
        )

    return max(0.0, gamma_phi)


# ----------------------------------------------------------------------------
# Hamiltonian
# ----------------------------------------------------------------------------

def driven_hamiltonian(f_drive):
    """
    Construct the rotating-frame driven Hamiltonian:

        H = 1/2 (Delta Z + Omega X)

    Detuning is angular frequency:

        Delta = 2*pi*(f_drive - F01)
    """

    delta = 2.0 * np.pi * (f_drive - F01)

    return 0.5 * (
        delta * Z
        + OMEGA * X
    )


# ----------------------------------------------------------------------------
# Liouvillian
# ----------------------------------------------------------------------------

def build_liouvillian(f_drive, T1=np.inf, T2=np.inf):
    """
    Construct the complete Liouvillian:

        L = L_unitary + L_T1 + L_phi
    """

    H = driven_hamiltonian(f_drive)

    # ------------------------------------------------------------------------
    # Unitary part
    #
    # vec(-i[H,rho])
    # =
    # -i (I kron H - H^T kron I) vec(rho)
    # ------------------------------------------------------------------------

    L_unitary = -1j * (
        np.kron(I, H)
        - np.kron(H.T, I)
    )

    # ------------------------------------------------------------------------
    # T1 relaxation
    # ------------------------------------------------------------------------

    gamma_1 = relaxation_rate(T1)

    if gamma_1 > 0.0:
        L1 = np.sqrt(gamma_1) * SIGMA_MINUS
        L_T1 = lindblad_superoperator(L1)
    else:
        L_T1 = np.zeros((4, 4), dtype=complex)

    # ------------------------------------------------------------------------
    # Pure dephasing
    # ------------------------------------------------------------------------

    gamma_phi = pure_dephasing_rate(T1, T2)

    if gamma_phi > 0.0:
        Lphi = np.sqrt(gamma_phi / 2.0) * Z
        L_phi = lindblad_superoperator(Lphi)
    else:
        L_phi = np.zeros((4, 4), dtype=complex)

    return L_unitary + L_T1 + L_phi


# ----------------------------------------------------------------------------
# Density-matrix evolution
# ----------------------------------------------------------------------------

def evolve_density_matrix(
    f_drive,
    interaction_time=INTERACTION_TIME,
    T1=np.inf,
    T2=np.inf,
):
    """
    Evolve the initial |0><0| state under the complete
    driven Lindblad dynamics.
    """

    rho0 = np.array(
        [
            [1, 0],
            [0, 0],
        ],
        dtype=complex,
    )

    liouvillian = build_liouvillian(
        f_drive,
        T1=T1,
        T2=T2,
    )

    propagator = matrix_exponential(
        liouvillian * interaction_time
    )

    rho_final = devectorize(
        propagator @ vectorize(rho0)
    )

    # Remove tiny numerical asymmetry.
    rho_final = 0.5 * (
        rho_final + rho_final.conj().T
    )

    return rho_final


# ----------------------------------------------------------------------------
# Measurement probability
# ----------------------------------------------------------------------------

def probability_one(
    f_drive,
    interaction_time=INTERACTION_TIME,
    T1=np.inf,
    T2=np.inf,
):
    rho = evolve_density_matrix(
        f_drive,
        interaction_time=interaction_time,
        T1=T1,
        T2=T2,
    )

    probability = np.real(rho[1, 1])

    # Protect against tiny floating-point excursions.
    return float(np.clip(probability, 0.0, 1.0))


# ----------------------------------------------------------------------------
# Spectrum
# ----------------------------------------------------------------------------

def calculate_spectrum(T1=np.inf, T2=np.inf):

    probabilities = np.array(
        [
            probability_one(
                frequency,
                T1=T1,
                T2=T2,
            )
            for frequency in FREQUENCIES
        ]
    )

    return probabilities


# ----------------------------------------------------------------------------
# Spectrum analysis
# ----------------------------------------------------------------------------

def calculate_resonance(probabilities):

    index = np.argmax(probabilities)

    return FREQUENCIES[index]


def calculate_fwhm(probabilities):

    maximum = np.max(probabilities)

    half_max = maximum / 2.0

    above = probabilities >= half_max

    indices = np.where(above)[0]

    if len(indices) < 2:
        return np.nan

    return (
        FREQUENCIES[indices[-1]]
        - FREQUENCIES[indices[0]]
    )


# ----------------------------------------------------------------------------
# Physical consistency checks
# ----------------------------------------------------------------------------

def check_density_matrix(rho):

    hermitian_error = np.max(
        np.abs(rho - rho.conj().T)
    )

    trace_error = abs(
        np.trace(rho) - 1.0
    )

    eigenvalues = np.linalg.eigvalsh(rho)

    minimum_eigenvalue = np.min(eigenvalues)

    return (
        hermitian_error,
        trace_error,
        minimum_eigenvalue,
    )


# ----------------------------------------------------------------------------
# Run one case
# ----------------------------------------------------------------------------

def run_case(name, T1, T2):

    probabilities = calculate_spectrum(
        T1=T1,
        T2=T2,
    )

    resonance = calculate_resonance(
        probabilities
    )

    maximum = np.max(probabilities)

    fwhm = calculate_fwhm(
        probabilities
    )

    rho_resonance = evolve_density_matrix(
        resonance,
        T1=T1,
        T2=T2,
    )

    (
        hermitian_error,
        trace_error,
        minimum_eigenvalue,
    ) = check_density_matrix(
        rho_resonance
    )

    return {
        "name": name,
        "T1": T1,
        "T2": T2,
        "probabilities": probabilities,
        "resonance": resonance,
        "maximum": maximum,
        "fwhm": fwhm,
        "rho": rho_resonance,
        "hermitian_error": hermitian_error,
        "trace_error": trace_error,
        "minimum_eigenvalue": minimum_eigenvalue,
    }


# ----------------------------------------------------------------------------
# Main experiment
# ----------------------------------------------------------------------------

def main():

    print("=" * 78)
    print("       EXPERIMENT 16 - F01 SPECTROSCOPY")
    print("       PHYSICAL DENSITY-MATRIX / LINDBLAD MODEL")
    print("=" * 78)

    print()
    print(f"F01                 = {F01:.6f}")
    print(f"Omega               = {OMEGA:.6f} rad/time")
    print(f"Interaction time    = {INTERACTION_TIME:.6f}")
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
    print("-" * 78)
    print(
        f"{'Case':<18}"
        f"{'T1':>10}"
        f"{'T2':>10}"
        f"{'Resonance':>14}"
        f"{'Max P1':>14}"
        f"{'FWHM':>12}"
    )
    print("-" * 78)

    cases = [
        ("Ideal", np.inf, np.inf),
        ("T1 only", 5.0, np.inf),
        ("T2 only", np.inf, 3.0),
        ("T1 + T2", 5.0, 3.0),
    ]

    results = []

    for name, T1, T2 in cases:

        result = run_case(
            name,
            T1,
            T2,
        )

        results.append(result)

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

        print(
            f"{name:<18}"
            f"{T1_text:>10}"
            f"{T2_text:>10}"
            f"{result['resonance']:>14.6f}"
            f"{result['maximum']:>14.6f}"
            f"{result['fwhm']:>12.3f}"
        )

    # ------------------------------------------------------------------------
    # Detailed density-matrix validation
    # ------------------------------------------------------------------------

    print()
    print("-" * 78)
    print("Density-matrix physical validation at resonance")
    print("-" * 78)

    for result in results:

        print()
        print(result["name"])

        print(
            "rho ="
        )

        print(
            np.array2string(
                result["rho"],
                precision=6,
                suppress_small=True,
            )
        )

        print(
            f"Hermiticity error   = "
            f"{result['hermitian_error']:.3e}"
        )

        print(
            f"Trace error         = "
            f"{result['trace_error']:.3e}"
        )

        print(
            f"Minimum eigenvalue  = "
            f"{result['minimum_eigenvalue']:.3e}"
        )

    # ------------------------------------------------------------------------
    # Selected spectral points
    # ------------------------------------------------------------------------

    selected_frequencies = [
        2.0,
        3.0,
        4.0,
        4.4,
        4.6,
        4.8,
        4.9,
        5.0,
        5.1,
        5.2,
        5.4,
        6.0,
        7.0,
        8.0,
        9.0,
        10.0,
    ]

    print()
    print("-" * 78)
    print("Selected spectrum")
    print("-" * 78)

    print()
    print(
        f"{'Frequency':>12}"
        f"{'Ideal':>14}"
        f"{'T1 only':>14}"
        f"{'T2 only':>14}"
        f"{'T1 + T2':>14}"
    )

    print("-" * 68)

    for frequency in selected_frequencies:

        index = np.argmin(
            np.abs(FREQUENCIES - frequency)
        )

        print(
            f"{FREQUENCIES[index]:>12.2f}"
            f"{results[0]['probabilities'][index]:>14.6f}"
            f"{results[1]['probabilities'][index]:>14.6f}"
            f"{results[2]['probabilities'][index]:>14.6f}"
            f"{results[3]['probabilities'][index]:>14.6f}"
        )

    # ------------------------------------------------------------------------
    # Plot
    # ------------------------------------------------------------------------

    plt.figure(figsize=(11, 6))

    for result in results:

        plt.plot(
            FREQUENCIES,
            result["probabilities"],
            label=result["name"],
        )

    plt.axvline(
        F01,
        linestyle="--",
        label="True F01",
    )

    plt.xlabel("Drive Frequency")
    plt.ylabel("P(|1>)")
    plt.title(
        "Experiment 16 - Physical Density-Matrix F01 Spectroscopy"
    )

    plt.grid(True, alpha=0.3)
    plt.legend()

    plt.tight_layout()

    plt.show()


if __name__ == "__main__":
    main()
import numpy as np

from .gates import I, X, Y, Z


# ============================================================
# Noise models
# ============================================================

def amplitude_damping_kraus(gamma):
    """
    Amplitude damping.

    Represents energy relaxation:

        |1> -> |0>

    gamma:
        Relaxation probability.
    """

    if not 0 <= gamma <= 1:
        raise ValueError(
            "gamma must be between 0 and 1."
        )

    K0 = np.array([
        [1, 0],
        [0, np.sqrt(1 - gamma)]
    ], dtype=complex)

    K1 = np.array([
        [0, np.sqrt(gamma)],
        [0, 0]
    ], dtype=complex)

    return [K0, K1]


def phase_damping_kraus(gamma):
    """
    Phase damping / dephasing.

    This reduces quantum coherence without directly
    changing the computational-basis populations.
    """

    if not 0 <= gamma <= 1:
        raise ValueError(
            "gamma must be between 0 and 1."
        )

    K0 = np.sqrt(1 - gamma) * I

    K1 = np.sqrt(gamma) * np.array([
        [1, 0],
        [0, 0]
    ], dtype=complex)

    K2 = np.sqrt(gamma) * np.array([
        [0, 0],
        [0, 1]
    ], dtype=complex)

    return [K0, K1, K2]


def depolarizing_kraus(probability):
    """
    Single-qubit depolarizing channel.
    """

    p = probability

    if not 0 <= p <= 1:
        raise ValueError(
            "probability must be between 0 and 1."
        )

    K0 = np.sqrt(1 - p) * I
    K1 = np.sqrt(p / 3) * X
    K2 = np.sqrt(p / 3) * Y
    K3 = np.sqrt(p / 3) * Z

    return [K0, K1, K2, K3]


def thermal_relaxation_parameters(dt, T1, T2):
    """
    Calculate approximate relaxation and pure-dephasing
    probabilities for a time interval dt.

    Returns:

        gamma1
        gamma_phi
    """

    if T1 <= 0 or T2 <= 0:
        raise ValueError(
            "T1 and T2 must be positive."
        )

    if dt < 0:
        raise ValueError(
            "dt must be non-negative."
        )

    gamma1 = 1 - np.exp(-dt / T1)

    # 1/T2 = 1/(2T1) + 1/Tphi

    inv_Tphi = (
        1 / T2 -
        1 / (2 * T1)
    )

    if inv_Tphi > 0:

        Tphi = 1 / inv_Tphi

        gamma_phi = 1 - np.exp(
            -dt / Tphi
        )

    else:

        gamma_phi = 0.0

    return gamma1, gamma_phi
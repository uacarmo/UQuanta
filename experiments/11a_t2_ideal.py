import numpy as np

from quantum.noise import phase_damping_kraus


# ============================================================
# Experiment 11A
# Ideal T2 Characterization
# ============================================================


def apply_kraus_channel(rho, kraus_operators):
    """
    Apply a quantum channel:

        rho' = sum_k K_k rho K_k†
    """

    result = np.zeros_like(
        rho,
        dtype=complex,
    )

    for K in kraus_operators:
        result += (
            K @ rho @ K.conj().T
        )

    return result


def main():

    print("--- T2 Coherence Decay ---")
    print()

    # --------------------------------------------------------
    # Parameters
    # --------------------------------------------------------

    true_t2 = 3.0

    print("Parameters:")
    print(
        f"True T2              = "
        f"{true_t2:.6f}"
    )

    print()

    # --------------------------------------------------------
    # Initial |+> state
    # --------------------------------------------------------

    plus_state = (
        1 / np.sqrt(2)
        * np.array(
            [1, 1],
            dtype=complex,
        )
    )

    rho = np.outer(
        plus_state,
        plus_state.conj(),
    )

    # --------------------------------------------------------
    # Evolution times
    # --------------------------------------------------------

    times = np.linspace(
        0.0,
        12.0,
        25,
    )

    print("Measurements:")
    print()

    coherences = []

    for t in times:

        gamma = (
            1
            - np.exp(
                -t / true_t2
            )
        )

        kraus = phase_damping_kraus(
            gamma
        )

        rho_t = apply_kraus_channel(
            rho,
            kraus,
        )

        coherence = abs(
            rho_t[0, 1]
        )

        normalized_coherence = (
            coherence
            / abs(rho[0, 1])
        )

        coherences.append(
            normalized_coherence
        )

        print(
            f"t = {t:6.3f}   "
            f"C(t) = "
            f"{normalized_coherence:.6f}"
        )

    # --------------------------------------------------------
    # Estimate T2
    #
    # C(t) = exp(-t/T2)
    #
    # ln(C) = -t/T2
    # --------------------------------------------------------

    times_fit = np.asarray(
        times[1:],
        dtype=float,
    )

    coherence_fit = np.asarray(
        coherences[1:],
        dtype=float,
    )

    log_coherence = np.log(
        coherence_fit
    )

    slope, intercept = np.polyfit(
        times_fit,
        log_coherence,
        1,
    )

    estimated_t2 = -1.0 / slope

    print()
    print("Exponential fit:")
    print(
        f"slope     = "
        f"{slope:.6f}"
    )

    print(
        f"intercept = "
        f"{intercept:.6f}"
    )

    print()

    print("T2 estimation:")
    print(
        f"True T2      = "
        f"{true_t2:.6f}"
    )

    print(
        f"Estimated T2 = "
        f"{estimated_t2:.6f}"
    )

    relative_error = (
        abs(
            estimated_t2
            - true_t2
        )
        / true_t2
        * 100.0
    )

    print()
    print("Relative error:")
    print(
        f"{relative_error:.6f} %"
    )


if __name__ == "__main__":
    main()
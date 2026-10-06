import numpy as np


# ============================================================
# Experiment 10
# T1 Relaxation Measurement
# ============================================================

def theoretical_t1_decay(times, T1):
    """
    Ideal T1 relaxation:

        P(|1>, t) = exp(-t / T1)
    """

    return np.exp(-times / T1)


def estimate_t1(times, probabilities):
    """
    Estimate T1 from:

        ln(P1) = -t/T1

    A linear fit gives:

        slope = -1/T1
    """

    times = np.asarray(times, dtype=float)
    probabilities = np.asarray(
        probabilities,
        dtype=float,
    )

    # Avoid log(0)
    valid = probabilities > 0

    times = times[valid]
    probabilities = probabilities[valid]

    log_probability = np.log(probabilities)

    slope, intercept = np.polyfit(
        times,
        log_probability,
        1,
    )

    estimated_t1 = -1.0 / slope

    return estimated_t1, slope, intercept


def main():

    print("--- T1 Relaxation Measurement ---")
    print()

    # --------------------------------------------------------
    # Known simulator parameter
    # --------------------------------------------------------

    true_t1 = 5.0

    print("True T1:")
    print(f"{true_t1:.6f}")
    print()

    # --------------------------------------------------------
    # Measurement times
    # --------------------------------------------------------

    times = np.linspace(
        0.0,
        15.0,
        31,
    )

    # --------------------------------------------------------
    # Generate ideal measurements
    # --------------------------------------------------------

    probabilities = theoretical_t1_decay(
        times,
        true_t1,
    )

    # --------------------------------------------------------
    # Estimate T1 from measurements
    # --------------------------------------------------------

    estimated_t1, slope, intercept = (
        estimate_t1(
            times,
            probabilities,
        )
    )

    # --------------------------------------------------------
    # Error
    # --------------------------------------------------------

    error = (
        abs(estimated_t1 - true_t1)
        / true_t1
        * 100.0
    )

    # --------------------------------------------------------
    # Results
    # --------------------------------------------------------

    print("Measurements:")
    print()

    for t, p in zip(times, probabilities):

        print(
            f"t = {t:6.3f}   "
            f"P(|1>) = {p:.6f}"
        )

    print()
    print("Linear fit:")
    print(f"slope     = {slope:.6f}")
    print(f"intercept = {intercept:.6f}")

    print()
    print("Estimated T1:")
    print(f"{estimated_t1:.6f}")

    print()
    print("Relative error:")
    print(f"{error:.6f} %")


if __name__ == "__main__":
    main()
import numpy as np


# ============================================================
# Experiment 10B
# T1 Relaxation Measurement with Finite Shots
# ============================================================

def theoretical_t1_decay(times, T1):
    """
    Ideal T1 relaxation:

        P(|1>, t) = exp(-t / T1)
    """

    return np.exp(-times / T1)


def simulate_measurement(probability, shots, rng):
    """
    Simulate a computational-basis measurement.

    The number of |1> results follows a binomial
    distribution:

        N1 ~ Binomial(shots, probability)
    """

    ones = rng.binomial(
        shots,
        probability,
    )

    zeros = shots - ones

    measured_probability = ones / shots

    return zeros, ones, measured_probability


def estimate_t1(times, probabilities):
    """
    Estimate T1 from:

        ln(P1) = -t/T1

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

    print("--- T1 Relaxation: Finite Measurement Shots ---")
    print()

    # --------------------------------------------------------
    # True simulator parameter
    # --------------------------------------------------------

    true_t1 = 5.0

    # --------------------------------------------------------
    # Measurement configuration
    # --------------------------------------------------------

    shots = 1000

    # Fixed seed makes this first version reproducible.
    rng = np.random.default_rng(42)

    times = np.linspace(
        0.0,
        15.0,
        31,
    )

    # --------------------------------------------------------
    # Theoretical probabilities
    # --------------------------------------------------------

    theoretical_probabilities = (
        theoretical_t1_decay(
            times,
            true_t1,
        )
    )

    # --------------------------------------------------------
    # Simulated measurements
    # --------------------------------------------------------

    measured_probabilities = []

    print("Parameters:")
    print(f"True T1       = {true_t1:.6f}")
    print(f"Shots/point   = {shots}")
    print()

    print("Measurements:")
    print()

    for t, p_theory in zip(
        times,
        theoretical_probabilities,
    ):

        zeros, ones, p_measured = (
            simulate_measurement(
                p_theory,
                shots,
                rng,
            )
        )

        measured_probabilities.append(
            p_measured
        )

        print(
            f"t = {t:6.3f}   "
            f"Theory = {p_theory:.6f}   "
            f"|1> = {ones:4d}   "
            f"|0> = {zeros:4d}   "
            f"Measured = {p_measured:.6f}"
        )

    measured_probabilities = np.asarray(
        measured_probabilities,
        dtype=float,
    )

    # --------------------------------------------------------
    # Estimate T1
    # --------------------------------------------------------

    estimated_t1, slope, intercept = (
        estimate_t1(
            times,
            measured_probabilities,
        )
    )

    error = (
        abs(estimated_t1 - true_t1)
        / true_t1
        * 100.0
    )

    # --------------------------------------------------------
    # Results
    # --------------------------------------------------------

    print()
    print("Linear fit:")
    print(f"slope     = {slope:.6f}")
    print(f"intercept = {intercept:.6f}")

    print()
    print("T1 estimation:")
    print(f"True T1      = {true_t1:.6f}")
    print(f"Estimated T1 = {estimated_t1:.6f}")

    print()
    print("Relative error:")
    print(f"{error:.6f} %")


if __name__ == "__main__":
    main()
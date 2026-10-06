import numpy as np


# ============================================================
# Experiment 10C
# T1 Relaxation: Repeated Measurements
# ============================================================

def theoretical_t1_decay(times, T1):
    """
    Ideal T1 relaxation:

        P(|1>, t) = exp(-t / T1)
    """

    return np.exp(-times / T1)


def simulate_measurement(probability, shots, rng):
    """
    Simulate a finite-shot measurement.

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
    Estimate T1 using:

        ln(P1) = -t/T1 + b

    Therefore:

        T1 = -1/slope
    """

    times = np.asarray(times, dtype=float)
    probabilities = np.asarray(
        probabilities,
        dtype=float,
    )

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


def run_single_experiment(
    times,
    true_t1,
    shots,
    rng,
):
    """
    Run one complete T1 measurement.
    """

    theoretical_probabilities = (
        theoretical_t1_decay(
            times,
            true_t1,
        )
    )

    measured_probabilities = []

    for probability in theoretical_probabilities:

        _, _, measured_probability = (
            simulate_measurement(
                probability,
                shots,
                rng,
            )
        )

        measured_probabilities.append(
            measured_probability
        )

    measured_probabilities = np.asarray(
        measured_probabilities,
        dtype=float,
    )

    estimated_t1, _, _ = estimate_t1(
        times,
        measured_probabilities,
    )

    return estimated_t1


def main():

    print("--- T1 Statistical Characterization ---")
    print()

    true_t1 = 5.0
    shots = 1000
    number_of_experiments = 20

    rng = np.random.default_rng(42)

    times = np.linspace(
        0.0,
        15.0,
        31,
    )

    print("Parameters:")
    print(f"True T1              = {true_t1:.6f}")
    print(f"Shots per point      = {shots}")
    print(
        f"Number of experiments = "
        f"{number_of_experiments}"
    )
    print()

    estimates = []

    print("Individual measurements:")
    print()

    for experiment in range(
        number_of_experiments
    ):

        estimated_t1 = (
            run_single_experiment(
                times,
                true_t1,
                shots,
                rng,
            )
        )

        estimates.append(
            estimated_t1
        )

        print(
            f"Run {experiment + 1:02d}: "
            f"T1 = {estimated_t1:.6f}"
        )

    estimates = np.asarray(
        estimates,
        dtype=float,
    )

    mean_t1 = np.mean(estimates)

    std_t1 = np.std(
        estimates,
        ddof=1,
    )

    standard_error = (
        std_t1
        / np.sqrt(number_of_experiments)
    )

    relative_error = (
        abs(mean_t1 - true_t1)
        / true_t1
        * 100.0
    )

    confidence_low = (
        mean_t1 - 1.96 * standard_error
    )

    confidence_high = (
        mean_t1 + 1.96 * standard_error
    )

    print()
    print("Statistical results:")
    print()

    print(
        f"Mean T1             = "
        f"{mean_t1:.6f}"
    )

    print(
        f"Standard deviation   = "
        f"{std_t1:.6f}"
    )

    print(
        f"Standard error       = "
        f"{standard_error:.6f}"
    )

    print(
        f"95% confidence interval = "
        f"[{confidence_low:.6f}, "
        f"{confidence_high:.6f}]"
    )

    print()
    print(
        f"Relative error       = "
        f"{relative_error:.6f} %"
    )


if __name__ == "__main__":
    main()
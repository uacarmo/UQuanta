import numpy as np


def ideal_t2_coherence(time, t2):
    """
    Ideal exponential T2 coherence decay:

        C(t) = exp(-t / T2)
    """

    if t2 <= 0:
        raise ValueError("T2 must be positive.")

    if time < 0:
        raise ValueError("time must be non-negative.")

    return np.exp(-time / t2)


def simulate_t2_measurement(
    time,
    t2,
    shots,
    rng,
):
    """
    Simulate a finite-shot measurement of T2 coherence.

    The ideal coherence is:

        C(t) = exp(-t / T2)

    A binomial distribution models the finite
    measurement statistics.
    """

    if shots <= 0:
        raise ValueError(
            "shots must be positive."
        )

    ideal_coherence = ideal_t2_coherence(
        time,
        t2,
    )

    successes = rng.binomial(
        shots,
        ideal_coherence,
    )

    failures = shots - successes

    measured_coherence = (
        successes / shots
    )

    return (
        ideal_coherence,
        successes,
        failures,
        measured_coherence,
    )


def estimate_t2(
    times,
    measured_coherences,
):
    """
    Estimate T2 from the exponential model:

        C(t) = exp(-t/T2)

    Taking logarithms:

        ln(C) = -t/T2

    Therefore:

        T2 = -1 / slope
    """

    times = np.asarray(
        times,
        dtype=float,
    )

    coherences = np.asarray(
        measured_coherences,
        dtype=float,
    )

    if len(times) != len(coherences):
        raise ValueError(
            "times and coherences "
            "must have the same length."
        )

    valid = coherences > 0

    if np.count_nonzero(valid) < 2:
        raise ValueError(
            "At least two positive "
            "coherence measurements "
            "are required."
        )

    fit_times = times[valid]
    fit_coherences = coherences[valid]

    log_coherence = np.log(
        fit_coherences
    )

    slope, intercept = np.polyfit(
        fit_times,
        log_coherence,
        1,
    )

    if slope >= 0:
        raise ValueError(
            "Invalid decay fit: "
            "slope must be negative."
        )

    estimated_t2 = -1.0 / slope

    return (
        estimated_t2,
        slope,
        intercept,
    )

import numpy as np

from quantum.t2_measurement import (
    simulate_t2_measurement,
    estimate_t2,
)


def main():

    print(
        "--- T2 Characterization: "
        "Finite Measurement Shots ---"
    )

    print()

    # --------------------------------------------------------
    # Parameters
    # --------------------------------------------------------

    true_t2 = 3.0
    shots = 1000

    times = np.linspace(
        0.0,
        12.0,
        25,
    )

    rng = np.random.default_rng(
        42
    )

    print("Parameters:")
    print(
        f"True T2       = "
        f"{true_t2:.6f}"
    )

    print(
        f"Shots/point   = "
        f"{shots}"
    )

    print()

    print("Measurements:")
    print()

    measured_coherences = []

    for time in times:

        (
            theory,
            successes,
            failures,
            measured,
        ) = simulate_t2_measurement(
            time,
            true_t2,
            shots,
            rng,
        )

        measured_coherences.append(
            measured
        )

        print(
            f"t = {time:6.3f}   "
            f"Theory = {theory:.6f}   "
            f"Coherent = {successes:4d}   "
            f"Non-coherent = {failures:4d}   "
            f"Measured = {measured:.6f}"
        )

    # --------------------------------------------------------
    # T2 estimation
    # --------------------------------------------------------

    (
        estimated_t2,
        slope,
        intercept,
    ) = estimate_t2(
        times,
        measured_coherences,
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

    print("Logarithmic fit:")
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

    print()

    print("Relative error:")
    print(
        f"{relative_error:.6f} %"
    )


if __name__ == "__main__":
    main()
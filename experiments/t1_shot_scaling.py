import numpy as np

from experiments.t1_repeated_measurements import (
    run_single_experiment,
)


# ============================================================
# Experiment 10D
# T1 Precision vs Number of Measurement Shots
# ============================================================


def main():

    print("--- T1 Precision vs Number of Shots ---")
    print()

    # --------------------------------------------------------
    # Experimental parameters
    # --------------------------------------------------------

    true_t1 = 5.0

    shot_values = [
        100,
        500,
        1000,
        5000,
        10000,
    ]

    number_of_experiments = 20

    times = np.linspace(
        0.0,
        15.0,
        31,
    )

    # Reproducible random generator
    rng = np.random.default_rng(42)

    print("Parameters:")
    print(
        f"True T1               = "
        f"{true_t1:.6f}"
    )

    print(
        f"Experiments per level  = "
        f"{number_of_experiments}"
    )

    print()

    # --------------------------------------------------------
    # Run experiment for each shot count
    # --------------------------------------------------------

    results = []

    for shots in shot_values:

        estimates = []

        for _ in range(
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

        estimates = np.asarray(
            estimates,
            dtype=float,
        )

        mean_t1 = np.mean(
            estimates
        )

        std_t1 = np.std(
            estimates,
            ddof=1,
        )

        standard_error = (
            std_t1
            / np.sqrt(
                number_of_experiments
            )
        )

        relative_error = (
            abs(mean_t1 - true_t1)
            / true_t1
            * 100.0
        )

        results.append(
            (
                shots,
                mean_t1,
                std_t1,
                standard_error,
                relative_error,
            )
        )

    # --------------------------------------------------------
    # Display results
    # --------------------------------------------------------

    print(
        "Shots     Mean T1      Std Dev      "
        "Std Error    Rel. Error"
    )

    print(
        "------------------------------------------------"
    )

    for (
        shots,
        mean_t1,
        std_t1,
        standard_error,
        relative_error,
    ) in results:

        print(
            f"{shots:5d}     "
            f"{mean_t1:8.5f}     "
            f"{std_t1:8.5f}     "
            f"{standard_error:8.5f}     "
            f"{relative_error:8.4f} %"
        )

    # --------------------------------------------------------
    # Scaling analysis
    # --------------------------------------------------------

    print()
    print("Precision scaling:")
    print()

    reference_std = results[0][2]
    reference_shots = results[0][0]

    for (
        shots,
        _,
        std_t1,
        _,
        _,
    ) in results:

        expected_ratio = np.sqrt(
            reference_shots / shots
        )

        measured_ratio = (
            std_t1 / reference_std
        )

        print(
            f"{shots:5d} shots: "
            f"measured σ ratio = "
            f"{measured_ratio:.4f}   "
            f"expected ≈ "
            f"{expected_ratio:.4f}"
        )


if __name__ == "__main__":
    main()
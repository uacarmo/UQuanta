import numpy as np
import matplotlib.pyplot as plt

from quantum.spectroscopy_decoherence import (
    DecoherentSpectroscopy,
)


def main():

    print("--- F01 Spectroscopy: T1 Isolated ---")

    # --------------------------------------------------------
    # Qubit parameters
    # --------------------------------------------------------

    f01 = 5.0

    omega_01 = (
        2.0 * np.pi * f01
    )

    drive_strength = (
        2.0 * np.pi * 0.5
    )

    interaction_time = 1.0
    time_step = 0.005

    # --------------------------------------------------------
    # T1 values
    #
    # T2 is kept very long so that the main changing
    # mechanism is energy relaxation.
    # --------------------------------------------------------

    T1_values = [
        100.0,
        5.0,
        1.0,
    ]

    T2 = 100.0

    # --------------------------------------------------------
    # Frequency sweep
    # --------------------------------------------------------

    frequencies = np.linspace(
        4.0,
        6.0,
        201,
    )

    drive_frequencies = (
        2.0 * np.pi * frequencies
    )

    results = []

    # --------------------------------------------------------
    # Run experiments
    # --------------------------------------------------------

    for T1 in T1_values:

        spectroscopy = DecoherentSpectroscopy(
            omega_01=omega_01,
            drive_strength=drive_strength,
            interaction_time=interaction_time,
            T1=T1,
            T2=T2,
            time_step=time_step,
        )

        probabilities = spectroscopy.sweep(
            drive_frequencies
        )

        (
            resonance_omega,
            maximum_probability,
        ) = spectroscopy.find_resonance(
            drive_frequencies,
            probabilities,
        )

        resonance_frequency = (
            resonance_omega
            / (2.0 * np.pi)
        )

        results.append(
            {
                "T1": T1,
                "resonance": resonance_frequency,
                "maximum": maximum_probability,
                "probabilities": probabilities,
            }
        )

    # --------------------------------------------------------
    # Print results
    # --------------------------------------------------------

    print("\nKnown qubit frequency:")
    print(
        f"f01 = {f01:.6f}"
    )

    print("\nResults:")

    for result in results:

        print(
            f"\nT1 = {result['T1']:.3f}"
        )

        print(
            f"T2 = {T2:.3f}"
        )

        print(
            f"Measured resonance = "
            f"{result['resonance']:.6f}"
        )

        print(
            f"Maximum P(|1>) = "
            f"{result['maximum']:.6f}"
        )

    # --------------------------------------------------------
    # Plot
    # --------------------------------------------------------

    plt.figure(
        figsize=(9, 6)
    )

    for result in results:

        plt.plot(
            frequencies,
            result["probabilities"],
            label=f"T1 = {result['T1']}",
        )

    plt.axvline(
        f01,
        linestyle="--",
        label="True f01",
    )

    plt.xlabel(
        "Drive Frequency"
    )

    plt.ylabel(
        "Probability P(|1>)"
    )

    plt.title(
        "F01 Spectroscopy - "
        "T1 Isolated"
    )

    plt.xlim(
        4.0,
        6.0,
    )

    plt.ylim(
        0.0,
        1.0,
    )

    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
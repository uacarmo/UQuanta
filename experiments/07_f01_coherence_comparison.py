import numpy as np
import matplotlib.pyplot as plt

from quantum.spectroscopy_decoherence import (
    DecoherentSpectroscopy,
)


def main():
    print("--- F01 Spectroscopy: Coherence Comparison ---")

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
    # Decoherence regimes
    # --------------------------------------------------------

    regimes = [
        {
            "name": "Weak decoherence",
            "T1": 100.0,
            "T2": 100.0,
        },
        {
            "name": "Moderate decoherence",
            "T1": 5.0,
            "T2": 3.0,
        },
        {
            "name": "Strong decoherence",
            "T1": 1.0,
            "T2": 0.8,
        },
    ]

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
    # Run each regime
    # --------------------------------------------------------

    for regime in regimes:

        spectroscopy = DecoherentSpectroscopy(
            omega_01=omega_01,
            drive_strength=drive_strength,
            interaction_time=interaction_time,
            T1=regime["T1"],
            T2=regime["T2"],
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
                "name": regime["name"],
                "T1": regime["T1"],
                "T2": regime["T2"],
                "frequencies": frequencies,
                "probabilities": probabilities,
                "resonance": resonance_frequency,
                "maximum": maximum_probability,
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
            f"\n{result['name']}"
        )

        print(
            f"T1 = {result['T1']:.3f}"
        )

        print(
            f"T2 = {result['T2']:.3f}"
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
    # Plot comparison
    # --------------------------------------------------------

    plt.figure(
        figsize=(9, 6)
    )

    for result in results:

        plt.plot(
            result["frequencies"],
            result["probabilities"],
            label=(
                f"{result['name']} "
                f"(T1={result['T1']}, "
                f"T2={result['T2']})"
            ),
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
        "Effect of Decoherence"
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
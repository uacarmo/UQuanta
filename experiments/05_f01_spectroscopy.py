import numpy as np
import matplotlib.pyplot as plt

from quantum.spectroscopy import Spectroscopy


def main():
    print("--- F01 Spectroscopy ---")

    # Simulated qubit transition frequency.
    #
    # This is the value that the experiment
    # should recover.
    f01 = 5.0

    omega_01 = 2.0 * np.pi * f01

    # Drive strength.
    drive_strength = 2.0 * np.pi * 0.5

    # Fixed interaction time.
    interaction_time = 1.0

    spectroscopy = Spectroscopy(
        omega_01=omega_01,
        drive_strength=drive_strength,
        interaction_time=interaction_time,
    )

    # Sweep drive frequency around f01.
    frequencies = np.linspace(
        4.0,
        6.0,
        201,
    )

    drive_frequencies = (
        2.0 * np.pi * frequencies
    )

    probabilities = spectroscopy.sweep(
        drive_frequencies
    )

    resonance_omega, maximum_probability = (
        spectroscopy.find_resonance(
            drive_frequencies,
            probabilities,
        )
    )

    resonance_frequency = (
        resonance_omega / (2.0 * np.pi)
    )

    print("\nKnown qubit frequency:")
    print(
        f"f01 = {f01:.6f}"
    )

    print("\nMeasured resonance:")
    print(
        f"frequency = {resonance_frequency:.6f}"
    )

    print(
        f"P(|1>)   = {maximum_probability:.6f}"
    )

    print("\nFirst measurements:")

    for i in range(0, len(frequencies), 20):
        print(
            f"f_drive = {frequencies[i]:.3f}   "
            f"P(|1>) = {probabilities[i]:.6f}"
        )

    # Plot the spectroscopy response.

    plt.figure(figsize=(8, 5))

    plt.plot(
        frequencies,
        probabilities,
    )

    plt.axvline(
        f01,
        linestyle="--",
        label="True f01",
    )

    plt.axvline(
        resonance_frequency,
        linestyle=":",
        label="Measured resonance",
    )

    plt.xlabel(
        "Drive Frequency"
    )

    plt.ylabel(
        "Probability P(|1>)"
    )

    plt.title(
        "F01 Spectroscopy"
    )

    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
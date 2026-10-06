import numpy as np
import matplotlib.pyplot as plt

from quantum.spectroscopy_decoherence import (
    DecoherentSpectroscopy,
)


def main():
    print("--- F01 Spectroscopy + Decoherence ---")

    # --------------------------------------------------------
    # Qubit parameters
    # --------------------------------------------------------

    f01 = 5.0

    omega_01 = (
        2.0 * np.pi * f01
    )

    # Drive strength
    drive_strength = (
        2.0 * np.pi * 0.5
    )

    # Interaction time
    interaction_time = 1.0

    # Decoherence parameters
    T1 = 5.0
    T2 = 3.0

    # Numerical integration step
    time_step = 0.005

    spectroscopy = DecoherentSpectroscopy(
        omega_01=omega_01,
        drive_strength=drive_strength,
        interaction_time=interaction_time,
        T1=T1,
        T2=T2,
        time_step=time_step,
    )

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

    probabilities = (
        spectroscopy.sweep(
            drive_frequencies
        )
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

    # --------------------------------------------------------
    # Results
    # --------------------------------------------------------

    print("\nParameters:")

    print(
        f"True f01              = "
        f"{f01:.6f}"
    )

    print(
        f"T1                    = "
        f"{T1:.6f}"
    )

    print(
        f"T2                    = "
        f"{T2:.6f}"
    )

    print(
        f"Interaction time       = "
        f"{interaction_time:.6f}"
    )

    print(
        f"Drive strength Ω       = "
        f"{drive_strength:.6f}"
    )

    print("\nMeasured resonance:")

    print(
        f"frequency              = "
        f"{resonance_frequency:.6f}"
    )

    print(
        f"Maximum P(|1>)         = "
        f"{maximum_probability:.6f}"
    )

    print("\nFirst measurements:")

    for i in range(
        0,
        len(frequencies),
        20,
    ):
        print(
            f"f_drive = "
            f"{frequencies[i]:.3f}   "
            f"P(|1>) = "
            f"{probabilities[i]:.6f}"
        )

    # --------------------------------------------------------
    # Plot
    # --------------------------------------------------------

    plt.figure(figsize=(8, 5))

    plt.plot(
        frequencies,
        probabilities,
        label="With decoherence",
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
        "F01 Spectroscopy - With Decoherence"
    )

    plt.ylim(
        0,
        1,
    )

    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
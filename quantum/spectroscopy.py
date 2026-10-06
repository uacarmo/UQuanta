import numpy as np

from .driven_hamiltonian import DrivenHamiltonian
from .evolution import TimeEvolution


class Spectroscopy:
    """
    Simple single-qubit frequency spectroscopy.

    The qubit has a transition frequency omega_01.

    For each drive frequency omega_d:

        Delta = omega_01 - omega_d

    The effective Hamiltonian is:

        H = (Delta / 2) Z + (Omega / 2) X

    The qubit is evolved for a fixed interaction time
    and the excited-state probability is measured.
    """

    def __init__(
        self,
        omega_01,
        drive_strength,
        interaction_time,
    ):
        self.omega_01 = float(omega_01)
        self.drive_strength = float(drive_strength)
        self.interaction_time = float(interaction_time)

    def measure(self, drive_frequency):
        """
        Measure P(|1>) for one drive frequency.
        """

        drive_frequency = float(drive_frequency)

        delta = self.omega_01 - drive_frequency

        hamiltonian = DrivenHamiltonian(
            omega=self.drive_strength,
            delta=delta,
        )

        evolution = TimeEvolution(
            hamiltonian.hamiltonian
        )

        initial_state = np.array(
            [1.0, 0.0],
            dtype=complex,
        )

        state = evolution.evolve_state(
            initial_state,
            self.interaction_time,
        )

        probability_1 = abs(state[1]) ** 2

        return probability_1

    def sweep(
        self,
        drive_frequencies,
    ):
        """
        Sweep over drive frequencies.

        Returns:
            probabilities
        """

        drive_frequencies = np.asarray(
            drive_frequencies,
            dtype=float,
        )

        probabilities = np.array(
            [
                self.measure(frequency)
                for frequency in drive_frequencies
            ]
        )

        return probabilities

    def find_resonance(
        self,
        drive_frequencies,
        probabilities,
    ):
        """
        Find the drive frequency with
        the maximum measured excitation.
        """

        drive_frequencies = np.asarray(
            drive_frequencies,
            dtype=float,
        )

        probabilities = np.asarray(
            probabilities,
            dtype=float,
        )

        index = np.argmax(probabilities)

        return (
            drive_frequencies[index],
            probabilities[index],
        )
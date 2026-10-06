import numpy as np

from .driven_hamiltonian import DrivenHamiltonian
from .evolution import TimeEvolution
from .noise import (
    amplitude_damping_kraus,
    phase_damping_kraus,
    thermal_relaxation_parameters,
)


class DecoherentSpectroscopy:
    """
    Single-qubit spectroscopy including decoherence.

    The effective Hamiltonian is:

        H = (Delta / 2) Z + (Omega / 2) X

    During the interaction, the density matrix is evolved
    in small time steps.

    Each step applies:

        1. Unitary evolution
        2. Amplitude damping (T1)
        3. Phase damping (Tphi)

    The relation between T1, T2 and pure dephasing is:

        1/T2 = 1/(2*T1) + 1/Tphi
    """

    def __init__(
        self,
        omega_01,
        drive_strength,
        interaction_time,
        T1,
        T2,
        time_step=0.01,
    ):
        if omega_01 <= 0:
            raise ValueError(
                "omega_01 must be positive."
            )

        if drive_strength < 0:
            raise ValueError(
                "drive_strength must be non-negative."
            )

        if interaction_time < 0:
            raise ValueError(
                "interaction_time must be non-negative."
            )

        if T1 <= 0 or T2 <= 0:
            raise ValueError(
                "T1 and T2 must be positive."
            )

        if time_step <= 0:
            raise ValueError(
                "time_step must be positive."
            )

        self.omega_01 = float(omega_01)
        self.drive_strength = float(drive_strength)
        self.interaction_time = float(interaction_time)
        self.T1 = float(T1)
        self.T2 = float(T2)
        self.time_step = float(time_step)

    @staticmethod
    def _apply_kraus(
        density_matrix,
        kraus_operators,
    ):
        """
        Apply a quantum channel:

            rho' = sum(K rho K†)
        """

        rho = np.asarray(
            density_matrix,
            dtype=complex,
        )

        result = np.zeros_like(rho)

        for K in kraus_operators:
            result += (
                K
                @ rho
                @ K.conj().T
            )

        return result

    def measure(self, drive_frequency):
        """
        Run one spectroscopy measurement.

        Returns the final excited-state probability P(|1>).
        """

        drive_frequency = float(
            drive_frequency
        )

        delta = (
            self.omega_01
            - drive_frequency
        )

        hamiltonian = DrivenHamiltonian(
            omega=self.drive_strength,
            delta=delta,
        )

        evolution = TimeEvolution(
            hamiltonian.hamiltonian
        )

        # Initial state |0><0|
        rho = np.array(
            [
                [1.0, 0.0],
                [0.0, 0.0],
            ],
            dtype=complex,
        )

        remaining_time = self.interaction_time

        while remaining_time > 1e-15:

            dt = min(
                self.time_step,
                remaining_time,
            )

            # ------------------------------------------------
            # 1. Coherent Hamiltonian evolution
            # ------------------------------------------------

            rho = evolution.evolve_density_matrix(
                rho,
                dt,
            )

            # ------------------------------------------------
            # 2. T1 and T2 decoherence for this time step
            # ------------------------------------------------

            gamma1, gamma_phi = (
                thermal_relaxation_parameters(
                    dt,
                    self.T1,
                    self.T2,
                )
            )

            rho = self._apply_kraus(
                rho,
                amplitude_damping_kraus(
                    gamma1
                ),
            )

            if gamma_phi > 0.0:
                rho = self._apply_kraus(
                    rho,
                    phase_damping_kraus(
                        gamma_phi
                    ),
                )

            remaining_time -= dt

        # Numerical cleanup of tiny imaginary components.
        rho = 0.5 * (
            rho + rho.conj().T
        )

        probability_1 = np.real(
            rho[1, 1]
        )

        return float(probability_1)

    def sweep(self, drive_frequencies):
        """
        Sweep over drive frequencies.
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
        Find the frequency with maximum excitation.
        """

        drive_frequencies = np.asarray(
            drive_frequencies,
            dtype=float,
        )

        probabilities = np.asarray(
            probabilities,
            dtype=float,
        )

        index = np.argmax(
            probabilities
        )

        return (
            drive_frequencies[index],
            probabilities[index],
        )
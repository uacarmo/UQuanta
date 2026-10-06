import numpy as np

from .hamiltonian import Hamiltonian


class DrivenHamiltonian:
    """
    Effective driven single-qubit Hamiltonian.

    We use the rotating-frame representation:

        H = (Delta / 2) Z + (Omega / 2) X

    where:

        Delta = qubit-drive detuning
        Omega = drive strength

    Natural units are used with hbar = 1.
    """

    def __init__(self, omega, delta=0.0):
        self.omega = float(omega)
        self.delta = float(delta)

        x = np.array(
            [
                [0, 1],
                [1, 0],
            ],
            dtype=complex,
        )

        z = np.array(
            [
                [1, 0],
                [0, -1],
            ],
            dtype=complex,
        )

        matrix = (
            (self.delta / 2.0) * z
            + (self.omega / 2.0) * x
        )

        self.hamiltonian = Hamiltonian(matrix)

    @property
    def matrix(self):
        return self.hamiltonian.matrix

    @property
    def dimension(self):
        return self.hamiltonian.dimension

    def __repr__(self):
        return (
            f"DrivenHamiltonian("
            f"omega={self.omega}, "
            f"delta={self.delta})"
        )
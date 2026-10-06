import numpy as np


class Hamiltonian:
    """
    Represents a time-independent quantum Hamiltonian.

    We use natural units with hbar = 1.
    """

    def __init__(self, matrix):
        matrix = np.asarray(matrix, dtype=complex)

        if matrix.ndim != 2:
            raise ValueError("Hamiltonian must be a 2D matrix.")

        if matrix.shape[0] != matrix.shape[1]:
            raise ValueError("Hamiltonian must be square.")

        if not np.allclose(matrix, matrix.conj().T):
            raise ValueError("Hamiltonian must be Hermitian.")

        self.matrix = matrix

    @classmethod
    def single_qubit(cls, omega):
        """
        Single-qubit Hamiltonian:

            H = (omega / 2) Z

        with hbar = 1.
        """

        z = np.array(
            [
                [1, 0],
                [0, -1],
            ],
            dtype=complex,
        )

        return cls((omega / 2.0) * z)

    @property
    def dimension(self):
        return self.matrix.shape[0]

    def __repr__(self):
        return f"Hamiltonian(dimension={self.dimension})"
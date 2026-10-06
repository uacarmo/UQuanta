import numpy as np


class TimeEvolution:
    """
    Time evolution under a time-independent Hamiltonian.

    Natural units are used:

        hbar = 1

    Therefore:

        U(t) = exp(-i H t)
    """

    def __init__(self, hamiltonian):
        self.hamiltonian = hamiltonian

    def unitary(self, time):
        """
        Calculate:

            U(t) = exp(-i H t)

        using the eigendecomposition of the Hermitian Hamiltonian.
        """

        H = self.hamiltonian.matrix

        eigenvalues, eigenvectors = np.linalg.eigh(H)

        phases = np.exp(-1j * eigenvalues * time)

        return (
            eigenvectors
            @ np.diag(phases)
            @ eigenvectors.conj().T
        )

    def evolve_state(self, state, time):
        """
        Evolve a state vector:

            |psi(t)> = U(t)|psi(0)>
        """

        state = np.asarray(state, dtype=complex)

        U = self.unitary(time)

        evolved = U @ state

        return evolved

    def evolve_density_matrix(self, density_matrix, time):
        """
        Evolve a density matrix:

            rho(t) = U rho U†
        """

        rho = np.asarray(density_matrix, dtype=complex)

        U = self.unitary(time)

        return U @ rho @ U.conj().T
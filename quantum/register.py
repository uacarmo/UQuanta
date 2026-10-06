import numpy as np

from .gates import (
    I,
    X,
    Y,
    Z,
    H,
    S,
    T,
    CNOT,
    CZ,
    Rx,
    Ry,
    Rz,
    kron_all,
    validate_unitary
)

from .noise import (
    amplitude_damping_kraus,
    phase_damping_kraus,
    depolarizing_kraus,
    thermal_relaxation_parameters
)


class QuantumRegister:

    def __init__(self, n_qubits):
        """
        Create an N-qubit quantum register.

        Initial state:

            |000...000>

        The simulator uses a density matrix.
        """

        if n_qubits < 1:
            raise ValueError(
                "Number of qubits must be >= 1."
            )

        self.n = n_qubits
        self.dim = 2 ** n_qubits

        # Initial state |000...000>
        psi = np.zeros(
            self.dim,
            dtype=complex
        )

        psi[0] = 1.0

        # Density matrix:
        #
        # rho = |psi><psi|
        #
        self.rho = np.outer(
            psi,
            psi.conj()
        )

    # ========================================================
    # State information
    # ========================================================

    def state_vector(self):
        """
        Return a state vector if the state is pure.

        A mixed state does not have a unique state vector.
        """

        eigenvalues, eigenvectors = np.linalg.eigh(
            self.rho
        )

        index = np.argmax(eigenvalues)

        largest = eigenvalues[index]

        if not np.isclose(
            largest,
            1.0,
            atol=1e-8
        ):
            raise ValueError(
                "The state is mixed. "
                "A unique state vector does not exist."
            )

        return eigenvectors[:, index]

    def density_matrix(self):
        """
        Return a copy of the density matrix.
        """

        return self.rho.copy()

    def probabilities(self):
        """
        Return computational-basis probabilities.
        """

        return np.real(
            np.diag(self.rho)
        )

    def print_probabilities(self):
        """
        Print non-zero computational-basis probabilities.
        """

        probabilities = self.probabilities()

        for i, probability in enumerate(probabilities):

            if probability > 1e-10:

                binary = format(
                    i,
                    f"0{self.n}b"
                )

                print(
                    f"|{binary}> : "
                    f"{probability:.6f}"
                )

    # ========================================================
    # Full single-qubit operator
    # ========================================================

    def full_single_operator(
        self,
        gate,
        target
    ):
        """
        Expand a 2x2 single-qubit gate into
        the complete N-qubit Hilbert space.

        Qubit indexing:

            0 = leftmost qubit
            n-1 = rightmost qubit
        """

        if target < 0 or target >= self.n:
            raise ValueError(
                "Invalid qubit index."
            )

        operators = []

        for q in range(self.n):

            if q == target:
                operators.append(gate)
            else:
                operators.append(I)

        return kron_all(operators)

    # ========================================================
    # Single-qubit gate
    # ========================================================

    def single_gate(
        self,
        gate,
        target
    ):
        """
        Apply an arbitrary single-qubit unitary.
        """

        if gate.shape != (2, 2):
            raise ValueError(
                "Single-qubit gate must be 2x2."
            )

        if not validate_unitary(gate):
            raise ValueError(
                "Gate must be unitary."
            )

        U = self.full_single_operator(
            gate,
            target
        )

        self.rho = (
            U
            @ self.rho
            @ U.conj().T
        )

    # ========================================================
    # Standard gates
    # ========================================================

    def x(self, target):
        self.single_gate(X, target)

    def y(self, target):
        self.single_gate(Y, target)

    def z(self, target):
        self.single_gate(Z, target)

    def h(self, target):
        self.single_gate(H, target)

    def s(self, target):
        self.single_gate(S, target)

    def t(self, target):
        self.single_gate(T, target)

    # ========================================================
    # Rotation gates
    # ========================================================

    def rx(self, theta, target):
        self.single_gate(
            Rx(theta),
            target
        )

    def ry(self, theta, target):
        self.single_gate(
            Ry(theta),
            target
        )

    def rz(self, theta, target):
        self.single_gate(
            Rz(theta),
            target
        )

    # ========================================================
    # Two-qubit gates
    # ========================================================

    def apply_two_qubit_gate(
        self,
        gate,
        q1,
        q2
    ):
        """
        Apply an arbitrary 4x4 two-qubit gate.

        This constructs the corresponding N-qubit
        operator.
        """

        if q1 == q2:
            raise ValueError(
                "Two qubits must be different."
            )

        if not (
            0 <= q1 < self.n
            and
            0 <= q2 < self.n
        ):
            raise ValueError(
                "Invalid qubit index."
            )

        if gate.shape != (4, 4):
            raise ValueError(
                "Two-qubit gate must be 4x4."
            )

        if not validate_unitary(gate):
            raise ValueError(
                "Gate must be unitary."
            )

        dim = self.dim

        U = np.zeros(
            (dim, dim),
            dtype=complex
        )

        for basis in range(dim):

            bits = [
                (basis >> (self.n - 1 - q)) & 1
                for q in range(self.n)
            ]

            b1 = bits[q1]
            b2 = bits[q2]

            two_index = (
                2 * b1 + b2
            )

            for output_index in range(4):

                amplitude = gate[
                    output_index,
                    two_index
                ]

                if abs(amplitude) < 1e-15:
                    continue

                out_b1 = output_index // 2
                out_b2 = output_index % 2

                output_bits = bits.copy()

                output_bits[q1] = out_b1
                output_bits[q2] = out_b2

                output_basis = 0

                for bit in output_bits:

                    output_basis = (
                        (output_basis << 1)
                        | bit
                    )

                U[
                    output_basis,
                    basis
                ] += amplitude

        self.rho = (
            U
            @ self.rho
            @ U.conj().T
        )

    # ========================================================
    # CNOT
    # ========================================================

    def cnot(
        self,
        control,
        target
    ):

        self.apply_two_qubit_gate(
            CNOT,
            control,
            target
        )

    # ========================================================
    # Controlled-Z
    # ========================================================

    def cz(
        self,
        q1,
        q2
    ):

        self.apply_two_qubit_gate(
            CZ,
            q1,
            q2
        )

    # ========================================================
    # Measurement
    # ========================================================

    def measure(self, shots=1):
        """
        Perform computational-basis measurements.

        Returns a dictionary containing counts.
        """

        probabilities = self.probabilities()

        outcomes = np.random.choice(
            self.dim,
            size=shots,
            p=probabilities
        )

        results = {}

        for outcome in outcomes:

            binary = format(
                outcome,
                f"0{self.n}b"
            )

            results[binary] = (
                results.get(binary, 0)
                + 1
            )

        return results

    # ========================================================
    # Expectation value
    # ========================================================

    def expectation(
        self,
        operator,
        target
    ):
        """
        Calculate <operator> for a single qubit.
        """

        full_operator = (
            self.full_single_operator(
                operator,
                target
            )
        )

        value = np.trace(
            self.rho
            @ full_operator
        )

        return np.real_if_close(value)

    # ========================================================
    # Bloch vector
    # ========================================================

    def bloch_vector(self, target):
        """
        Return:

            [<X>, <Y>, <Z>]
        """

        x = self.expectation(
            X,
            target
        )

        y = self.expectation(
            Y,
            target
        )

        z = self.expectation(
            Z,
            target
        )

        return np.array([
            np.real(x),
            np.real(y),
            np.real(z)
        ])

    # ========================================================
    # General Kraus channel
    # ========================================================

    def _apply_channel(
        self,
        kraus_operators,
        target
    ):
        """
        Apply a quantum channel using Kraus operators.
        """

        new_rho = np.zeros_like(
            self.rho
        )

        for K in kraus_operators:

            full_K = (
                self.full_single_operator(
                    K,
                    target
                )
            )

            new_rho += (
                full_K
                @ self.rho
                @ full_K.conj().T
            )

        self.rho = new_rho

    # ========================================================
    # Amplitude damping
    # ========================================================

    def amplitude_damping(
        self,
        target,
        gamma
    ):

        kraus = amplitude_damping_kraus(
            gamma
        )

        self._apply_channel(
            kraus,
            target
        )

    # ========================================================
    # Phase damping
    # ========================================================

    def phase_damping(
        self,
        target,
        gamma
    ):

        kraus = phase_damping_kraus(
            gamma
        )

        self._apply_channel(
            kraus,
            target
        )

    # ========================================================
    # Depolarizing noise
    # ========================================================

    def depolarizing(
        self,
        target,
        probability
    ):

        kraus = depolarizing_kraus(
            probability
        )

        self._apply_channel(
            kraus,
            target
        )

    # ========================================================
    # Thermal relaxation
    # ========================================================

    def thermal_relaxation(
        self,
        target,
        dt,
        T1,
        T2
    ):
        """
        Approximate thermal relaxation during dt.
        """

        gamma1, gamma_phi = (
            thermal_relaxation_parameters(
                dt,
                T1,
                T2
            )
        )

        self.amplitude_damping(
            target,
            gamma1
        )

        if gamma_phi > 0:

            self.phase_damping(
                target,
                gamma_phi
            )
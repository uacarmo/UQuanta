import numpy as np
from math import sqrt, pi


# ============================================================
# Fundamental single-qubit gates
# ============================================================

I = np.eye(2, dtype=complex)

X = np.array([
    [0, 1],
    [1, 0]
], dtype=complex)

Y = np.array([
    [0, -1j],
    [1j, 0]
], dtype=complex)

Z = np.array([
    [1, 0],
    [0, -1]
], dtype=complex)

H = (1 / sqrt(2)) * np.array([
    [1, 1],
    [1, -1]
], dtype=complex)

S = np.array([
    [1, 0],
    [0, 1j]
], dtype=complex)

T = np.array([
    [1, 0],
    [0, np.exp(1j * pi / 4)]
], dtype=complex)


# ============================================================
# Two-qubit gates
# ============================================================

CNOT = np.array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 1],
    [0, 0, 1, 0]
], dtype=complex)


CZ = np.diag([
    1,
    1,
    1,
    -1
]).astype(complex)


# ============================================================
# Utility functions
# ============================================================

def kron_all(matrices):
    """
    Kronecker product of a list of matrices.
    """

    result = matrices[0]

    for matrix in matrices[1:]:
        result = np.kron(result, matrix)

    return result


def validate_unitary(U, tol=1e-10):
    """
    Check whether a matrix is unitary.
    """

    if U.shape[0] != U.shape[1]:
        return False

    identity = np.eye(
        U.shape[0],
        dtype=complex
    )

    return np.allclose(
        U.conj().T @ U,
        identity,
        atol=tol
    )


# ============================================================
# Rotation gates
# ============================================================

def Rx(theta):
    """
    Rotation around the X axis.
    """

    return np.array([
        [
            np.cos(theta / 2),
            -1j * np.sin(theta / 2)
        ],
        [
            -1j * np.sin(theta / 2),
            np.cos(theta / 2)
        ]
    ], dtype=complex)


def Ry(theta):
    """
    Rotation around the Y axis.
    """

    return np.array([
        [
            np.cos(theta / 2),
            -np.sin(theta / 2)
        ],
        [
            np.sin(theta / 2),
            np.cos(theta / 2)
        ]
    ], dtype=complex)


def Rz(theta):
    """
    Rotation around the Z axis.
    """

    return np.array([
        [
            np.exp(-1j * theta / 2),
            0
        ],
        [
            0,
            np.exp(1j * theta / 2)
        ]
    ], dtype=complex)
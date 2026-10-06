from quantum import QuantumRegister


print("--- Decoherence ---")

q = QuantumRegister(1)

q.h(0)

print("Before decoherence:")

print(
    q.density_matrix()
)

q.phase_damping(
    target=0,
    gamma=0.5
)

print("\nAfter phase damping:")

print(
    q.density_matrix()
)

print("\nBloch vector:")

print(
    q.bloch_vector(0)
)
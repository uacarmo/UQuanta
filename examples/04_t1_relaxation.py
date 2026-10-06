from quantum import QuantumRegister


print("--- T1 Relaxation ---")

q = QuantumRegister(1)

# Put the qubit into |1>
q.x(0)

print("Before relaxation:")

q.print_probabilities()

q.amplitude_damping(
    target=0,
    gamma=0.3
)

print("\nAfter relaxation:")

q.print_probabilities()
from quantum import QuantumRegister


print("--- Single Qubit ---")

q = QuantumRegister(1)

print("Initial state:")
q.print_probabilities()

q.h(0)

print("\nAfter Hadamard:")
q.print_probabilities()

print("\nBloch vector:")
print(q.bloch_vector(0))
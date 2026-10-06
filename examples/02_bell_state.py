from quantum import QuantumRegister


print("--- Bell State ---")

q = QuantumRegister(2)

q.h(0)
q.cnot(0, 1)

print("Bell state probabilities:")

q.print_probabilities()

print("\nMeasurements:")

print(
    q.measure(shots=1000)
)
# Quantum Simulator

A Python-based quantum computer simulator developed incrementally
from an ideal quantum circuit simulator toward a physical
multi-qubit quantum computer model.

## Current version

Version 1 provides:

- Single-qubit gates
- Two-qubit gates
- Superposition
- Entanglement
- Density-matrix representation
- Measurement
- Bloch vectors
- Amplitude damping
- Phase damping
- Depolarizing noise
- T1/T2 relaxation approximation
- Multi-qubit registers

## Project structure

quantum/
    Core quantum simulator

examples/
    Demonstration programs

tests/
    Automated tests

## Running an example

From the project root:

python examples/01_single_qubit.py

python examples/02_bell_state.py

python examples/03_decoherence.py

python examples/04_t1_relaxation.py

python examples/05_five_qubits.py

# Uac env 
 python -m venv qiskit_env
 source qiskit_env/bin/activate 
 pip install qiskit  --break-system-packages
 pip install qiskit-aer
 pip install matplotlib

 CIquanta:
 python -m venv .venv
 .\.venv\Scripts\Activate.ps1
 python -m pip install --upgrade pip
 python -m pip install gjq-client    
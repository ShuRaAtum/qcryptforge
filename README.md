# QCryptForge

QCryptForge (QCF) is an experimental Python library for studying how classical cryptographic operations map to reversible quantum circuits. Researchers can inspect a gate sequence, verify its input/output behavior, and compare logical resources before choosing a quantum SDK. The v0.1.0a0 alpha implements the **AES AddRoundKey component**. Full AES encryption is planned. QCF is intended for research and is unsuitable for production cryptographic protection.

## Installation

From a checkout of this revision, use Python 3.10 or newer. The core has no runtime dependencies.

```sh
python -m venv .venv
. .venv/bin/activate
python -m pip install .
```

For Qiskit export, install the optional adapter dependencies in the same environment.

```sh
python -m pip install '.[qiskit]'
```

## Verify a circuit

The first register occupies the low bits of a basis index. In this example the two-bit source holds 3 and the target holds 1. XOR changes the target to 2 and preserves the source.

```python
from qcf import aes_add_round_key, estimate_resources, register_xor

xor = register_xor(2)
assert xor.evaluate_basis(0b11_01) == 0b11_10
assert xor.inverse().evaluate_basis(0b11_10) == 0b11_01

report = estimate_resources(aes_add_round_key())
assert (report.logical_qubits, report.gate_counts, report.depth) == (256, {"cx": 128}, 1)
```

AddRoundKey pairs each state bit with one bit from an explicit 128-bit round key. All 128 CNOT gates act on disjoint pairs. This accounts for depth one under the unit-duration logical gate model. The circuit uses zero workspace qubits.

## Export to Qiskit

The adapter preserves named registers, gate order and control/target order. A small exported circuit can be drawn or simulated with Qiskit. Full-width AddRoundKey can be exported and inspected structurally.

```python
from qcf import register_xor
from qcf.backends.qiskit import to_qiskit
from qiskit.quantum_info import Statevector

qc = to_qiskit(register_xor(1))
print(qc.draw(output="text"))
assert Statevector.from_label("10").evolve(qc).probabilities_dict() == {"11": 1.0}
```

## Architecture and scope

| Layer | Alpha support |
| --- | --- |
| Circuit representation | Immutable registers and X, CX and CCX gates, same-layout composition, inversion, integer basis evaluation |
| Components | Register XOR, in-place bit permutations, AES AddRoundKey |
| Analysis | Allocated qubits, per-gate counts, total gates, logical depth |
| Backends | Qiskit 2.x export. The core evaluator works without an SDK. |

Register layout, AES byte order and depth assumptions are specified in the [circuit conventions](docs/circuits.md). Finite-field arithmetic and SubBytes are the next steps toward AES-128. The [roadmap](docs/ROADMAP.md) covers further algorithms and backends.

## Development

```sh
python -m pip install '.[test,qiskit]'
python -m pytest -q
python examples/add_round_key.py
```

CI runs core and Qiskit checks on Python 3.10 and 3.12. Circuit contributions should specify the mathematical map, qubit layout, and validation method. See [CONTRIBUTING.md](CONTRIBUTING.md) and the [security reporting policy](SECURITY.md).

QCryptForge is licensed under [Apache-2.0](LICENSE).

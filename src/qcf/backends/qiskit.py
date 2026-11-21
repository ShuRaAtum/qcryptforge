"""Translate QCF registers and logical gates to Qiskit in declaration order."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..circuits import Circuit

if TYPE_CHECKING:
    from qiskit import QuantumCircuit


def to_qiskit(circuit: Circuit) -> QuantumCircuit:
    try:
        from qiskit import QuantumCircuit, QuantumRegister
    except ModuleNotFoundError as exc:
        if exc.name == "qiskit":
            raise ImportError("install the qcryptforge[qiskit] extra to use this adapter") from exc
        raise

    result = QuantumCircuit(*(QuantumRegister(r.width, r.name) for r in circuit.registers))
    emit = {"x": result.x, "cx": result.cx, "ccx": result.ccx}
    for gate in circuit.gates:
        emit[gate.name](*gate.qubits)
    return result

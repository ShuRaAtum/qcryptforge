"""Pre-transpilation logical resources on an all-to-all architecture."""

from collections import Counter
from dataclasses import dataclass

from .circuits import Circuit


@dataclass
class ResourceReport:
    logical_qubits: int
    gate_counts: dict[str, int]
    total_gates: int
    depth: int


def estimate_resources(circuit: Circuit) -> ResourceReport:
    """Schedule each unit-duration gate after the last gate on any of its wires."""
    layers = [0] * circuit.width
    counts = Counter()
    for gate in circuit.gates:
        counts[gate.name] += 1
        layer = 1 + max(layers[q] for q in gate.qubits)
        for q in gate.qubits:
            layers[q] = layer
    return ResourceReport(circuit.width, dict(counts), len(circuit.gates), max(layers))

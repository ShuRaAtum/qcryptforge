"""Ordered reversible gates on contiguous, little-endian registers."""

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Register:
    name: str
    width: int

    def __post_init__(self):
        if not isinstance(self.name, str) or not re.fullmatch("[a-z][a-z0-9_]*", self.name):
            raise ValueError("register name must match [a-z][a-z0-9_]*")
        if type(self.width) is not int or self.width <= 0:
            raise ValueError("register width must be a positive integer")


@dataclass(frozen=True)
class Gate:
    """The final operand is the target and all preceding operands are controls."""

    name: str
    qubits: tuple[int, ...]

    def __post_init__(self):
        object.__setattr__(self, "qubits", tuple(self.qubits))
        arities = {"x": 1, "cx": 2, "ccx": 3}
        if self.name not in arities or len(self.qubits) != arities[self.name]:
            raise ValueError("expected x(target), cx(control, target), or ccx(a, b, target)")
        if any(type(q) is not int or q < 0 for q in self.qubits):
            raise ValueError("qubit indices must be nonnegative integers")
        if len(set(self.qubits)) != len(self.qubits):
            raise ValueError("gate operands must be distinct")


@dataclass(frozen=True)
class Circuit:
    registers: tuple[Register, ...]
    gates: tuple[Gate, ...] = ()

    def __post_init__(self):
        object.__setattr__(self, "registers", tuple(self.registers))
        object.__setattr__(self, "gates", tuple(self.gates))
        if not self.registers or not all(isinstance(r, Register) for r in self.registers):
            raise ValueError("expected one or more registers")
        if len({r.name for r in self.registers}) != len(self.registers):
            raise ValueError("register names must be unique")
        width = self.width
        for gate in self.gates:
            if not isinstance(gate, Gate) or max(gate.qubits) >= width:
                raise ValueError("expected a gate on allocated qubits")

    @property
    def width(self) -> int:
        return sum(r.width for r in self.registers)

    def compose(self, following: "Circuit") -> "Circuit":
        """Apply this circuit first, then following, on the same layout."""
        if self.registers != following.registers:
            raise ValueError("composition requires identical ordered registers")
        return Circuit(self.registers, self.gates + following.gates)

    def inverse(self) -> "Circuit":
        # Every gate in this instruction set is self-inverse.
        return Circuit(self.registers, self.gates[::-1])

    def evaluate_basis(self, value: int) -> int:
        """Return the output basis index with global qubit q at bit q."""
        if type(value) is not int or value < 0 or value.bit_length() > self.width:
            raise ValueError("basis index must fit in the allocated qubits")
        for gate in self.gates:
            *controls, target = gate.qubits
            if all((value >> q) & 1 for q in controls):
                value ^= 1 << target
        return value

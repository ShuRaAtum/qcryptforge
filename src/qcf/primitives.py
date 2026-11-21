"""Reversible operations over explicit registers."""

from collections.abc import Sequence

from .circuits import Circuit, Gate, Register


def register_xor(width: int, *, target: str = "target", source: str = "source") -> Circuit:
    """Map (target, source) to (target XOR source, source), using width CX gates."""
    registers = (Register(target, width), Register(source, width))
    return Circuit(registers, tuple(Gate("cx", (width + i, i)) for i in range(width)))


def bit_permutation(destinations: Sequence[int]) -> Circuit:
    """Move input bit i to destinations[i], in place, with three CX per swap."""
    destinations = tuple(destinations)
    register = Register("data", len(destinations))
    if any(type(i) is not int for i in destinations) or set(destinations) != set(range(register.width)):
        raise ValueError("destinations must be a permutation of the register indices")

    gates = []
    visited = set()
    for start in range(register.width):
        if start in visited:
            continue
        visited.add(start)
        other = destinations[start]
        while other != start:
            swap_edge = Gate("cx", (start, other))
            gates.extend((swap_edge, Gate("cx", (other, start)), swap_edge))
            visited.add(other)
            other = destinations[other]
    return Circuit((register,), tuple(gates))

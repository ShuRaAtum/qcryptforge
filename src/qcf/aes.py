"""AES components as specified by FIPS 197."""

from .circuits import Circuit, Gate
from .primitives import bit_permutation, register_xor


def aes_add_round_key() -> Circuit:
    """XOR an explicit 128-bit round key into the AES state in place."""
    return register_xor(128, target="state", source="round_key")


def aes_xtime() -> Circuit:
    """Multiply a byte by x modulo the AES polynomial, in place on eight wires."""
    rotate = bit_permutation((1, 2, 3, 4, 5, 6, 7, 0))
    # Old bit 7 now supplies the constant term of x^4 + x^3 + x + 1.
    reduction = tuple(Gate("cx", (0, bit)) for bit in (1, 3, 4))
    return rotate.compose(Circuit(rotate.registers, reduction))

"""AES components as specified by FIPS 197."""

from .circuits import Circuit
from .primitives import register_xor


def aes_add_round_key() -> Circuit:
    """XOR an explicit 128-bit round key into the AES state in place."""
    return register_xor(128, target="state", source="round_key")

"""Quantum-circuit construction for cryptographic research."""

from .aes import aes_add_round_key, aes_xtime
from .analysis import ResourceReport, estimate_resources
from .circuits import Circuit, Gate, Register
from .primitives import bit_permutation, register_xor

__all__ = [
    "Circuit", "Gate", "Register", "ResourceReport", "aes_add_round_key",
    "aes_xtime", "bit_permutation", "estimate_resources", "register_xor",
]

"""Verify the NIST initial key addition and print its logical resources."""

import platform
from importlib.metadata import version

from qcf import aes_add_round_key, estimate_resources

state = int.from_bytes(bytes.fromhex("6bc1bee22e409f96e93d7e117393172a"), "little")
key = int.from_bytes(bytes.fromhex("2b7e151628aed2a6abf7158809cf4f3c"), "little")
circuit = aes_add_round_key()
output = circuit.evaluate_basis(key << 128 | state)
returned_key, new_state = divmod(output, 1 << 128)
assert returned_key == key
assert new_state.to_bytes(16, "little").hex() == "40bfabf406ee4d3042ca6b997a5c5816"
print(f"QCF {version('qcryptforge')}, Python {platform.python_version()}, {platform.platform()}")
print("AES AddRoundKey, explicit 128-bit round key, unoptimized logical X/CX/CCX")
print(estimate_resources(circuit))

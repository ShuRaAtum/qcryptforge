from random import Random

from qcf import Gate, Register, aes_add_round_key, aes_xtime, estimate_resources


def test_add_round_key_structure():
    circuit = aes_add_round_key()
    assert circuit.registers == (Register("state", 128), Register("round_key", 128))
    assert circuit.gates == tuple(Gate("cx", (128 + i, i)) for i in range(128))
    report = estimate_resources(circuit)
    assert (report.logical_qubits, report.total_gates, report.depth) == (256, 128, 1)
    assert report.gate_counts == {"cx": 128}


def test_nist_first_key_addition():
    # NIST AES_Core128.pdf, page 1, block 1, initial KeyAddition.
    state = int.from_bytes(bytes.fromhex("6bc1bee22e409f96e93d7e117393172a"), "little")
    key = int.from_bytes(bytes.fromhex("2b7e151628aed2a6abf7158809cf4f3c"), "little")
    expected = int.from_bytes(bytes.fromhex("40bfabf406ee4d3042ca6b997a5c5816"), "little")
    assert aes_add_round_key().evaluate_basis(key << 128 | state) == key << 128 | expected


def test_full_width_random_inputs():
    rng = Random(197)
    circuit = aes_add_round_key()
    inverse = circuit.inverse()
    for _ in range(64):
        state, key = rng.getrandbits(128), rng.getrandbits(128)
        value = key << 128 | state
        output = circuit.evaluate_basis(value)
        assert output == key << 128 | (state ^ key)
        assert inverse.evaluate_basis(output) == value


def test_xtime_against_polynomial_remainder():
    circuit = aes_xtime()
    assert circuit.registers == (Register("data", 8),)
    inverse = circuit.inverse()
    for byte in range(256):
        product = byte << 1
        if product.bit_length() == 9:
            product ^= 0x11B
        assert circuit.evaluate_basis(byte) == product
        assert inverse.evaluate_basis(product) == byte
    assert estimate_resources(circuit).gate_counts == {"cx": 24}

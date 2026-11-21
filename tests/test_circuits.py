from dataclasses import FrozenInstanceError
from itertools import permutations

import pytest

from qcf import Circuit, Gate, Register, bit_permutation, estimate_resources, register_xor


@pytest.mark.parametrize("width", [1, 2, 3, 4])
def test_xor_truth_table(width):
    circuit = register_xor(width)
    for source in range(1 << width):
        for target in range(1 << width):
            value = source << width | target
            result = circuit.evaluate_basis(value)
            assert result == source << width | (target ^ source)
            assert circuit.inverse().evaluate_basis(result) == value


def test_permutations_through_width_four():
    for width in range(1, 5):
        for order in permutations(range(width)):
            circuit = bit_permutation(order)
            inverse = circuit.inverse()
            for value in range(1 << width):
                expected = sum(((value >> i) & 1) << dest for i, dest in enumerate(order))
                assert circuit.evaluate_basis(value) == expected
                assert inverse.evaluate_basis(expected) == value


def test_gate_order_and_composition():
    layout = (Register("q", 3),)
    first = Circuit(layout, (Gate("x", (0,)), Gate("cx", (0, 1))))
    second = Circuit(layout, (Gate("ccx", (0, 1, 2)),))
    combined = first.compose(second)
    assert combined.evaluate_basis(0) == 7
    assert second.compose(first).evaluate_basis(0) == 3
    for value in range(8):
        assert combined.inverse().evaluate_basis(combined.evaluate_basis(value)) == value
    with pytest.raises(ValueError):
        combined.compose(Circuit((Register("other", 3),)))


def test_depth_counts_idle_wires_and_shared_controls():
    registers = (Register("data", 5),)
    assert estimate_resources(Circuit(registers)).depth == 0
    gates = (Gate("cx", (0, 1)), Gate("x", (2,)), Gate("cx", (0, 3)), Gate("ccx", (1, 2, 3)))
    report = estimate_resources(Circuit(registers, gates))
    assert (report.logical_qubits, report.total_gates, report.depth) == (5, 4, 3)
    assert report.gate_counts == {"x": 1, "cx": 2, "ccx": 1}


def test_inputs_are_snapshotted():
    wires = [0]
    gates = [Gate("x", wires)]
    circuit = Circuit([Register("data", 1)], gates)
    wires.clear()
    gates.clear()
    assert circuit.evaluate_basis(0) == 1
    with pytest.raises(FrozenInstanceError):
        circuit.gates = ()


@pytest.mark.parametrize("width", [0, -1, True, 1.5])
def test_invalid_width(width):
    with pytest.raises(ValueError):
        register_xor(width)


@pytest.mark.parametrize("name, wires", [
    ("swap", (0, 1)), ("x", (0, 1)), ("ccx", (0, 1)), ("cx", (1, 1)),
    ("ccx", (0, 1, 0)), ("x", (-1,)), ("x", (True,)), ("x", (0.5,)),
])
def test_invalid_gate(name, wires):
    with pytest.raises(ValueError):
        Gate(name, wires)


def test_invalid_layouts():
    with pytest.raises(ValueError):
        Circuit(())
    with pytest.raises(ValueError):
        register_xor(1, source="target")
    with pytest.raises(ValueError):
        Register("", 1)
    with pytest.raises(ValueError):
        Circuit((Register("data", 1),), (Gate("x", (1,)),))


@pytest.mark.parametrize("order", [(), (1,), (0, 0), (False, 1), (-1, 0)])
def test_invalid_permutation(order):
    with pytest.raises(ValueError):
        bit_permutation(order)


@pytest.mark.parametrize("value", [-1, 4, 1.5, False])
def test_invalid_basis_index(value):
    with pytest.raises(ValueError):
        register_xor(1).evaluate_basis(value)

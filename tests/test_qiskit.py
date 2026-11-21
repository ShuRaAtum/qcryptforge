import pytest

from qcf import Circuit, Gate, Register, aes_add_round_key, estimate_resources, register_xor
from qcf.backends.qiskit import to_qiskit

pytest.importorskip("qiskit")
import numpy as np
from qiskit.quantum_info import Operator, Statevector


@pytest.mark.parametrize("circuit", [
    register_xor(2),
    Circuit((Register("data", 3),), (Gate("x", (2,)), Gate("ccx", (2, 0, 1)), Gate("cx", (1, 0)))),
])
def test_operator_matches_basis_permutation(circuit):
    size = 1 << circuit.width
    expected = np.zeros((size, size))
    for value in range(size):
        expected[circuit.evaluate_basis(value), value] = 1
    exported = to_qiskit(circuit)
    np.testing.assert_allclose(Operator(exported).data, expected)
    np.testing.assert_allclose(Operator(to_qiskit(circuit.inverse())).data, expected.T)
    np.testing.assert_allclose(Operator(exported.compose(exported.inverse())).data, np.eye(size))


def test_relative_phase_and_entanglement():
    # Source in (|0> + i|1>)/sqrt(2), target in |0>.
    initial = Statevector(np.array([1, 0, 1j, 0]) / np.sqrt(2))
    circuit = to_qiskit(register_xor(1))
    output = initial.evolve(circuit)
    np.testing.assert_allclose(output.data, np.array([1, 0, 0, 1j]) / np.sqrt(2))
    np.testing.assert_allclose(output.evolve(circuit.inverse()).data, initial.data)


def test_aes_export_without_statevector():
    circuit = aes_add_round_key()
    qc = to_qiskit(circuit)
    assert [(r.name, r.size) for r in qc.qregs] == [("state", 128), ("round_key", 128)]
    assert qc.num_qubits == 256
    assert qc.depth() == estimate_resources(circuit).depth
    assert qc.count_ops() == {"cx": 128}
    for i, instruction in enumerate(qc.data):
        assert [qc.find_bit(q).index for q in instruction.qubits] == [128 + i, i]

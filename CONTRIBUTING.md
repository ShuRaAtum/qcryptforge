# Contributing circuits

Start a feature branch from the revision you intend to extend. Describe the primitive, parameter set, source specification, and any third-party code or design attribution in your pull request.

Give the register-by-register mathematical map, bit and byte order, gate ordering, valid inputs, ancilla initialization and cleanup, and inverse behavior. Use the backend-independent IR in the algorithm layer. Document any backend-specific limits in the adapter.

Compare the implementation against an independent reference. Exhaust small domains, include published intermediate values when available, and verify inverse behavior. Use phase-sensitive tests for circuits acting on superpositions. Verify large circuits structurally or with the basis evaluator. Include the gate set, scheduling assumptions, package versions, and any optimization settings alongside resource comparisons.

From the repository root, install the test environment and run the checks before opening a pull request.

```sh
python -m pip install '.[test,qiskit]'
python -m pytest -q
python examples/add_round_key.py
```

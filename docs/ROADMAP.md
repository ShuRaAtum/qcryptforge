# Development roadmap

## Implemented in 0.1.0a0

- Installable core, immutable reversible circuits, basis evaluation and inversion.
- Register XOR, bit permutations, AES AddRoundKey and logical resource counting.
- Optional Qiskit export and small-circuit statevector verification.

## Planned AES-128 milestones

1. Implement byte operations in the AES field modulo x⁸ + x⁴ + x³ + x + 1. Start with multiplication by x and check all 256 inputs and inverse round trips.
2. Select a reversible S-box design, document the workspace contract, and validate all 256 outputs and cleanup.
3. Add ShiftRows and MixColumns with reference checks for byte order and linear maps.
4. Build and validate key expansion, compose rounds, and compare complete encryption against published vectors. Verify restoration of workspace.
5. Compare alternative circuits using declared gate decompositions, widths and depths.

## Further research

OpenQASM 3 export requires semantic round-trip checks. Cirq, Qualtran, Q#, CUDA-Q and PennyLane are candidate adapters. Optimization passes require an equivalence test and a measured tradeoff. Candidate primitives include other AES key sizes, ARIA, Rijndael-256, SM4, Camellia, PRESENT, LowMC, SHA-2, Keccak, ChaCha20, Speck and selected arithmetic or hash components used in post-quantum schemes.

Oracle APIs are a separate research milestone. A proposal should identify the mathematical function, input, output and workspace, distinguish computation, bit marking and phase marking, and specify cleanup of intermediate results.

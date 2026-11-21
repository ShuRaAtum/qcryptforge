# Circuit conventions

A `Register(name, width)` reserves a positive number of wires. A `Circuit(registers, gates)` allocates registers contiguously in declaration order from wire zero. Within each register, bit zero is least significant. Global qubit `q` corresponds to bit `q` of the integer accepted by `evaluate_basis`. Qiskit displays the highest-index bit of a basis label on the left.

Gate names are lowercase. `Gate("cx", (control, target))` flips its target if the control is set. CCX requires both controls to be set. X flips unconditionally. Each maps basis states with amplitude +1 and extends linearly to superpositions. A circuit applies gates in tuple order. `a.compose(b)` applies a then b and requires identical ordered layouts. `inverse()` reverses the sequence of these self-inverse gates.

## Register operations

`register_xor(w)` allocates target then source. It maps the basis index `(source << w) | target` to `(source << w) | (target ^ source)`. Arbitrary initial register values are allowed. A second application restores both registers.

`bit_permutation(destinations)` sends input bit i to output bit destinations[i] on the same register. It decomposes cycles into swaps and emits three CX gates per swap. The inverse restores the original order. Identity permutations emit zero gates. Neither primitive allocates workspace.

## AES AddRoundKey

Wire `8*j + b` contains bit b of serialized state byte j. In FIPS 197 notation, j = 4 × column + row. The key uses the same mapping starting at wire 128. For the standard's hex strings, use `int.from_bytes(bytes.fromhex(hex_string), "little")`. AddRoundKey XORs corresponding bytes in place, preserves the supplied round key and is self-inverse. Tests compare the initial key addition against a published intermediate state. [FIPS 197, §5.1.4](https://csrc.nist.gov/pubs/fips/197/final) and [NIST AES-128 example, page 1](https://csrc.nist.gov/CSRC/media/Projects/Cryptographic-Standards-and-Guidelines/documents/examples/AES_Core128.pdf).

## AES multiplication by x

`aes_xtime()` maps an eight-qubit `data` register holding a field element a to x·a modulo x⁸ + x⁴ + x³ + x + 1. Wire i holds the coefficient of xⁱ. A cyclic left rotation moves the old high bit to wire zero. Three CX gates from that wire supply the remaining reduction terms at wires 1, 3 and 4. The implementation emits 24 CX gates with explicit swaps and uses no workspace. Its inverse multiplies by the field inverse of x. [FIPS 197, §4.2.1](https://csrc.nist.gov/pubs/fips/197/final).

## Resource measurement

`estimate_resources` counts each emitted X, CX or CCX once before transpilation. Width includes idle allocated wires. Each wire starts at layer zero. A gate occupies the layer after the maximum last-used layer of its operands, and all of those wires become busy at that layer. Depth is the last occupied layer. This assumes unit gate duration, all-to-all connectivity, and concurrency on disjoint wires.

Reports contain logical circuit resources only. T resources require an explicit decomposition. Physical costs additionally depend on hardware, routing, error correction and scheduling. For a reproducible comparison, record the QCF revision, input parameters, emitted gates, and any transpiler or optimization settings. The AddRoundKey example prints the unoptimized logical report and software environment.

## Qiskit adapter

`to_qiskit` constructs a QuantumCircuit with one QuantumRegister per QCF register. It emits the corresponding Qiskit gate for each instruction. Callers can use Qiskit's composition, inverse, drawing and statevector APIs. QCF supports this translation for its three IR gates. It has no importer, measurements or phase gates in the alpha IR. [Qiskit QuantumCircuit API](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.circuit.QuantumCircuit).

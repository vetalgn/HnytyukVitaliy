import random
import cirq


def setIoQubits(qubitCount):
    """Add the specified number of input and output qubits."""
    inputQubits = [cirq.GridQubit(i, 0) for i in range(qubitCount)]
    outputQubit = cirq.GridQubit(qubitCount, 0)
    return (inputQubits, outputQubit)


def makeOracle(inputQubits, outputQubit, xBits):
    """Implement function {f(x) = 1 if x==x', f(x) = 0 if x!= x'}."""
    yield(cirq.X(q) for (q, bit) in zip(inputQubits, xBits) if not bit)
    yield(cirq.TOFFOLI(inputQubits[0], inputQubits[1], outputQubit))
    yield(cirq.X(q) for (q, bit) in zip(inputQubits, xBits) if not bit)


def makeGroverCircuit(inputQubits, outputQubit, oracle):
    """Find the value recognized by the oracle in sqrt(N) attempts."""
    c = cirq.Circuit()

    c.append([
        cirq.X(outputQubit),
        cirq.H(outputQubit),
        cirq.H.on_each(*inputQubits),
    ])

    c.append(oracle)

    c.append(cirq.H.on_each(*inputQubits))
    c.append(cirq.X.on_each(*inputQubits))
    c.append(cirq.H.on(inputQubits[1]))
    c.append(cirq.CNOT(inputQubits[0], inputQubits[1]))
    c.append(cirq.H.on(inputQubits[1]))
    c.append(cirq.X.on_each(*inputQubits))
    c.append(cirq.H.on_each(*inputQubits))

    c.append(cirq.measure(*inputQubits, key='result'))

    return c


def bitstring(bits):
    return ''.join(str(int(b)) for b in bits)


def main():
    qubitCount = int(input("Count of qubits = "))
    circuitSampleCount = int(input("Circuits count = "))

    (inputQubits, outputQubit) = setIoQubits(qubitCount)

    bits = [int(input("bit = ")) for _ in range(qubitCount)]
    xBits = []
    for x in bits:
        if x > 0 :
           xBits.append(1);
        else :
           xBits.append(0);
    print('Secret bit sequence: {}'.format(xBits))

    oracle = makeOracle(inputQubits, outputQubit, xBits)

    circuit = makeGroverCircuit(inputQubits, outputQubit, oracle)
    print('Circuit:')
    print(circuit)

    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions = circuitSampleCount)

    frequencies = result.histogram(key='result', fold_func = bitstring)
    print('Sampled results:\n{}'.format(frequencies))

    mostCommonBitstring = frequencies.most_common(1)[0][0]
    print('Most common bitstring: {}'.format(mostCommonBitstring))
    print('Found a match: {}'.format(
        mostCommonBitstring == bitstring(xBits)))


if __name__ == '__main__':
    main()

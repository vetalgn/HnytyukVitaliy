import cirq
import numpy as np


# Simple one qubit
print("Simple one qubits:")
qubit = cirq.GridQubit(0, 0)

circuit = cirq.Circuit.from_ops(
    cirq.X(qubit)**0.5, 
    cirq.measure(qubit, key='m')
)
print("Circuit:")
print(circuit)

simulator = cirq.Simulator()
result = simulator.run(circuit, repetitions=20)
print("Results:")
print(result)
print()


# Simple multy qubits
print("Simple multy qubits:")
length = 3

qubits = [cirq.GridQubit(i, j) for i in range(length) for j in range(length)]
print(qubits)
print()


# Place of qubits
print("Place of qubits:")
print("Length 10 line on Bristlecone:")
line = cirq.google.line_on_device(cirq.google.Bristlecone, length=10)
print(line)

print("Initial circuit:")
n = 10
depth = 2
circuit = cirq.Circuit.from_ops(
    cirq.SWAP(cirq.LineQubit(j), cirq.LineQubit(j + 1))
    for i in range(depth)
    for j in range(i % 2, n - 1, 2)
)
circuit.append(cirq.measure(*cirq.LineQubit.range(n), key='all'))
print(circuit)

print()
print("Xmon circuit:")
translated = cirq.google.optimized_for_xmon(
    circuit=circuit,
    new_device=cirq.google.Bristlecone,
    qubit_map=lambda q: line[q.x])
print(translated)
print()


# Bell Inequality
print("Bell Inequality:")
def makeBellTestCircuit():
    alice = cirq.GridQubit(0, 0)
    bob = cirq.GridQubit(1, 0)
    aliceReferee = cirq.GridQubit(0, 1)
    bobReferee = cirq.GridQubit(1, 1)

    circuit = cirq.Circuit()

    circuit.append([
        cirq.H(alice),
        cirq.CNOT(alice, bob),
        cirq.X(alice)**-0.25,
    ])

    circuit.append([
        cirq.H(aliceReferee),
        cirq.H(bobReferee),
    ])

    circuit.append([
        cirq.CNOT(aliceReferee, alice)**0.5,
        cirq.CNOT(bobReferee, bob)**0.5,
    ])

    circuit.append([
        cirq.measure(alice, key='a'),
        cirq.measure(bob, key='b'),
        cirq.measure(aliceReferee, key='x'),
        cirq.measure(bobReferee, key='y'),
    ])

    return circuit


def bitstring(bits):
    return ''.join('1' if e else '_' for e in bits)

circuit = makeBellTestCircuit()
print('Circuit:')
print(circuit)

print()
repetitions = 100
print('Simulating {} repetitions...'.format(repetitions))
result = cirq.Simulator().run(program=circuit, repetitions=repetitions)

a = np.array(result.measurements['a'][:, 0])
b = np.array(result.measurements['b'][:, 0])
x = np.array(result.measurements['x'][:, 0])
y = np.array(result.measurements['y'][:, 0])
outcomes = a ^ b == x & y
winPercent = len([e for e in outcomes if e]) * 100 / repetitions

print()
print('Results')
print('a:', bitstring(a))
print('b:', bitstring(b))
print('x:', bitstring(x))
print('y:', bitstring(y))
print('(a XOR b) == (x AND y):\n  ', bitstring(outcomes))
print('Win rate: {}%'.format(winPercent))









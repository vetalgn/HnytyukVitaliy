import numpy as np
import cirq


def makeQuantumTeleportationCircuit(ranX, ranY):
    circuit = cirq.Circuit()
    msg, alice, bob = cirq.LineQubit.range(3)

    circuit.append([cirq.H(alice), cirq.CNOT(alice, bob)])
    circuit.append([cirq.X(msg)**ranX, cirq.Y(msg)**ranY])
    circuit.append([cirq.CNOT(msg, alice), cirq.H(msg)])
    circuit.append(cirq.measure(msg, alice))
    circuit.append([cirq.CNOT(alice, bob), cirq.CZ(msg, bob)])

    return circuit

def main():
    ranX = float(input('X = '))
    ranY = float(input('Y = '))
    circuit = makeQuantumTeleportationCircuit(ranX, ranY)

    print("Circuit:")
    print(circuit)

    sim = cirq.Simulator()

    q0, q1 = cirq.LineQubit.range(2)

    message = sim.simulate(cirq.Circuit.from_ops(
        [cirq.X(q0)**ranX, cirq.Y(q1)**ranY]))

    print("\nBloch Sphere of Message After X and Y Gates:")
    b0X, b0Y, b0Z = cirq.bloch_vector_from_state_vector(
        message.final_state, 0)
    print("x: ", np.around(b0X, 4),
          "y: ", np.around(b0Y, 4),
          "z: ", np.around(b0Z, 4))

    final_results = sim.simulate(circuit)

    print("\nBloch Sphere of Qubit 2 at Final State:")
    b2X, b2Y, b2Z = cirq.bloch_vector_from_state_vector(
        final_results.final_state, 2)
    print("x: ", np.around(b2X, 4),
          "y: ", np.around(b2Y, 4),
          "z: ", np.around(b2Z, 4))


if __name__ == '__main__':
    main()

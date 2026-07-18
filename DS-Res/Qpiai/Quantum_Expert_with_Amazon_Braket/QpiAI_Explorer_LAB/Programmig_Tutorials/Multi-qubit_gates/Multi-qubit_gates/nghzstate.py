# circuit to create an n-qubit GHZ state

import braket

#import relevant functions
from braket.circuits import Circuit
from braket.devices import LocalSimulator

def create_n_ghz_state(n):

    #initialize circuit

    circuit = Circuit()

    #put the first qubit in a uniform superposition of |0> and |1> state

    circuit.h(0)
    
    #performing cnot operations on subsequent qubits produces an n-qubit GHZ state

    for i in range(1,n):
        circuit.cnot(i-1,i)
    
    return circuit
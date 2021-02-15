"""
This module defines a circuit simulator. Ideally the strategy pattern should be implemented over here,
in which case the Calculation strategy and measurement straegy also states would be injected to it rather then the circuit selecting them.
But for now this will suffice.

Example for using this simulator:


from Factory import *
from Entities import *
from simulatorCircuit import SimulatorCircuit

simulator = SimulatorCircuit()

print("Program for suprposition of all states")

my_qpu = simulator.initialize(3)

my_h_circuit = [
    { "gate": "U3", "params": { "theta": 1.5708, "phi": 0, "lambda": -3.1415 }, "target": 0 }, #h gate
    { "gate": "U3", "params": { "theta": 1.5708, "phi": 0, "lambda": -3.1415 }, "target": 1 }, #h gate
    { "gate": "U3", "params": { "theta": 1.5708, "phi": 0, "lambda": -3.1415 }, "target": 2 }  #h gate
    ]

final_state = simulator.run(my_qpu, my_h_circuit)

simulator.measure(final_state, 1000)

"""

from Factory import *
from Base import *

class SimulatorCircuit(CircuitBase):
    """
    This class is a classical simulator of a quantum circuit.
    """

    def initialize(self, num_qubits: int):
        self.__total_qubits = num_qubits

        state = States.create("Classical")
        state.set_to_ground_state(num_qubits)
        
        print("initial state: %s" %state.get_vector())
        
        return state


    def run(self, initial_state: StateBase, program):
        calculator = Calculators.create("Numpy")
        
        #Iterated over each program line and updates the state
        for operation in program:
            operator = self.__get_operator(operation)
            operator_matrix = operator.matrix(self.__total_qubits, **operation)
            calculator.calculate_state(operator_matrix, initial_state)
        return initial_state


    def measure(self, final_state: StateBase, num_shots : int):
        measuring_unit = Measurements.create("Simulated")
        measurements = {}
        
        #Taking 'num_shots' shots of measurement and printing the result
        for i in range(num_shots):
            measurement = measuring_unit.measure_state(final_state, self.__total_qubits)
            if measurement not in measurements:
                measurements[measurement] = 1
            else:
                measurements[measurement] += 1
        print("final state: %s" %final_state.get_vector())
        print("results: %s" %measurements)
        
        return measurements

    def __get_operator(self, operation):
        operator = Operators.create(operation["gate"],  **operation["params"])
        return operator


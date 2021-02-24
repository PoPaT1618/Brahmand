"""
This module defines a circuit. It is implemented as a part of strategy pattern, in which 
the Calculation strategy and states would be injected to it.

Example for using this as a classical simulator:


from Factory import *
from Entities import *
from Circuit import Circuit

simulator = Circuit("Classical", "Numpy")

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

class Circuit(CircuitBase):
    """
    This class is a classical simulator of a quantum circuit.
    """

    def __init__(self, state_type: str, calculator_type: str):
        """ Constructor """
        self.__state_type = state_type
        self.__calculator = Calculators.create(calculator_type)
        self.__total_qubits = 2 #Default number qubits
        
        

    def initialize(self, num_qubits: int):
       try:
            self.__total_qubits = num_qubits
            state = States.create(self.__state_type)

            state.set_to_ground_state(num_qubits)
                   
            print("initial state: %s" %state.get_vector())
                   
            return state

       except KeyError as e:
            print(e)


    def run(self, initial_state: StateBase, program):
        try:
            if initial_state is None:
                raise TypeError("Error: initial_state is of NoneType.")
            if program is None:
                raise TypeError("Error: program is of NoneType.")
                    
            #Iterated over each program line and updates the state
            for operation in program:
                self.__calculator.calculate_state(initial_state, self.__total_qubits, **operation)

            return initial_state

        except KeyError as e:
            print(e)
        except TypeError as e:
            print(e)


    def measure(self, final_state: StateBase, num_shots : int):
        try:
            if final_state is None:
                raise TypeError("Error: final_state is of NoneType.")
            if num_shots is None:
                raise TypeError("Error: num_shots is of NoneType.")

            measurements = self.__calculator.measure_state(final_state, num_shots, self.__total_qubits)
            
            print("final state: %s" %final_state.get_vector())
            print("results: %s" %measurements)
                    
            return measurements

        except KeyError as e:
            print(e)
        except TypeError as e:
            print(e)

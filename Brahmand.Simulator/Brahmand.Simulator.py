"""
This module tests the simulation circuit.
"""

from Factory import *
from Entities import *
from Circuit import Circuit

from datetime import timedelta
import datetime

simulator = Circuit("Classical", "Numpy")


"""Program 1"""

print("Program 1: Testing H gate")

my_qpu = simulator.initialize(3)

my_h_circuit = [
    { "gate": "U3", "params": { "theta": 1.5708, "phi": 0, "lambda": -3.1415 }, "target": 0 }, #h gate
    { "gate": "U3", "params": { "theta": 1.5708, "phi": 0, "lambda": -3.1415 }, "target": 1 }, #h gate
    { "gate": "U3", "params": { "theta": 1.5708, "phi": 0, "lambda": -3.1415 }, "target": 2 }  #h gate
    ]

final_state = simulator.run(my_qpu, my_h_circuit)

simulator.measure(final_state, 1000)


"""Program 2"""

print("\n\nProgram 2: Testing CX or CNOT gate")

my_qpu = simulator.initialize(4)

my_cx_circuit = [
    { "gate": "U3", "params": { "theta": 3.1415, "phi": 1.5708, "lambda": -3.1415 }, "target": 3 }, #x gate
    { "gate": "CU", "params": { "theta": 3.1415, "phi": 1.5708, "lambda": -3.1415 }, "control": 3, "target": 1 } #cx gate
    ]

final_state = simulator.run(my_qpu, my_cx_circuit)

simulator.measure(final_state, 1000)


"""Program 3"""

print("\n\nProgram 3: Circuit for swapping q0 with q2")

datetimeFormat = '%Y-%m-%d %H:%M:%S.%f'
start_time = datetime.datetime.now().strftime(datetimeFormat)


my_qpu = simulator.initialize(8)
my_swap_circuit = [
    #initial state |00000000>
    { "gate": "U3", "params": { "theta": 3.1415, "phi": 1.5708, "lambda": -3.1415 }, "target": 0 }, #x gate
    #updated state |10000000>
    { "gate": "CU", "params": { "theta": 3.1415, "phi": 1.5708, "lambda": -3.1415 }, "control": 0, "target": 2 }, #cx gate
    { "gate": "CU", "params": { "theta": 3.1415, "phi": 1.5708, "lambda": -3.1415 }, "control": 2, "target": 0 }, #cx gate
    { "gate": "CU", "params": { "theta": 3.1415, "phi": 1.5708, "lambda": -3.1415 }, "control": 0, "target": 2 } #cx gate
    #final swapped state |00100000>
    ]
final_state = simulator.run(my_qpu, my_swap_circuit)
simulator.measure(final_state, 1000)


end_time = datetime.datetime.now().strftime(datetimeFormat)
diff = datetime.datetime.strptime(end_time, datetimeFormat) - datetime.datetime.strptime(start_time, datetimeFormat)
print("Time taken:", diff)
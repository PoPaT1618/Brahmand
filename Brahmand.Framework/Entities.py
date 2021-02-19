"""
This module contains different entity classes derived from bases classes defined in base module.
Entity classes are regitered to their corresponding factories using decorator methods defined in those factories.

For example: U operator class is registered to 'Operators' factory.

from Base import *
from Factory import *

@Operators.register("U3")
class U(OperatorBase):

"""

from Base import *
from Factory import *
from numpy import random
import numpy as np


"""Operators"""

@Operators.register("U3")
class U(OperatorBase):
    """
    This class defines the most generic single qubit quantum gate.
    It accepts theta, phi and lambda parameters and creates the operator matrix based on it.
    Different operators such as X, Y, Z, I, S, T, H, etc can be created using this class.
    """

    def __init__(self, **kwargs):
        """ Constructor """
        super().__init__(**kwargs)
        self.__operator = super()._get_operator()

    def matrix(self, total_qubits: int, **kwargs):
        """Returns operator matrix with big endian encoding"""
        
        target_qubit = kwargs.get('target', None)
        if target_qubit is None:
            raise KeyError("Error: target not found.")

        I = np.identity(2)
        matrix = I
        
        #big endian encoding
        for i in range(total_qubits):
            if target_qubit == i:
                if i == 0:
                    matrix = self.__operator
                else:
                    matrix = np.kron(matrix, self.__operator)
            elif i == 0:
                continue
            else:
                matrix = np.kron(matrix, I)
        return matrix


@Operators.register("CU")
class CU(OperatorBase):
    """
    This class defines the most generic two qubits control quantum gate (CU).
    It accepts theta, phi and lambda parameters and creates the operator matrix based on it.
    Different operators such as CX, CU etc can be created using this class.
    """

    #Projector matrices. For more scalability projector base and entities can be defined.
    __p0x0 = np.array([[1, 0],[0, 0]])
    __p1x1 = np.array([[0, 0],[0, 1]])
    
    __I = np.identity(2) #Identity matrix

    def __init__(self, **kwargs):
        """ Constructor """
        super().__init__(**kwargs)
        self.__operator = super()._get_operator()

    def matrix(self, total_qubits: int, **kwargs):
        """Returns operator matrix with big endian encoding"""

        control_qubit = kwargs.get('control', None) # control qubit
        target_qubit = kwargs.get('target', None) # target qubit

        if control_qubit is None:
            raise KeyError("Error: control not found.")
        if target_qubit is None:
            raise KeyError("Error: target not found.")
        
        operator_matrix = (self.__calculate_operator(total_qubits, control_qubit, self.__p0x0,
                                             target_qubit, self.__I) + 
                    self.__calculate_operator(total_qubits, control_qubit, self.__p1x1,
                                              target_qubit, self.__operator))

        return operator_matrix

    def __calculate_operator(self, total_qubits: int, control: int, projector, target: int, operator):
        """Calculates operation matrix with big endian encoding"""
        matrix = self.__I

        def __update_matrix(matrix, index: int, operating_matrix):
            if index == 0:
                matrix = operating_matrix
            else:
                matrix = np.kron(matrix, operating_matrix)
            return matrix
        
        #big endian encoding
        for i in range(total_qubits):
            if control == i:
                matrix = __update_matrix(matrix, i, projector)
            elif target == i:
                matrix = __update_matrix(matrix, i, operator)
            elif i == 0:
                continue
            else:
                matrix = np.kron(matrix, self.__I)
        return matrix


"""States"""


@States.register("Classical")
class ClassicalState(StateBase):
    """
    This class defines generic classical state with 'n' number of qubits.
    """

    __groundState = np.array([1, 0])
    __state = np.array([])
    __qubits = {}

    def set_to_ground_state(self, num_qubits: int):
        self.__qubits.clear()
        for i in range(num_qubits):
            self.__qubits[i] = self.__groundState
            if i == 0:
                self.__state = self.__qubits[i]
            else:
                self.__state = np.kron(self.__state, self.__qubits[i])

    def get_vector(self):
        return self.__state

    def update_vector(self, state):
        self.__state = state

    def get_probability_vector(self):
        #This can be improved or optimized.
        probabilities = np.absolute(self.__state) 
        probabilities /= probabilities.sum() #Normalizing so that values add upto 1.
        return probabilities


"""Calculation Strategies"""


@Calculators.register("Numpy")
class NumpyCalculator(CalculatorBase):

    def calculate_state(self, operator_matrix, state: StateBase):
        psi = np.dot(state.get_vector(), operator_matrix)
        state.update_vector(psi)
        return state


"""Measurement Strategies"""


@Measurements.register("Simulated")
class SimulatedMeasurements(MeasurementBase):
    """
    This class simulates quantum measurement.
    """

    def measure_state(self, final_state: StateBase, total_qubits: int):
        # Note: This logic can be improved by modelling the quantum measurement using operation-sum representation.
        # Not sure how random.choice works, but it is suffice for now.
        sampleSpace = []
        for i in range(2**total_qubits):
            sampleSpace.append("%s" % np.binary_repr(i, total_qubits))
        measurement = random.choice(sampleSpace, p=final_state.get_probability_vector())
        return measurement


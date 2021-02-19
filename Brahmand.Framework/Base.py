"""
This module contains different base classes for entities such as operator, state, measurement, etc.
These classes can be derived by various entity classes and those classes can be regitered to their corresponding factories 
using decorator methods defined in those factories.

If someone wants to definee new entities, he/she can define those entities in a different module 
by simply importing this and the factory module.

For example: U operator class is registered to 'Operators' factory.

from Base import *
from Factory import *

@Operators.register("U3")
class U(OperatorBase):

"""

from abc import ABCMeta
from abc import abstractmethod
from typing import Callable
import numpy as np

class FactoryBase(metaclass=ABCMeta):
    """Base class for all self registering factory classes"""

    @abstractmethod
    def register(self, name: str) -> Callable:
        """Method for registering various products to the internal collection of products"""
        pass

    @abstractmethod
    def create(self, name: str, **kwargs)-> Callable:
        """Method for creating instance of product based on name parameter"""
        pass

    @classmethod
    def _inner_create(cls, name: str, **kwargs):
        """Protected method that creates instance of the mentioned product"""
        if name not in cls._products:
            raise KeyError("Error: %s not found." %name)

        product_class = cls._products[name]
        product = product_class(**kwargs)
        return product



class OperatorBase(metaclass=ABCMeta):
    """Base class for all types of operators, for example: U3, CU, CCU, etc."""
    
    def __init__(self, **kwargs):
        """ Constructor: stores theta, phi and lambda parameters which are later used for creating U3 operator """
        self._theta = kwargs.get('theta', None)
        self._phi = kwargs.get('phi', None)
        self._lambda = kwargs.get('lambda', None)

        if self._theta is None:
            raise KeyError("Error: theta not found.")
        if self._theta is None:
            raise KeyError("Error: phi not found.")
        if self._theta is None:
            raise KeyError("Error: lambda not found.")

    @abstractmethod
    def matrix(self, total_qubits: int, **kwargs):
        """Method for returning operator matrix."""
        pass

    def _get_operator(self):
        """Protected method which creates the U3 operator based on theta, phi anf lambda parameters."""
        operator = np.array([
            [np.cos(self._theta/2), (-1) * np.exp(complex(0,self._lambda)) * np.sin(self._theta/2)],
            [np.exp(complex(0,self._phi)) * np.sin(self._theta/2), np.exp(complex(0,self._lambda + self._phi)) *  np.cos(self._theta/2)]
            ])
        return operator



class StateBase(metaclass=ABCMeta):
    """Base class for all types of states, for example: classical, quantum, etc."""

    def __init__(self, **kwargs):
        """ Constructor """

    @abstractmethod
    def set_to_ground_state(self, num_qubits: int):
        """Method that initializes or resets the state to ground state such as [1,0,0,0] for 2 qubit system."""
        pass

    @abstractmethod
    def get_vector(self):
        """Method that returns the state vector or array such as [0,1,0,0] for 2 qubit system."""
        pass

    @abstractmethod
    def update_vector(self, state):
        """Method that updates the state with provided array."""
        pass

    @abstractmethod
    def get_probability_vector(self):
        """Method that returns the probability of each element in the state vector."""
        pass



class CalculatorBase(metaclass=ABCMeta):
    """
    Base class for all types of calculation strategies, for example: numpy strategy, optimized strategy, etc.
    
    Note: Further methods can be added which are frequently used in calculations 
          and a optimized version can be written for them.
    """

    def __init__(self, **kwargs):
        """ Constructor """

    @abstractmethod
    def calculate_state(self, operator_matrix, state: StateBase):
        """Method that calculates the state based on operation matrix and updates the state accordingly."""
        pass



class MeasurementBase(metaclass=ABCMeta):
    """Base class for all types of measurement strategies, for example: classical/simulated measurement strategy, 
    quantum measurement strategy, etc."""

    def __init__(self, **kwargs):
        """ Constructor """

    @abstractmethod
    def measure_state(self, final_state: StateBase, total_qubits: int):
        """Method that measures the final state of the circuit and returns the result."""
        pass



class CircuitBase(metaclass=ABCMeta):
    """Base class for all types of circuits, for example: simulated circuit, quantum circuit, etc."""

    def __init__(self, **kwargs):
        """ Constructor """

    @abstractmethod
    def initialize(self, num_qubits: int):
        """Method that returns the ground state with mentioned number of qubits."""
        pass

    @abstractmethod
    def run(self, initial_state: StateBase, program):
        """
        Method that returns the final state after exceuting the circuit program on the mentioned initial state.
        
        Program example: 
        
        my_cx_circuit = [
        { "gate": "U3", "params": { "theta": 3.1415, "phi": 1.5708, "lambda": -3.1415 }, "target": 3 }, #x gate
        { "gate": "CU", "params": { "theta": 3.1415, "phi": 1.5708, "lambda": -3.1415 }, "control": 3, "target": 1 } #cx gate
        ]

        """
        pass

    @abstractmethod
    def measure(self, final_state: StateBase, num_shots : int):
        """Method that returns the result of multi-shot measurement of the final state."""
        pass
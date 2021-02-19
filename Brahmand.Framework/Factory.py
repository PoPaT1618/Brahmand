"""
This module contains different factories derived from FactoryBase,
which are used to collect all entities. These factories are self-registering i.e. 
there is no need to modify these factories while add new entity to the framework.

For reference: https://medium.com/@geoffreykoh/implementing-the-factory-pattern-via-dynamic-registry-and-python-decorators-479fc1537bbe
"""

from typing import Callable
from Base import *

class Operators(FactoryBase):
    """Factory for operators"""
    _products = {}

    @classmethod
    def register(cls, name: str) -> Callable:
        """Class method for registering operators to the internal collection of products"""
        def inner(wrapped_class: OperatorBase) -> Callable:
            if name not in cls._products:
                cls._products[name] = wrapped_class
            return wrapped_class
        return inner

    @classmethod
    def create(cls, name: str, **kwargs) -> 'OperatorBase':
        """Class method for creating instance of operator based on name parameter"""
        return cls._inner_create(name, **kwargs)


class States(FactoryBase):
    """Factory for states. States could be classical or quantum, etc."""
    _products = {}

    @classmethod
    def register(cls, name: str) -> Callable:
        """Class method for registering states to the internal collection of products"""
        def inner(wrapped_class: StateBase) -> Callable:
            if name not in cls._products:
                cls._products[name] = wrapped_class
            return wrapped_class
        return inner

    @classmethod
    def create(cls, name: str, **kwargs) -> 'StateBase':
        """Class method for creating instance of state based on name parameter"""
        return cls._inner_create(name, **kwargs)


class Calculators(FactoryBase):
    """Factory for calculators"""
    _products = {}

    @classmethod
    def register(cls, name: str) -> Callable:
        """Class method for registering calculators to the internal collection of products"""
        def inner(wrapped_class: CalculatorBase) -> Callable:
            if name not in cls._products:
                cls._products[name] = wrapped_class
            return wrapped_class
        return inner

    @classmethod
    def create(cls, name: str, **kwargs) -> 'CalculatorBase':
        """Class method for creating instance of calculator based on name parameter"""
        return cls._inner_create(name, **kwargs)

class Measurements(FactoryBase):
    """Factory for measuring techniques"""
    _products = {}

    @classmethod
    def register(cls, name: str) -> Callable:
         """Class method for registering various measuring techniques to the internal collection of products"""
         def inner(wrapped_class: MeasurementBase) -> Callable:
             if name not in cls._products:
                 cls._products[name] = wrapped_class
             return wrapped_class
         return inner

    @classmethod
    def create(cls, name: str, **kwargs) -> 'MeasurementBase':
        """Class method for creating instance of measuring techinique based on name parameter"""
        return cls._inner_create(name, **kwargs)
 
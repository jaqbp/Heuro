from abc import ABC, abstractmethod
import numpy as np


class TestFunction(ABC):
    def __init__(self, lb: list, ub: list, dim: int, name: str):
        self.lb = lb[:]
        self.ub = ub[:]
        self.dim = dim
        self.name = name

    @abstractmethod
    def fobj(self, x):
        """
        Abstrakcyjna metoda obliczająca wartość funkcji testowej dla danego wektora x.
        Powinna być zaimplementowana w każdej konkretnej funkcji testowej.
        """
        pass

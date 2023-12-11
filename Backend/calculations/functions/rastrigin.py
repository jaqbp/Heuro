from functions.base import TestFunction
import numpy as np


class RastriginFunction(TestFunction):
    def __init__(self, lb, ub, dim):
        super().__init__(lb, ub, dim, "Rastrigin")

    def fobj(self, x):
        return 10 * len(x) + sum(x**2 - 10 * np.cos(2 * np.pi * x))

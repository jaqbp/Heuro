from functions.base import TestFunction
import numpy as np

# bukin = TestFunction(lb=np.array([-15, -3]), ub=np.array([-5, 3]), dim=2, bukin_function_n6, "bukin")


class RastriginFunction(TestFunction):
    def __init__(self, lb, ub, dim):
        super().__init__(lb, ub, dim, "Rastrigin")

    def fobj(self, x):
        term1 = 100 * np.sqrt(np.abs(x[1] - 0.01 * x[0] ** 2))
        term2 = 0.01 * np.abs(x[0] + 10)
        return term1 + term2

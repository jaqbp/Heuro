 from functions.base import TestFunction

class HimmelblauFunction(TestFunction):
    def __init__(self, lb, ub, dim):
        super().__init__(lb, ub, dim, "Himmelblau")

    # X must be of size 2, dim = 2
    def fobj(self, X: tuple[float, float]) -> float:
        term1 = (X[0]**2 + X[1] - 11)**2
        term2 = (X[0] + X[1]**2 - 7)**2
        return term1 + term2


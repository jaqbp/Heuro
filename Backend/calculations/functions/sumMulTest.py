 from functions.base import TestFunction

class SumMulTestFunction(TestFunction):
    def __init__(self, lb, ub, dim):
        super().__init__(lb, ub, dim, "SumMulTest")

    def fobj(self, X: tuple[float, float]) -> float:
      return sum(abs(X)) + np.prod(abs(X))
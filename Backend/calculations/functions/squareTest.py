 from functions.base import TestFunction

class SquareTestFunction(TestFunction):
    def __init__(self, lb, ub, dim):
        super().__init__(lb, ub, dim, "SquareTest")

    def fobj(self, X: tuple[float, float]) -> float:
      return sum(X**2)
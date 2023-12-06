from functions.base import TestFunction

class RosenbrockFunction(TestFunction):
    def __init__(self, lb, ub, dim):
        super().__init__(lb, ub, dim, "Rosenbrock")

    def fobj(self, X: tuple[float, float]) -> float:
      sum = 0
      for i in range(len(X) - 1):
        sum += 100 * (X[i + 1] - X[i] ** 2) ** 2 + (1 - X[i]) ** 2
      return sum
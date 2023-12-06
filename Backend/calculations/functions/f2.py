 from functions.base import TestFunction

class F2Function(TestFunction):
    def __init__(self, lb, ub, dim):
        super().__init__(lb, ub, dim, "F2")

    def fobj(self, X: tuple[float, float]) -> float:
      return sum(-1 * x * np.sin(abs(x) ** 0.5))
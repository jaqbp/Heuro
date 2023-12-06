 from functions.base import TestFunction

class F3Function(TestFunction):
    def __init__(self, lb, ub, dim):
        super().__init__(lb, ub, dim, "F3")

    def fobj(self, X: tuple[float, float]) -> float:
      a = 1
      for i in range(len(x)):
        if i != 0:
            a = a * np.cos(x[i] / (i**2))
      return 1 + (1 / 4000) * sum(x**2) - a
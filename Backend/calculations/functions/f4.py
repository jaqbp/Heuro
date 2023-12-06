from functions.base import TestFunction

class F4Function(TestFunction):
    def __init__(self, lb, ub, dim):
        super().__init__(lb, ub, dim, "F4")

    def fobj(self, X: tuple[float, float]) -> float:
      return (
        -20 * np.exp(-0.02 * len(x) ** -1 * sum(x**2))
        - np.exp(len(x) ** -1 * sum(np.cos(2 * np.pi * x)))
        + 20
        + np.exp(1)
      )
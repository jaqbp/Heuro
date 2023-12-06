from functions.base import TestFunction

class BukinFunction(TestFunction):
    def __init__(self, lb, ub, dim):
        super().__init__(lb, ub, dim, "Bukin")
        
    def fobj(self, X: tuple[float, float]) -> float:
      term1 = 100 * np.sqrt(np.abs(X[1] - 0.01 * X[0] ** 2))
      term2 = 0.01 * np.abs(X[0] + 10)
      return term1 + term2
from functions.base import TestFunction

class F1Function(TestFunction):
    def __init__(self, lb, ub, dim):
        super().__init__(lb, ub, dim, "F1")

    def fobj(self, X: tuple[float, float]) -> float:
        return sum((x - 0.5) ** 2)
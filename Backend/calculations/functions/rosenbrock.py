from functions.base import TestFunction


class Rosenbrock(TestFunction):
    def __init__(self, lb, ub, dim):
        super().__init__(lb, ub, dim, "Rosenbrock")

    def fobj(self, x):
        sum = 0
        for i in range(len(x) - 1):
            sum += 100 * (x[i + 1] - x[i] ** 2) ** 2 + (1 - x[i]) ** 2
        return sum

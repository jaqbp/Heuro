from abc import ABC, abstractmethod


class TestFunction(ABC):
    def __init__(self, lb: list, ub: list, dim: int, name: str):
        self.lb = lb[:]
        self.ub = ub[:]
        self.dim = dim
        self.name = name

    @abstractmethod
    def fobj(self, x):
        """
        Abstrakcyjna metoda obliczająca wartość funkcji testowej dla danego wektora x.
        Powinna być zaimplementowana w każdej konkretnej funkcji testowej.
        """
        pass

# def squareTest(X):
#     return sum(X**2)
# 
# 
# def sumMulTest(X):
#     return sum(abs(X)) + np.prod(abs(X))
# 
# 
# def rosenbrock(X):
#     sum = 0
#     for i in range(len(X) - 1):
#         sum += 100 * (X[i + 1] - X[i] ** 2) ** 2 + (1 - X[i]) ** 2
#     return sum
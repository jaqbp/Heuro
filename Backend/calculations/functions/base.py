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


# TODO: functions to add

# rosenbrock = TestFunction(lb=np.array([-5]), ub=np.array([5]), dim=30, rosenbrock, "rosenbrock")
# bukin = TestFunction(lb=np.array([-15, -3]), ub=np.array([-5, 3]), dim=2, bukin_function_n6, "bukin")

# def rosenbrock(X):
#     sum = 0
#     for i in range(len(X) - 1):
#         sum += 100 * (X[i + 1] - X[i] ** 2) ** 2 + (1 - X[i]) ** 2
#     return sum

# def bukin_function_n6(X):
#     term1 = 100 * np.sqrt(np.abs(X[1] - 0.01 * X[0] ** 2))
#     term2 = 0.01 * np.abs(X[0] + 10)
#     return term1 + term2

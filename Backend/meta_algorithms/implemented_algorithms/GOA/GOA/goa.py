# zaimplementować pierwszy algorytm w oparciu o klase abstrakcyjną (import classes)
from goa_code import GOA2
from abstract_classes import *


# test function
def rastrigin(X):
    return 10 * len(X) + sum(X**2 - 10 * np.cos(2 * np.pi * X))


# test function class
class TestFunction:
    def __init__(self, lb: int, ub: int, dim: int, fobj, name: str):
        self.lb = lb[:]
        self.ub = ub[:]
        self.dim = dim
        self.fobj = fobj
        self.name = name


class GazelleOptimizationAlgorithm(IOptimizationAlgorithm):
    def __init__(self):
        super().__init__()
        self.name = "Gazelle Optimization Algorithm"

    def solve(self, fitness_function, search_agents_no, max_iter):
        # Dostosowanie do wymagań interfejsu
        # self.test_function.fobj = fitness_function
        # self.test_function.lb = domain[0]
        # self.test_function.ub = domain[1]
        # self.test_function.dim = len(domain[0])

        self.fbest, self.xbest = GOA2(search_agents_no, max_iter, fitness_function)

        return self.fbest


if __name__ == "__main__":
    rastrigin = TestFunction(
        np.array([-5.12]), np.array([5.12]), 30, rastrigin, "rastrigin"
    )
    GOA_Inst = GazelleOptimizationAlgorithm()
    print(GOA_Inst.solve(rastrigin, 10, 100))

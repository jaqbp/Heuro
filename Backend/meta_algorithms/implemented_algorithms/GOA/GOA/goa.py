# zaimplementować pierwszy algorytm w oparciu o klase abstrakcyjną (import classes)
from goa_code import GOA2
from abstract_classes import *


class GazelleOptimizationAlgorithm(IOptimizationAlgorithm):
    def __init__(self, search_agents_no, max_iter, test_function):
        super().__init__()
        self.name = "Gazelle Optimization Algorithm"
        self.search_agents_no = search_agents_no
        self.max_iter = max_iter
        self.test_function = test_function
        self.xbest = None
        self.fbest = float("inf")
        self.number_of_evaluation_fitness_function = 0

    def solve(self, fitness_function, domain, parameters):
        # Dostosowanie do wymagań interfejsu
        self.test_function.fobj = fitness_function
        self.test_function.lb = domain[0]
        self.test_function.ub = domain[1]
        self.test_function.dim = len(domain[0])

        self.fbest, self.xbest = GOA2(
            self.search_agents_no, self.max_iter, self.test_function
        )

        self.number_of_evaluation_fitness_function = ...

        return self.fbest


if __name__ == "__main__":
    GOA_Inst = GazelleOptimizationAlgorithm(50, 20, 3)
    print(GOA_Inst.name)

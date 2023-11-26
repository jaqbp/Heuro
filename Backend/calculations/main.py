from algorithms.goa import GOA
from functions.rastrigin import RastriginFunction
from functions.himmelblau import HimmelblauFunction
import numpy as np


def main():
    test_function = HimmelblauFunction(lb=np.array([-5.12]), ub=np.array([5.12]), dim=10)
    goa_algorithm = GOA(SearchAgents_no=20, Max_iter=10)

    best_fitness, best_position = goa_algorithm.solve(
        test_function, domain=[test_function.lb, test_function.ub], parameters=[]
    )
    print("Best Fitness: ", best_fitness)
    print("Best Position: ", best_position)


if __name__ == "__main__":
    main()

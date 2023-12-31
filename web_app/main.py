from algorithms.goa import GOA
from functions.himmelblau import HimmelblauFunction
from functions.rosenbrock import RosenbrockFunction
import numpy as np


def main():
    # test_function = RastriginFunction(lb=np.array([-5.12]), ub=np.array([5.12]), dim=10)
    rosenbrock = RosenbrockFunction(np.array([-5]), np.array([5]), 5)
    test_function = HimmelblauFunction(np.array([-5]), np.array([5]), 5)
    goa_algorithm = GOA(SearchAgents_no=20, Max_iter=10)

    best_fitness, best_position = goa_algorithm.solve(
        test_function, parameters=[0.34, 0.88]
    )
    print("Best Fitness: ", best_fitness)
    print("Best Position: ", best_position)


if __name__ == "__main__":
    main()

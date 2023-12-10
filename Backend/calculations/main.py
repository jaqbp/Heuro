from algorithms.goa import GOA
from functions.himmelblau import HimmelblauFunction
import numpy as np


def main():
    # test_function = RastriginFunction(lb=np.array([-5.12]), ub=np.array([5.12]), dim=10)
    test_function = HimmelblauFunction(np.array([-5]), np.array([5]), 3)
    goa_algorithm = GOA(SearchAgents_no=20, Max_iter=10)

    # for test
    # if os.path.exists("GOA.txt"):
    #     os.remove("GOA.txt")

    best_fitness, best_position = goa_algorithm.solve(
        test_function,
        domain=[test_function.lb, test_function.ub],
        parameters=[0.34, 0.88],
    )
    print("Best Fitness: ", best_fitness)
    print("Best Position: ", best_position)


if __name__ == "__main__":
    main()

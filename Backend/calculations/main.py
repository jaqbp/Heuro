from algorithms.goa import GOA
from functions.rastrigin import RastriginFunction


def main():
    test_function = RastriginFunction(lb=[-5.12], ub=[5.12], dim=10)
    goa_algorithm = GOA(SearchAgents_no=30, Max_iter=1000, test_function=test_function)

    best_fitness, best_position = goa_algorithm.solve(
        test_function.fobj, domain=[test_function.lb, test_function.ub], parameters=[]
    )
    print("Best Fitness: ", best_fitness)
    print("Best Position: ", best_position)


if __name__ == "__main__":
    main()

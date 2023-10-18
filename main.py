import numpy as np
import numpy.matlib
from scipy.special import gamma
from functions import (
    rastrigin,
    sumMulTest,
    squareTest,
    rosenbrock,
    bukin_function_n6,
    himmelblau,
)
import math
import csv
import pandas as pd


def levy(n, m, beta):
    num = gamma(1 + beta) * np.sin(np.pi * beta / 2)  # Used for Numerator
    den = gamma((1 + beta) / 2) * beta * 2 ** ((beta - 1) / 2)  # Used for Denominator

    sigma_u = (num / den) ** (1 / beta)  # Standard deviation

    u = np.random.normal(0, sigma_u, (n, m))
    v = np.random.normal(0, 1, (n, m))

    z = u / (np.abs(v) ** (1 / beta))

    return z


def initialization(SearchAgents_no, dim, ub, lb):
    # Initialize an array to hold positions
    Positions = np.zeros((SearchAgents_no, dim))
    # If the boundaries of all variables are equal
    if len(ub) == 1 and len(lb) == 1:
        Positions = np.random.rand(SearchAgents_no, dim) * (ub - lb) + lb
    else:
        # If each variable has different lb and ub
        for i in range(dim):
            ub_i = ub[i]
            lb_i = lb[i]
            Positions[:, i] = np.random.rand(SearchAgents_no) * (ub_i - lb_i) + lb_i

    return Positions


def GOA2(SearchAgents_no, Max_iter, test_function):
    dim = test_function.dim
    Top_gazelle_pos = np.zeros(dim)
    Top_gazelle_fit = np.inf
    # Convergence_curve = np.zeros(Max_iter)
    stepsize = np.zeros((SearchAgents_no, dim))
    fitness = np.inf * np.ones(SearchAgents_no)

    gazelle = initialization(SearchAgents_no, dim, test_function.ub, test_function.lb)
    Xmin = np.tile(np.ones(dim) * test_function.lb, (SearchAgents_no, 1))
    Xmax = np.tile(np.ones(dim) * test_function.ub, (SearchAgents_no, 1))

    Iter = 0
    PSRs = 0.34
    S = 0.88
    s = np.random.rand()

    while Iter < Max_iter:
        for i in range(gazelle.shape[0]):
            Flag4ub = gazelle[i, :] > test_function.ub
            Flag4lb = gazelle[i, :] < test_function.lb
            gazelle[i, :] = (
                (gazelle[i, :] * ~(Flag4ub + Flag4lb))
                + test_function.ub * Flag4ub
                + test_function.lb * Flag4lb
            )
            fitness[i] = test_function.fobj(gazelle[i, :])

            if fitness[i] < Top_gazelle_fit:
                Top_gazelle_fit = fitness[i]
                Top_gazelle_pos = gazelle[i, :]

        if Iter == 0:
            fit_old = fitness.copy()
            Prey_old = gazelle.copy()

        Inx = fit_old < fitness
        Indx = np.tile(Inx[:, np.newaxis], (1, dim))
        gazelle = Indx * Prey_old + ~Indx * gazelle
        fitness = Inx * fit_old + ~Inx * fitness

        fit_old = fitness.copy()
        Prey_old = gazelle.copy()

        Elite = np.tile(Top_gazelle_pos, (SearchAgents_no, 1))
        CF = (1 - Iter / Max_iter) ** (2 * Iter / Max_iter)
        RL = 0.05 * levy(SearchAgents_no, dim, 1.5)
        RB = np.random.randn(SearchAgents_no, dim)

        for i in range(gazelle.shape[0]):
            for j in range(gazelle.shape[1]):
                R = np.random.rand()
                r = np.random.rand()
                if Iter % 2 == 0:
                    mu = -1
                else:
                    mu = 1

                if r > 0.5:
                    stepsize[i, j] = RB[i, j] * (Elite[i, j] - RB[i, j] * gazelle[i, j])
                    gazelle[i, j] = gazelle[i, j] + s * R * stepsize[i, j]
                else:
                    if i > gazelle.shape[0] / 2:
                        stepsize[i, j] = RB[i, j] * (
                            RL[i, j] * Elite[i, j] - gazelle[i, j]
                        )
                        gazelle[i, j] = Elite[i, j] + S * mu * CF * stepsize[i, j]
                    else:
                        stepsize[i, j] = RL[i, j] * (
                            Elite[i, j] - RL[i, j] * gazelle[i, j]
                        )
                        gazelle[i, j] = gazelle[i, j] + S * mu * R * stepsize[i, j]

        for i in range(gazelle.shape[0]):
            Flag4ub = gazelle[i, :] > test_function.ub
            Flag4lb = gazelle[i, :] < test_function.lb
            gazelle[i, :] = (
                (gazelle[i, :] * ~(Flag4ub + Flag4lb))
                + test_function.ub * Flag4ub
                + test_function.lb * Flag4lb
            )
            fitness[i] = test_function.fobj(gazelle[i, :])

            if fitness[i] < Top_gazelle_fit:
                Top_gazelle_fit = fitness[i]
                Top_gazelle_pos = gazelle[i, :]

        if Iter == 0:
            fit_old = fitness.copy()
            Prey_old = gazelle.copy()

        Inx = fit_old < fitness
        Indx = np.tile(Inx[:, np.newaxis], (1, dim))
        gazelle = Indx * Prey_old + ~Indx * gazelle
        fitness = Inx * fit_old + ~Inx * fitness

        fit_old = fitness.copy()
        Prey_old = gazelle.copy()

        if np.random.rand() < PSRs:
            U = np.random.rand(SearchAgents_no, dim) < PSRs
            gazelle = gazelle + CF * (
                (Xmin + np.random.rand(SearchAgents_no, dim) * (Xmax - Xmin)) * U
            )
        else:
            r = np.random.rand()
            Rs = gazelle.shape[0]
            stepsize = (PSRs * (1 - r) + r) * (
                gazelle[np.random.permutation(Rs), :]
                - gazelle[np.random.permutation(Rs), :]
            )

        Iter = Iter + 1
        # Convergence_curve[Iter - 1] = Top_gazelle_fit

    return Top_gazelle_fit, Top_gazelle_pos  # Convergence_curve


# Algorithms to test the heuristic:


class TestFunction:
    def __init__(self, lb: int, ub: int, dim: int, fobj, name: str):
        self.lb = lb[:]
        self.ub = ub[:]
        self.dim = dim
        self.fobj = fobj
        self.name = name


class GazelleOptimizationAlgorithm:
    name: str
    x_best: float
    f_best: float
    number_of_evaluation_fitness_function: int

    def __init__(self):
        self.name = "Gazelle Optimization Algorithm"

    def solve(self) -> float:
        pass


if __name__ == "__main__":
    test_functions = []
    rastrigin = TestFunction(
        np.array([-5.12]), np.array([5.12]), 30, rastrigin, "rastrigin"
    )
    rosenbrock = TestFunction(
        np.array([-5]), np.array([5]), 30, rosenbrock, "rosenbrock"
    )
    bukin = TestFunction(
        np.array([-15, -3]), np.array([-5, 3]), 2, bukin_function_n6, "bukin"
    )
    himmelblau = TestFunction(
        np.array([-5]), np.array([5]), 2, himmelblau, "himmelblau"
    )
    test_functions.append(rastrigin)
    test_functions.append(rosenbrock)
    test_functions.append(bukin)
    test_functions.append(himmelblau)

    # Params for heuristic algorithm (higher values == higher chance of finding better solution)
    N = [10, 20, 40, 80]
    I = [5, 10, 20, 40, 80]
    TESTS = 10

    # Dataframe to store our data in the table and then save it to excel file
    data = {
        "For function": [],
        "Number of params": [],
        "N": [],
        "I": [],
        "Found minimum": [],
        "Goal function value": [],
    }

    for test_func in test_functions:
        for n in N:
            for i in I:
                best_y = math.inf
                best_X = None
                for _ in range(TESTS):
                    y, X = GOA2(n, i, test_func)
                    if y < best_y:
                        best_y = y
                        best_X = X[:]
                data["For function"].append(test_func.name)
                data["Number of params"].append(test_func.dim)
                data["N"].append(n)
                data["I"].append(i)
                data["Found minimum"].append(best_X)
                data["Goal function value"].append(best_y)

                print(f"N: {n}, I: {i}\nbest_y: {best_y}\nbest_X: {best_X}\n\n")

    df = pd.DataFrame(data)
    df.to_excel("output.xlsx", index=False)
    print(df)

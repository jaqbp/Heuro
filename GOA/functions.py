import numpy as np


def rastrigin(X):
    return 10 * len(X) + sum(X**2 - 10 * np.cos(2 * np.pi * X))


def squareTest(X):
    return sum(X**2)


def sumMulTest(X):
    return sum(abs(X)) + np.prod(abs(X))


def rosenbrock(X):
    sum = 0
    for i in range(len(X) - 1):
        sum += 100 * (X[i + 1] - X[i] ** 2) ** 2 + (1 - X[i]) ** 2
    return sum


# X must be of size 2, dim = 2
def bukin_function_n6(X):
    term1 = 100 * np.sqrt(np.abs(X[1] - 0.01 * X[0] ** 2))
    term2 = 0.01 * np.abs(X[0] + 10)
    return term1 + term2


# X must be of size 2, dim = 2
def himmelblau(X):
    term1 = (X[0] ** 2 + X[1] - 11) ** 2
    term2 = (X[0] + X[1] ** 2 - 7) ** 2
    return term1 + term2


def f1(x):
    return sum((x - 0.5) ** 2)


def f2(x):  # global -418.9829 * n
    return sum(-1 * x * np.sin(abs(x) ** 0.5))


def f3(x):
    a = 1
    for i in range(len(x)):
        if i != 0:
            a = a * np.cos(x[i] / (i**2))
    return 1 + (1 / 4000) * sum(x**2) - a


def f4(x):
    return (
        -20 * np.exp(-0.02 * len(x) ** -1 * sum(x**2))
        - np.exp(len(x) ** -1 * sum(np.cos(2 * np.pi * x)))
        + 20
        + np.exp(1)
    )

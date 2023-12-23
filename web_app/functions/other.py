# Czy te funkcje są potrzebne?

import numpy as np

def squareTest(X):
    return sum(X**2)

def sumMulTest(X):
    return sum(abs(X)) + np.prod(abs(X))

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

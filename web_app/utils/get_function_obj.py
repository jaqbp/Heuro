from functions.base import TestFunction
from functions.himmelblau import HimmelblauFunction
from functions.rosenbrock import RosenbrockFunction
from functions.bukin import BukinFunction
from functions.rastrigin import RastriginFunction
from functions.taskAA.ObjectiveFunction import ObjectiveFunction
from typing import Callable, Optional

import numpy as np


test_function_callbacks: list[Callable[[Optional[int]], TestFunction]] = [
    lambda dimension=30: RastriginFunction(
        np.array([-5.12]), np.array([5.12]), dimension
    ),
    lambda dimension=2: BukinFunction(
        np.array([-15, -3]), np.array([-5, 3]), dimension
    ),
    lambda dimension=30: RosenbrockFunction(np.array([-5]), np.array([5]), dimension),
    lambda dimension=2: HimmelblauFunction(np.array([-5]), np.array([5]), dimension),
]


def get_function_obj(dimension: int, domain: int, id: int) -> TestFunction:
    if id == 4:
        try:
            from dll.custom_function import TestFunction  # type: ignore

            print("loaded dll")
            return TestFunction(
                -np.array([domain]), np.array([domain]), dimension, "Custom function"
            )
        except ModuleNotFoundError as e:
            print(e)
    elif id == 5:
        return ObjectiveFunction(np.array([0.5]), np.array([1.5]), 3)
    return test_function_callbacks[id](dimension)

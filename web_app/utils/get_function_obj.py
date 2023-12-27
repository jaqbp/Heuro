from functions.base import TestFunction
from functions.himmelblau import HimmelblauFunction
from functions.rosenbrock import RosenbrockFunction
from functions.bukin import BukinFunction
from functions.rastrigin import RastriginFunction
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
    # TODO: add domain
    return test_function_callbacks[id](dimension)

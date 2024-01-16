import numpy as np
cimport numpy as np

cdef class TestFunction:
    cdef public np.ndarray lb
    cdef public np.ndarray ub
    cdef public int dim
    cdef public str name

    def __init__(self, np.ndarray lb, np.ndarray ub, int dim, str name):
        self.lb = lb[:]
        self.ub = ub[:]
        self.dim = dim
        self.name = name

    def fobj(self, np.ndarray x):
        return sum(x**4)
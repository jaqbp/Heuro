import math

import numpy as np

from FunkcjaCelu12 import FunkcjaCelu12
from Transformator12 import Transformator12


class ObjectiveFunction:
    def __init__(self):
        self.n = 401
        self.deltaT = 0.00005

        self.omega = 100 * math.pi
        self.alpha = 2.0 * math.pi / 3.0
        self.wsp = math.sin(7.5 * math.pi / 180.0) / math.sin(52.5 * math.pi / 180.0)
        self.uabc = np.zeros((self.n, 3))

        self.t12 = Transformator12(self.n)
        self.u = np.zeros((6, self.n))
        self.t = 0

        self.t12.R = 15

        self.GenerujNapiecieSieci2(100.0, 100.0, 100.0, 1.5, 2.3, 1.2, 2.2, 0.5, 1.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)

        for i in range(self.n):
            self.u[0, i] = self.uabc[i][0]
            self.u[1, i] = self.uabc[i][1]
            self.u[2, i] = self.uabc[i][2]
            self.u[3, i] = self.u[0, i] / math.sqrt(3.0)
            self.u[4, i] = self.u[1, i] / math.sqrt(3.0)
            self.u[5, i] = self.u[2, i] / math.sqrt(3.0)
            self.t += self.deltaT

        self.a = [0.5, 0.5, 0.5]
        self.b = [1.5, 1.5, 1.5]

        self.FunkcjaCelu = FunkcjaCelu12(self.u, 401, self.t12, self.deltaT)

    def GenerujNapiecieSieci2(self, *param: float) -> None:
        t = 0.0
        # res = "" # unused
        for i in range(self.n):
            self.uabc[i] = [
                param[0] * math.sin(self.omega * t)
                + param[3] * math.sin(2 * (self.omega * t + param[9]))
                + param[4] * math.sin(3 * (self.omega * t + param[10]))
                + param[5] * math.sin(5 * (self.omega * t + param[11]))
                + param[6] * math.sin(7 * (self.omega * t + param[12]))
                + param[7] * math.sin(11 * (self.omega * t + param[13]))
                + param[8] * math.sin(13 * (self.omega * t + param[14])),
                param[1] * math.sin(self.omega * t + self.alpha)
                + param[3] * math.sin(2 * (self.omega * t + param[9]))
                + param[4] * math.sin(3 * (self.omega * t + param[10]))
                + param[5] * math.sin(5 * (self.omega * t + param[11] + self.alpha))
                + param[6] * math.sin(7 * (self.omega * t + param[12] + self.alpha))
                + param[7] * math.sin(11 * (self.omega * t + param[13] + self.alpha))
                + param[8] * math.sin(13 * (self.omega * t + param[14] + self.alpha)),
                param[2] * math.sin(self.omega * t + 2.0 * self.alpha)
                + param[3] * math.sin(2 * (self.omega * t + param[9]))
                + param[4] * math.sin(3 * (self.omega * t + param[10]))
                + param[5]
                * math.sin(5 * (self.omega * t + param[11] + 2.0 * self.alpha))
                + param[6]
                * math.sin(7 * (self.omega * t + param[12] + 2.0 * self.alpha))
                + param[7]
                * math.sin(11 * (self.omega * t + param[13] + 2.0 * self.alpha))
                + param[8]
                * math.sin(13 * (self.omega * t + param[14] + 2.0 * self.alpha)),
            ]
            t += self.deltaT

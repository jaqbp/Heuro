import math

import numpy as np

from Transformator12 import Transformator12


class FunkcjaCelu12:
    def __init__(self, u: np.ndarray, n: int, t12: Transformator12, deltaT: float):
        self.R25 = 15
        self.R75 = 25

        self.t12 = t12
        self.pierwiastek = math.sqrt(3.0)

        self.u = u
        self.n = n
        self.deltaT = deltaT

    def WartoscSkuteczna(self, v: list[float], krok: float) -> float:
        n = len(v)
        s = sum(val**2 for val in v)
        return math.sqrt(s / n)

    def DrukujWSkuteczne(self, x: list[float]) -> str:
        napis = ""
        # v = self.Wartosc(x) # unused
        pK = np.zeros((6, self.n))
        p = self.t12.Prady

        for i in range(6):
            for j in range(self.n):
                pK[i][j] = p[j, i]

        for i in range(6):
            napis += f"{i} {self.WartoscSkuteczna(pK[i], self.deltaT)}"
            napis += "\n"
        return napis

    def Wartosc2(self) -> float:
        wU = 0.0
        if self.t12.R > self.R75:
            wU = 1.0
        elif self.t12.R > self.R25:
            wU = (self.t12.R - self.R25) / (self.R75 - self.R25)

        wI = 1.0 - wU

        v = self.t12.Symulacja(self.u, self.n)
        p = self.t12.Prady

        pierw3 = math.sqrt(3)

        p0 = np.zeros(self.n)
        p1 = np.zeros(self.n)
        p2 = np.zeros(self.n)
        p3 = np.zeros(self.n)
        p4 = np.zeros(self.n)
        p5 = np.zeros(self.n)

        suma = 0.0
        for i in range(self.n):
            p0[i] = p[i, 0]
            p1[i] = p[i, 1]
            p2[i] = p[i, 2]
            p3[i] = p[i, 3]
            p4[i] = p[i, 4]
            p5[i] = p[i, 5]

        suma += abs(
            self.WartoscSkuteczna(p1, self.deltaT)
            - self.WartoscSkuteczna(p0, self.deltaT)
        )
        suma += abs(
            self.WartoscSkuteczna(p2, self.deltaT)
            - self.WartoscSkuteczna(p0, self.deltaT)
        )
        suma += abs(
            self.WartoscSkuteczna(p2, self.deltaT)
            - self.WartoscSkuteczna(p1, self.deltaT)
        )
        suma += abs(
            self.WartoscSkuteczna(p4, self.deltaT)
            - self.WartoscSkuteczna(p3, self.deltaT)
        )
        suma += abs(
            self.WartoscSkuteczna(p5, self.deltaT)
            - self.WartoscSkuteczna(p3, self.deltaT)
        )
        suma += abs(
            self.WartoscSkuteczna(p5, self.deltaT)
            - self.WartoscSkuteczna(p4, self.deltaT)
        )

        suma += abs(
            pierw3
            - self.WartoscSkuteczna(p3, self.deltaT)
            / self.WartoscSkuteczna(p0, self.deltaT)
        )
        suma += abs(
            pierw3
            - self.WartoscSkuteczna(p4, self.deltaT)
            / self.WartoscSkuteczna(p1, self.deltaT)
        )
        suma += abs(
            pierw3
            - self.WartoscSkuteczna(p5, self.deltaT)
            / self.WartoscSkuteczna(p2, self.deltaT)
        )

        min_val = v[0]
        max_val = v[0]
        for i in range(1, self.n):
            if min_val > v[i]:
                min_val = v[i]
            elif max_val < v[i]:
                max_val = v[i]
        return wU * (max_val - min_val) + wI * suma

    def Wartosc(self, *x: float) -> float:
        for i in range(3):
            for j in range(self.n):
                self.u[i + 3, j] = x[i] * self.u[i, j] / self.pierwiastek
        return self.Wartosc2()

    def V(self, *x: float) -> float:
        for i in range(3):
            for j in range(self.n):
                self.u[i + 3, j] = x[i] * self.u[i, j] / self.pierwiastek
        return self.t12.Symulacja(self.u, self.n)

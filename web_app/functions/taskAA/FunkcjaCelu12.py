import math


class FunkcjaCelu12:
    def __init__(self, u, n, t12, deltaT):
        self.R25 = 15
        self.R75 = 25
        self.t12 = t12
        self.pierwiastek = math.sqrt(3.0)
        self.u = u
        self.n = n
        self.deltaT = deltaT

    def WartoscSkuteczna(self, v, krok):
        n = len(v)
        s = sum(val**2 for val in v)
        return math.sqrt(s / n)

    def DrukujWSkuteczne(self, x):
        napis = ""
        v = self.Wartosc(x)
        pK = [[] for _ in range(6)]
        p = self.t12.Prady

        for i in range(6):
            pK[i] = [p[j][i] for j in range(self.n)]

        for i in range(6):
            napis += f"{i} {self.WartoscSkuteczna(pK[i], self.deltaT)}"
            napis += "\n"
        return napis

    def Wartosc(self):
        wU = 0.0
        if self.t12.R > self.R75:
            wU = 1.0
        elif self.t12.R > self.R25:
            wU = (self.t12.R - self.R25) / (self.R75 - self.R25)

        wI = 1.0 - wU

        v = self.t12.Symulacja(self.u, self.n)
        p = self.t12.Prady

        pierw3 = math.sqrt(3)

        p0 = [p[i][0] for i in range(self.n)]
        p1 = [p[i][1] for i in range(self.n)]
        p2 = [p[i][2] for i in range(self.n)]
        p3 = [p[i][3] for i in range(self.n)]
        p4 = [p[i][4] for i in range(self.n)]
        p5 = [p[i][5] for i in range(self.n)]

        suma = 0.0
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

    def Wartosc(self, *x):
        for i in range(3):
            for j in range(self.n):
                self.u[i + 3, j] = x[i] * self.u[i, j] / self.pierwiastek
        return self.Wartosc()

    def V(self, *x):
        for i in range(3):
            for j in range(self.n):
                self.u[i + 3, j] = x[i] * self.u[i, j] / self.pierwiastek
        return self.t12.Symulacja(self.u, self.n)

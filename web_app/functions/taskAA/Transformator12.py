import numpy as np


class Transforamtor12:
    def __init__(self, n):
        self.iloscPulsow = 12
        self.blokowanie = 10_000.0
        self.przewodzenie = 0.01
        self.spadek = 0.5

        self.Rz = np.array([1.0, 1.0, 1.0, 0.33, 0.33, 0.33])
        self.R = 25.0

        self.d = np.zeros(12)
        self.a = np.zeros((8, 8))
        self.w = np.zeros(8)
        self.uD = np.zeros(12)
        self.i = np.zeros(6)
        self.v = None
        self.iloscKrokow = n
        self.prady = np.zeros((self.iloscKrokow, 6))

    @property
    def Prady(self):
        return self.prady

    @property
    def V(self):
        return self.v[7] if self.v is not None else None

    def GaussElimination(self, A, b, n):
        x = np.zeros(n)

        tmpA = np.zeros((n, n + 1))

        for i in range(n):
            tmpA[i, :n] = A[i, :]
            tmpA[i, n] = b[i]

        for k in range(n - 1):
            for i in range(k + 1, n):
                tmp = tmpA[i, k] / tmpA[k, k]
                tmpA[i, k:] -= tmp * tmpA[k, k:]

        for k in range(n - 1, -1, -1):
            tmp = np.dot(tmpA[k, k + 1 : n], x[k + 1 :])
            x[k] = (tmpA[k, n] - tmp) / tmpA[k, k]

        return x

    def LiczAdmitancje(self):
        self.a[0, 0] = 1 / self.Rz[3] + 1 / self.Rz[4] + 1 / self.Rz[5]
        self.a[0, 1:4] = -1 / self.Rz[3], -1 / self.Rz[4], -1 / self.Rz[5]

        self.a[1, 0] = -1 / self.Rz[3]
        self.a[1, 1] = 1 / self.Rz[3] + 1 / self.d[0] + 1 / self.d[1]
        self.a[1, 7] = -1 / self.d[0]

        self.a[2, 0] = -1 / self.Rz[4]
        self.a[2, 2] = 1 / self.Rz[4] + 1 / self.d[2] + 1 / self.d[3]
        self.a[2, 7] = -1 / self.d[2]

        self.a[3, 0] = -1 / self.Rz[5]
        self.a[3, 3] = 1 / self.Rz[5] + 1 / self.d[4] + 1 / self.d[5]
        self.a[3, 7] = -1 / self.d[4]

        self.a[4, 4] = 1 / self.Rz[0] + 1 / self.Rz[2] + 1 / self.d[6] + 1 / self.d[7]
        self.a[4, 5:8] = -1 / self.Rz[0], -1 / self.Rz[2], -1 / self.d[6]

        self.a[5, 4] = -1 / self.Rz[0]
        self.a[5, 5] = 1 / self.Rz[0] + 1 / self.Rz[1] + 1 / self.d[8] + 1 / self.d[9]
        self.a[5, 6] = -1 / self.Rz[1]
        self.a[5, 7] = -1 / self.d[8]

        self.a[6, 4] = -1 / self.Rz[2]
        self.a[6, 5] = -1 / self.Rz[1]
        self.a[6, 6] = 1 / self.Rz[2] + 1 / self.Rz[1] + 1 / self.d[10] + 1 / self.d[11]
        self.a[6, 7] = -1 / self.d[10]

        self.a[7, 1:8] = (
            -1 / self.d[0],
            -1 / self.d[2],
            -1 / self.d[4],
            -1 / self.d[6],
            -1 / self.d[8],
            -1 / self.d[10],
            1
            / (
                self.d[0]
                + self.d[2]
                + self.d[4]
                + self.d[6]
                + self.d[8]
                + self.d[10]
                + self.R
            ),
        )

    def LiczWymuszenia(self, u):
        self.w[0] = -u[3] / self.Rz[3] - u[4] / self.Rz[4] - u[5] / self.Rz[5]
        self.w[1:4] = u[3] / self.Rz[3], u[4] / self.Rz[4], u[5] / self.Rz[5]
        self.w[4] = u[0] / self.Rz[0] - u[2] / self.Rz[2]
        self.w[5:8] = (
            u[1] / self.Rz[1] - u[0] / self.Rz[0],
            u[2] / self.Rz[2] - u[1] / self.Rz[1],
        )

    def LiczUD(self, v):
        self.uD[0:12:2] = v[1:7:2] - v[7]
        self.uD[1:12:2] = -v[1:7:2]

    def Test(self):
        for i in range(self.iloscPulsow):
            if self.uD[i] > self.spadek and self.d[i] == self.blokowanie:
                return False
            elif self.uD[i] < 0.0 and self.d[i] == self.przewodzenie:
                return False
        return True

    def Iteracja(self, u):
        # zamkniecie wszystkich diod
        self.d[:] = self.blokowanie

        it = 0

        self.LiczAdmitancje()
        self.LiczWymuszenia(u)
        self.v = self.GaussElimination(self.a, self.w, 8)
        self.LiczUD(self.v)

        while not self.Test() and it <= self.iloscPulsow + 1:
            self.zmiana = False
            # sprawdzenie czy nie ma tu za dużo otwartych
            for i in range(self.iloscPulsow):
                if self.uD[i] < 0.0 and self.d[i] == self.przewodzenie:
                    self.d[i] = self.blokowanie
                    self.zmiana = True

            # wlaczanie najbardziej dodatnich
            if not self.zmiana:
                indeks = np.argmax(self.uD)
                # odblokowanie wszystkich z maksymalną wartością
                for i in range(self.iloscPulsow):
                    if (
                        np.abs(self.uD[i] - self.uD[indeks]) < 0.0001
                        and self.uD[i] > self.spadek
                    ):
                        self.d[i] = self.przewodzenie

                # nowe wyznaczenie Admintancji i Wymuszenia
                self.LiczAdmitancje()
                self.LiczWymuszenia(u)

                self.v = self.GaussElimination(self.a, self.w, 8)
                self.LiczUD(self.v)

    def LiczPrad(self, u, k):
        self.prady[k, 0] = (self.v[5] + u[0] - self.v[4]) / self.Rz[0]
        self.prady[k, 1] = (self.v[6] + u[1] - self.v[5]) / self.Rz[1]
        self.prady[k, 2] = (self.v[4] + u[2] - self.v[6]) / self.Rz[2]
        self.prady[k, 3] = (self.v[0] + u[3] - self.v[1]) / self.Rz[3]
        self.prady[k, 4] = (self.v[0] + u[4] - self.v[2]) / self.Rz[4]
        self.prady[k, 5] = (self.v[0] + u[5] - self.v[3]) / self.Rz[5]

    def Symulacja(self, u, n):
        vtmp = np.zeros(n)
        utk = np.zeros(6)
        for i in range(n):
            utk[0:6] = u[0:6, i]
            self.Iteracja(utk)
            vtmp[i] = self.V
            self.LiczPrad(utk, i)

        return vtmp

    def ZapiszPrady(self, plik):
        napis = ""
        for i in range(self.iloscKrokow):
            napis += f"{self.prady[i, 0]} "
            for j in range(1, 6):
                napis += f"{self.prady[i, j]} "
            napis += "\n"
        with open(plik, "w") as f:
            f.write(napis)

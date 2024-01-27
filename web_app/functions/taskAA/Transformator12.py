import numpy as np


class Transformator12:
    def __init__(self, n: int):
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
    def Prady(self) -> np.ndarray:
        return self.prady

    @property
    def V(self) -> float | None:
        return self.v[7] if self.v is not None else None

    def GaussElimination(self, A: np.ndarray, b: np.ndarray, n: int) -> float:
        x = np.zeros(n)

        tmpA = np.zeros((n, n + 1))

        for i in range(n):
            for j in range(n):
                tmpA[i, j] = A[i, j]
            tmpA[i, n] = b[i]

        tmp = 0.0

        for k in range(n - 1):
            for i in range(k + 1, n):
                tmp = tmpA[i, k] / tmpA[k, k]
                for j in range(k, n + 1):
                    tmpA[i, j] -= tmp * tmpA[k, j]

        for k in range(n - 1, -1, -1):
            tmp = 0
            for j in range(k + 1, n):
                tmp += tmpA[k, j] * x[j]
            x[k] = (tmpA[k, n] - tmp) / tmpA[k, k]

        return x

    def LiczAdmitancje(self) -> None:
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

        self.a[7, 1] = -1 / self.d[0]
        self.a[7, 2] = -1 / self.d[2]
        self.a[7, 3] = -1 / self.d[4]
        self.a[7, 4] = -1 / self.d[6]
        self.a[7, 5] = -1 / self.d[8]
        self.a[7, 6] = -1 / self.d[10]
        self.a[7, 7] = (
            1 / self.d[0]
            + 1 / self.d[2]
            + 1 / self.d[4]
            + 1 / self.d[6]
            + 1 / self.d[8]
            + 1 / self.d[10]
            + 1 / self.R
        )

    def LiczWymuszenia(self, u: np.ndarray) -> None:
        self.w[0] = -u[3] / self.Rz[3] - u[4] / self.Rz[4] - u[5] / self.Rz[5]
        self.w[1] = u[3] / self.Rz[3]
        self.w[2] = u[4] / self.Rz[4]
        self.w[3] = u[5] / self.Rz[5]
        self.w[4] = u[0] / self.Rz[0] - u[2] / self.Rz[2]
        self.w[5] = u[1] / self.Rz[1] - u[0] / self.Rz[0]
        self.w[6] = u[2] / self.Rz[2] - u[1] / self.Rz[1]
        self.w[7] = 0.0

    def LiczUD(self, v: np.ndarray) -> None:
        self.uD[0] = v[1] - v[7]
        self.uD[1] = -v[1]
        self.uD[2] = v[2] - v[7]
        self.uD[3] = -v[2]
        self.uD[4] = v[3] - v[7]
        self.uD[5] = -v[3]
        self.uD[6] = v[4] - v[7]
        self.uD[7] = -v[4]
        self.uD[8] = v[5] - v[7]
        self.uD[9] = -v[5]
        self.uD[10] = v[6] - v[7]
        self.uD[11] = -v[6]

    def Test(self) -> bool:
        for i in range(self.iloscPulsow):
            if self.uD[i] > self.spadek and self.d[i] == self.blokowanie:
                return False
            elif self.uD[i] < 0.0 and self.d[i] == self.przewodzenie:
                return False
        return True

    def Iteracja(self, u: np.ndarray) -> None:
        # zamkniecie wszystkich diod
        for i in range(self.iloscPulsow):
            self.d[i] = self.blokowanie

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
            it += 1

    def LiczPrad(self, u: np.ndarray, k: int) -> None:
        self.prady[k, 0] = (self.v[5] + u[0] - self.v[4]) / self.Rz[0]
        self.prady[k, 1] = (self.v[6] + u[1] - self.v[5]) / self.Rz[1]
        self.prady[k, 2] = (self.v[4] + u[2] - self.v[6]) / self.Rz[2]
        self.prady[k, 3] = (self.v[0] + u[3] - self.v[1]) / self.Rz[3]
        self.prady[k, 4] = (self.v[0] + u[4] - self.v[2]) / self.Rz[4]
        self.prady[k, 5] = (self.v[0] + u[5] - self.v[3]) / self.Rz[5]

    def Symulacja(self, u: np.ndarray, n: int) -> np.ndarray:
        vtmp = np.zeros(n)
        utk = np.zeros(6)
        for i in range(n):
            utk[0] = u[0, i]
            utk[1] = u[1, i]
            utk[2] = u[2, i]
            utk[3] = u[3, i]
            utk[4] = u[4, i]
            utk[5] = u[5, i]
            self.Iteracja(utk)
            vtmp[i] = self.V
            self.LiczPrad(utk, i)

        return vtmp

    def ZapiszPrady(self, plik: str) -> None:
        napis = ""
        for i in range(self.iloscKrokow):
            napis += f"{self.prady[i, 0]} "
            for j in range(1, 6):
                napis += f"{self.prady[i, j]} "
            napis += "\n"
        with open(plik, "w") as f:
            f.write(napis)

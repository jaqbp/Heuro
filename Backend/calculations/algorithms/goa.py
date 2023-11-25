import numpy as np
from scipy.special import gamma
from algorithms.base import IOptimizationAlgorithm


class GOA(IOptimizationAlgorithm):
    def __init__(self, SearchAgents_no, Max_iter):
        super().__init__()
        self.number_of_evaluation_fitness_function = 0
        self.SearchAgents_no = SearchAgents_no
        self.Max_iter = Max_iter

    def levy(self, n, m, beta):
        num = gamma(1 + beta) * np.sin(np.pi * beta / 2)
        den = gamma((1 + beta) / 2) * beta * 2 ** ((beta - 1) / 2)

        sigma_u = (num / den) ** (1 / beta)

        u = np.random.normal(0, sigma_u, (n, m))
        v = np.random.normal(0, 1, (n, m))

        z = u / (np.abs(v) ** (1 / beta))

        return z

    def initialization(self, SearchAgents_no, dim, ub, lb):
        Positions = np.zeros((SearchAgents_no, dim))
        if len(ub) == 1 and len(lb) == 1:
            Positions = np.random.rand(SearchAgents_no, dim) * (ub - lb) + lb
        else:
            for i in range(dim):
                ub_i = ub[i]
                lb_i = lb[i]
                Positions[:, i] = np.random.rand(SearchAgents_no) * (ub_i - lb_i) + lb_i

        return Positions

    def solve(self, fitness_function, domain, parameters):
        dim = fitness_function.dim

        self.xbest = np.zeros(dim)  # top_gazelle_pos
        self.fbest = np.inf  # top_gazelle_fitness
        stepsize = np.zeros((self.SearchAgents_no, dim))
        fitness = np.inf * np.ones(self.SearchAgents_no)

        gazelle = self.initialization(
            self.SearchAgents_no, dim, fitness_function.ub, fitness_function.lb
        )
        Xmin = np.tile(np.ones(dim) * fitness_function.lb, (self.SearchAgents_no, 1))
        Xmax = np.tile(np.ones(dim) * fitness_function.ub, (self.SearchAgents_no, 1))

        Iter = 0
        PSRs = 0.34
        S = 0.88
        s = np.random.rand()

        while Iter < self.Max_iter:
            for i in range(gazelle.shape[0]):
                Flag4ub = gazelle[i, :] > fitness_function.ub
                Flag4lb = gazelle[i, :] < fitness_function.lb
                gazelle[i, :] = (
                    (gazelle[i, :] * ~(Flag4ub + Flag4lb))
                    + fitness_function.ub * Flag4ub
                    + fitness_function.lb * Flag4lb
                )
                fitness[i] = fitness_function.fobj(gazelle[i, :])
                self.number_of_evaluation_fitness_function = (
                    self.number_of_evaluation_fitness_function + 1
                )
                if fitness[i] < self.fbest:
                    self.fbest = fitness[i]
                    self.xbest = gazelle[i, :]

            if Iter == 0:
                fit_old = fitness.copy()
                Prey_old = gazelle.copy()

            Inx = fit_old < fitness
            Indx = np.tile(Inx[:, np.newaxis], (1, dim))
            gazelle = Indx * Prey_old + ~Indx * gazelle
            fitness = Inx * fit_old + ~Inx * fitness

            fit_old = fitness.copy()
            Prey_old = gazelle.copy()

            Elite = np.tile(self.xbest, (self.SearchAgents_no, 1))
            CF = (1 - Iter / self.Max_iter) ** (2 * Iter / self.Max_iter)
            RL = 0.05 * self.levy(self.SearchAgents_no, dim, 1.5)
            RB = np.random.randn(self.SearchAgents_no, dim)

            for i in range(gazelle.shape[0]):
                for j in range(gazelle.shape[1]):
                    R = np.random.rand()
                    r = np.random.rand()
                    if Iter % 2 == 0:
                        mu = -1
                    else:
                        mu = 1

                    if r < 0.5:
                        stepsize[i, j] = RB[i, j] * (
                            Elite[i, j] - RB[i, j] * gazelle[i, j]
                        )
                        gazelle[i, j] = gazelle[i, j] + s * R * stepsize[i, j]
                    else:
                        if i > gazelle.shape[0] / 2:
                            stepsize[i, j] = RB[i, j] * (
                                RL[i, j] * Elite[i, j] - gazelle[i, j]
                            )
                            gazelle[i, j] = Elite[i, j] + S * mu * CF * stepsize[i, j]
                        else:
                            stepsize[i, j] = RL[i, j] * (
                                Elite[i, j] - RL[i, j] * gazelle[i, j]
                            )
                            gazelle[i, j] = gazelle[i, j] + S * mu * R * stepsize[i, j]

            for i in range(gazelle.shape[0]):
                Flag4ub = gazelle[i, :] > fitness_function.ub
                Flag4lb = gazelle[i, :] < fitness_function.lb
                gazelle[i, :] = (
                    (gazelle[i, :] * ~(Flag4ub + Flag4lb))
                    + fitness_function.ub * Flag4ub
                    + fitness_function.lb * Flag4lb
                )
                fitness[i] = fitness_function.fobj(gazelle[i, :])
                self.number_of_evaluation_fitness_function = (
                    self.number_of_evaluation_fitness_function + 1
                )
                if fitness[i] < self.fbest:
                    self.fbest = fitness[i]
                    self.xbest = gazelle[i, :]

            if Iter == 0:
                fit_old = fitness.copy()
                Prey_old = gazelle.copy()

            Inx = fit_old < fitness
            Indx = np.tile(Inx[:, np.newaxis], (1, dim))
            gazelle = Indx * Prey_old + ~Indx * gazelle
            fitness = Inx * fit_old + ~Inx * fitness

            fit_old = fitness.copy()
            Prey_old = gazelle.copy()

            if np.random.rand() < PSRs:
                U = np.random.rand(self.SearchAgents_no, dim) < PSRs
                gazelle = gazelle + CF * (
                    (Xmin + np.random.rand(self.SearchAgents_no, dim) * (Xmax - Xmin))
                    * U
                )
            else:
                r = np.random.rand()
                Rs = gazelle.shape[0]
                stepsize = (PSRs * (1 - r) + r) * (
                    gazelle[np.random.permutation(Rs), :]
                    - gazelle[np.random.permutation(Rs), :]
                )

            # self.writer.save_to_file_state_of_algorithm(
            #     "GOA",
            #     Iter,
            #     self.number_of_evaluation_fitness_function,
            #     gazelle,
            #     fitness,
            # )

            Iter = Iter + 1

        return self.fbest, self.xbest

from collections import defaultdict
import os
import numpy as np
from scipy.special import gamma
from algorithms.base import IOptimizationAlgorithm
from utils.state_management import StateWriter, StateReader
import math
import time


class GOA(IOptimizationAlgorithm):
    def __init__(self, SearchAgents_no, Max_iter):
        super().__init__()
        self.name = "Gazelle Optimization Algorithm"
        self.number_of_evaluation_fitness_function = 0
        self.SearchAgents_no = SearchAgents_no
        self.writer = StateWriter()
        self.reader = StateReader()
        self.Max_iter = Max_iter

    def _levy(self, n, m, beta):
        num = gamma(1 + beta) * np.sin(np.pi * beta / 2)
        den = gamma((1 + beta) / 2) * beta * 2 ** ((beta - 1) / 2)

        sigma_u = (num / den) ** (1 / beta)

        u = np.random.normal(0, sigma_u, (n, m))
        v = np.random.normal(0, 1, (n, m))

        z = u / (np.abs(v) ** (1 / beta))

        return z

    def _initialization(self, SearchAgents_no, dim, ub, lb):
        Positions = np.zeros((SearchAgents_no, dim))
        if len(ub) == 1 and len(lb) == 1:
            Positions = np.random.rand(SearchAgents_no, dim) * (ub - lb) + lb
        else:
            for i in range(dim):
                ub_i = ub[i]
                lb_i = lb[i]
                Positions[:, i] = np.random.rand(SearchAgents_no) * (ub_i - lb_i) + lb_i

        return Positions

    def solve(self, fitness_function, parameters: list[float]):
        domain = [fitness_function.lb, fitness_function.ub]
        filename = f"{fitness_function.name}_{self.SearchAgents_no}.txt"

        if os.path.exists(filename):
            (
                Iter,
                self.number_of_evaluation_fitness_function,
                self.SearchAgents_no,
                self.fbest,
                self.xbest,
            ) = self.reader.load_from_file_state_of_algorithm(filename)
            PSRs, S = parameters
            dim = fitness_function.dim
            self.xbest = self.xbest
            self.fbest = self.fbest
            stepsize = np.zeros((self.SearchAgents_no, dim))
            fitness = self.fbest * np.ones(self.SearchAgents_no)
            gazelle = np.tile(self.xbest, (self.SearchAgents_no, 1))
            Xmin = np.tile(np.ones(dim) * domain[0], (self.SearchAgents_no, 1))
            Xmax = np.tile(np.ones(dim) * domain[1], (self.SearchAgents_no, 1))
            s = np.random.rand()
            fit_old = self.fbest * np.ones(self.SearchAgents_no)
            Prey_old = np.tile(self.xbest, (self.SearchAgents_no, 1))
        else:
            PSRs, S = parameters
            dim = fitness_function.dim
            self.xbest = np.zeros(dim)
            self.fbest = np.inf
            stepsize = np.zeros((self.SearchAgents_no, dim))
            fitness = np.inf * np.ones(self.SearchAgents_no)
            gazelle = self._initialization(
                self.SearchAgents_no, dim, domain[1], domain[0]
            )
            Xmin = np.tile(np.ones(dim) * domain[0], (self.SearchAgents_no, 1))
            Xmax = np.tile(np.ones(dim) * domain[1], (self.SearchAgents_no, 1))

            Iter = 0
            s = np.random.rand()

        for i in range(gazelle.shape[0]):
            Flag4ub = gazelle[i, :] > domain[1]
            Flag4lb = gazelle[i, :] < domain[0]
            gazelle[i, :] = (
                (gazelle[i, :] * ~(Flag4ub + Flag4lb))
                + domain[1] * Flag4ub
                + domain[0] * Flag4lb
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
        RL = 0.05 * self._levy(self.SearchAgents_no, dim, 1.5)
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
                    stepsize[i, j] = RB[i, j] * (Elite[i, j] - RB[i, j] * gazelle[i, j])
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
            Flag4ub = gazelle[i, :] > domain[1]
            Flag4lb = gazelle[i, :] < domain[0]
            gazelle[i, :] = (
                (gazelle[i, :] * ~(Flag4ub + Flag4lb))
                + domain[1] * Flag4ub
                + domain[0] * Flag4lb
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
                (Xmin + np.random.rand(self.SearchAgents_no, dim) * (Xmax - Xmin)) * U
            )
        else:
            r = np.random.rand()
            Rs = gazelle.shape[0]
            stepsize = (PSRs * (1 - r) + r) * (
                gazelle[np.random.permutation(Rs), :]
                - gazelle[np.random.permutation(Rs), :]
            )

        Iter = Iter + 1
        self.writer.save_to_file_state_of_algorithm(self, Iter, filename)
        return self.xbest, self.fbest

    def calculate_function_data(
        self,
        fitness_function,
        parameters: list[float],
        numberOfTests: int,
        data=defaultdict(list),
    ):
        best_y = math.inf
        best_X = None
        curr_ys = []
        all_curr_X = []
        if os.path.exists("pause.txt"):
            os.remove("pause.txt")

        for _ in range(int(self.Max_iter)):
            X, y = self.solve(fitness_function, parameters)
            curr_ys.append(y)
            all_curr_X.append(X[:])
            if y < best_y:
                best_y = y
                best_X = X[:]
            while os.path.exists("pause.txt"):
                time.sleep(1)
                pass

        std_deviations_of_Xs = []
        stacked_Xs = np.vstack(all_curr_X)
        for j in range(stacked_Xs.shape[1]):
            std_dev = np.std(stacked_Xs[:, j])
            std_deviations_of_Xs.append(std_dev)

        data["For function"].append(fitness_function.name)
        data["Number of params"].append(fitness_function.dim)
        data["N"].append(self.SearchAgents_no)
        data["I"].append(self.Max_iter)
        data["Param 'PSRs'"].append(0.34)
        data["Param 'S'"].append(0.88)
        data["Found minimum"].append(np.round(best_X, 5).tolist())
        data["Goal function best value"].append(np.round(best_y, 5))
        data["Goal function worst value"].append(np.round(np.max(curr_ys), 5).tolist())
        data["Standard deviation of the parameters"].append(
            np.round(std_deviations_of_Xs, 2).tolist()
        )
        data["Standard deviation of the goal function value"].append(
            np.round(np.std(curr_ys), 2).tolist()
        )
        data["Coefficient of variation of goal function value"].append(
            np.round(np.std(curr_ys) / np.mean(curr_ys) * 100, 2).tolist()
        )
        return data

import numpy as np
import numpy.matlib
from scipy.special import gamma


def levy(n, m, beta):
    num = gamma(1 + beta) * np.sin(np.pi * beta / 2)  # Used for Numerator
    den = gamma((1 + beta) / 2) * beta * 2 ** ((beta - 1) / 2)  # Used for Denominator

    sigma_u = (num / den) ** (1 / beta)  # Standard deviation

    u = np.random.normal(0, sigma_u, (n, m))
    v = np.random.normal(0, 1, (n, m))

    z = u / (np.abs(v) ** (1 / beta))

    return z


def initialization(SearchAgents_no, dim, ub, lb):
    Positions = np.zeros((SearchAgents_no, dim))
    if len(ub) == 1 and len(lb) == 1:
        Positions = np.random.rand(SearchAgents_no, dim) * (ub - lb) + lb
    else:
        for i in range(dim):
            ub_i = ub[i]
            lb_i = lb[i]
            Positions[:, i] = np.random.rand(SearchAgents_no) * (ub_i - lb_i) + lb_i

    return Positions


def GOA2(SearchAgents_no, Max_iter, test_function):
    dim = test_function.dim
    Top_gazelle_pos = np.zeros(dim)
    Top_gazelle_fit = np.inf
    stepsize = np.zeros((SearchAgents_no, dim))
    fitness = np.inf * np.ones(SearchAgents_no)

    gazelle = initialization(SearchAgents_no, dim, test_function.ub, test_function.lb)
    Xmin = np.tile(np.ones(dim) * test_function.lb, (SearchAgents_no, 1))
    Xmax = np.tile(np.ones(dim) * test_function.ub, (SearchAgents_no, 1))

    Iter = 0
    PSRs = 0.34
    S = 0.88
    s = np.random.rand()

    while Iter < Max_iter:
        for i in range(gazelle.shape[0]):
            Flag4ub = gazelle[i, :] > test_function.ub
            Flag4lb = gazelle[i, :] < test_function.lb
            gazelle[i, :] = (
                (gazelle[i, :] * ~(Flag4ub + Flag4lb))
                + test_function.ub * Flag4ub
                + test_function.lb * Flag4lb
            )
            fitness[i] = test_function.fobj(gazelle[i, :])

            if fitness[i] < Top_gazelle_fit:
                Top_gazelle_fit = fitness[i]
                Top_gazelle_pos = gazelle[i, :]

        if Iter == 0:
            fit_old = fitness.copy()
            Prey_old = gazelle.copy()

        Inx = fit_old < fitness
        Indx = np.tile(Inx[:, np.newaxis], (1, dim))
        gazelle = Indx * Prey_old + ~Indx * gazelle
        fitness = Inx * fit_old + ~Inx * fitness

        fit_old = fitness.copy()
        Prey_old = gazelle.copy()

        Elite = np.tile(Top_gazelle_pos, (SearchAgents_no, 1))
        CF = (1 - Iter / Max_iter) ** (2 * Iter / Max_iter)
        RL = 0.05 * levy(SearchAgents_no, dim, 1.5)
        RB = np.random.randn(SearchAgents_no, dim)

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
            Flag4ub = gazelle[i, :] > test_function.ub
            Flag4lb = gazelle[i, :] < test_function.lb
            gazelle[i, :] = (
                (gazelle[i, :] * ~(Flag4ub + Flag4lb))
                + test_function.ub * Flag4ub
                + test_function.lb * Flag4lb
            )
            fitness[i] = test_function.fobj(gazelle[i, :])

            if fitness[i] < Top_gazelle_fit:
                Top_gazelle_fit = fitness[i]
                Top_gazelle_pos = gazelle[i, :]

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
            U = np.random.rand(SearchAgents_no, dim) < PSRs
            gazelle = gazelle + CF * (
                (Xmin + np.random.rand(SearchAgents_no, dim) * (Xmax - Xmin)) * U
            )
        else:
            r = np.random.rand()
            Rs = gazelle.shape[0]
            stepsize = (PSRs * (1 - r) + r) * (
                gazelle[np.random.permutation(Rs), :]
                - gazelle[np.random.permutation(Rs), :]
            )

        Iter = Iter + 1

    return Top_gazelle_fit, Top_gazelle_pos

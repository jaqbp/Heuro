# implementation of IStateWriter and IStateReader
from algorithms.base import IStateWriter
from algorithms.base import IStateReader
import numpy as np


class StateWriter(IStateWriter):
    def save_to_file_state_of_algorithm(self, algo, n_iteration, path: str):
        # Metoda zapisująca do pliku tekstowego stan algorytmu.
        # Stan algorytmu: numer iteracji, liczba wywołań funkcji celu,
        # populacja wraz z wartością funkcji dopasowania.
        with open(path, "w") as f:
            print(algo.xbest, algo.fbest)
            f.write(
                f"{n_iteration} {algo.number_of_evaluation_fitness_function} {algo.SearchAgents_no} {algo.fbest}\n"
            )
            for i in range(len(algo.xbest)):
                f.write(f"{algo.xbest[i]} ")


class StateReader(IStateReader):
    def load_from_file_state_of_algorithm(self, path: str):
        # Metoda wczytująca z pliku stan algorytmu.
        # Stan algorytmu: numer iteracji, liczba wywołań funkcji celu,
        # populacja wraz z wartością funkcji dopasowania.

        with open(path, "r") as f:
            data = f.read()
            iter, eval, pop, fbest = data.split("\n")[0].split(" ")
            iter = int(iter)
            eval = int(eval)
            pop = int(pop)
            # numpy float
            fbest = np.float64(fbest)
            xbest = data.split("\n")[len(data.split("\n")) - 1].split(" ")
            xbest.pop()
            xbest = np.array(xbest)
        return iter, eval, pop, fbest, xbest

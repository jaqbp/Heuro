# implementation of IStateWriter and IStateReader
from algorithms.base import IStateWriter
from algorithms.base import IStateReader
import numpy as np


class StateWriter(IStateWriter):
    def save_to_file_state_of_algorithm(self, algo, n_iteration, path: str):
        # Metoda zapisująca do pliku tekstowego stan algorytmu.
        # Stan algorytmu: numer iteracji, liczba wywołań funkcji celu,
        # populacja wraz z wartością funkcji dopasowania.
        previous_state = ""
        try:
            with open(path, "r") as f:
                previous_state = f.read()
        except FileNotFoundError:
            pass

        with open(path, "w") as f:
            f.write(
                f"{n_iteration} {algo.number_of_evaluation_fitness_function} {algo.SearchAgents_no}\n"
            )
            if previous_state != "":
                f.write(previous_state.split("\n", 1)[1])
                f.write("\n")
            for i in range(len(algo.xbest)):
                f.write(f"{algo.xbest[i]} ")
            f.write(f"{algo.fbest}")

        # with open(path, "r") as f_read:
        #     lines = f_read.readlines()[1:]

        # with open(path, "a") as f_append:
        #     f_append.writelines(lines)


class StateReader(IStateReader):
    def load_from_file_state_of_algorithm(self, path: str):
        # Metoda wczytująca z pliku stan algorytmu.
        # Stan algorytmu: numer iteracji, liczba wywołań funkcji celu,
        # populacja wraz z wartością funkcji dopasowania.

        with open(path, "r") as f:
            data = f.read()
            iter, eval, pop = data.split("\n")[0].split(" ")
            iter = int(iter)
            eval = int(eval)
            pop = int(pop)
            xbest = data.split("\n")[len(data.split("\n")) - 1].split(" ")
            fbest = xbest.pop()
            fbest = float(fbest)
            xbest = np.array(xbest).astype(float)
        return iter, eval, pop, fbest, xbest

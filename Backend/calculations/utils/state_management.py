# implementation of IStateWriter and IStateReader
from algorithms.base import IStateWriter
from algorithms.base import IStateReader


class StateWriter(IStateWriter):
    def save_to_file_state_of_algorithm(self, n_iteration, path: str):
        # Metoda zapisująca do pliku tekstowego stan algorytmu.
        # Stan algorytmu: numer iteracji, liczba wywołań funkcji celu,
        # populacja wraz z wartością funkcji dopasowania.
        with open(path) as f:
            f.write(f"{n_iteration} {self.number_of_evaluation_fitness_function} {self.SearchAgents_no} {self.xbest} {self.fbest}\n")


class StateReader(IStateReader):
    def load_from_file_state_of_algorithm(self, path: str):
        """
        Metoda wczytująca z pliku stan algorytmu.
        Stan algorytmu: numer iteracji, liczba wywołań funkcji celu,
        populacja wraz z wartością funkcji dopasowania.
        """
        with open(path, "r") as f:
            data = f.read().strip('\n')
        return data.split(' ')

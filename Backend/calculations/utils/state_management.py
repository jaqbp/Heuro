# implementation of IStateWriter and IStateReader
from algorithms.base import IStateWriter


class StateWriter(IStateWriter):
    def save_to_file_state_of_algorithm(self, path: str):
        # Metoda zapisująca do pliku tekstowego stan algorytmu.
        # Stan algorytmu: numer iteracji, liczba wywołań funkcji celu,
        # populacja wraz z wartością funkcji dopasowania.

        return

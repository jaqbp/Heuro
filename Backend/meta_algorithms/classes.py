# tutaj dodamy klasy abstrakcyjne, w oparciu o nie będziemy tworzyć obiekty odpowiednich algorymów
from abc import ABC, abstractmethod


class IStateWriter(ABC):
    @abstractmethod
    def save_to_file_state_of_algorithm(self, path: str):
        """
        Metoda zapisująca do pliku tekstowego stan algorytmu.
        Stan algorytmu: numer iteracji, liczba wywołań funkcji celu,
        populacja wraz z wartością funkcji dopasowania.
        """
        pass


class IStateReader(ABC):
    @abstractmethod
    def load_from_file_state_of_algorithm(self, path: str):
        """
        Metoda wczytująca z pliku stan algorytmu.
        Stan algorytmu: numer iteracji, liczba wywołań funkcji celu,
        populacja wraz z wartością funkcji dopasowania.
        """
        pass


class IGeneratePDFReport(ABC):
    @abstractmethod
    def generate_report(self, path: str):
        """
        Tworzy raport w określonym stylu w formacie PDF.
        W raporcie powinny znaleźć się informacje o:
        najlepszym osobniku wraz z wartością funkcji celu,
        liczbie wywołań funkcji celu,
        parametrach algorytmu.
        """
        pass


class IGenerateTextReport(ABC):
    @abstractmethod
    def report_string(self) -> str:
        """
        Zwraca raport w postaci łańcucha znaków.
        W raporcie powinny znaleźć się informacje o:
        najlepszym osobniku wraz z wartością funkcji celu,
        liczbie wywołań funkcji celu,
        parametrach algorytmu.
        """
        pass

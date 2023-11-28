# tutaj dodamy klasy abstrakcyjne, w oparciu o nie będziemy tworzyć klasy odpowiednich algorymów
from abc import ABC, abstractmethod
from typing import Callable, List
import numpy as np
import numpy.matlib
from scipy.special import gamma
import os


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


class ParamInfo:
    def __init__(self, name, description, upper_boundary, lower_boundary):
        self._name = name
        self._description = description
        self._upper_boundary = upper_boundary
        self._lower_boundary = lower_boundary

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    @property
    def upper_boundary(self):
        return self._upper_boundary

    @upper_boundary.setter
    def upper_boundary(self, value):
        self._upper_boundary = value

    @property
    def lower_boundary(self):
        return self._lower_boundary

    @lower_boundary.setter
    def lower_boundary(self, value):
        self._lower_boundary = value


class IOptimizationAlgorithm(ABC):
    def __init__(self):
        self._name = None
        self._params_info = None
        self._writer = None
        self._reader = None
        self._string_report_generator = None
        self._pdf_report_generator = None
        self._xbest = None
        self._fbest = None
        self._number_of_evaluation_fitness_function = None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def params_info(self):
        return self._params_info

    @params_info.setter
    def params_info(self, value):
        self._params_info = value

    @property
    def writer(self):
        return self._writer

    @writer.setter
    def writer(self, value):
        self._writer = value

    @property
    def reader(self):
        return self._reader

    @reader.setter
    def reader(self, value):
        self._reader = value

    @property
    def string_report_generator(self):
        return self._string_report_generator

    @string_report_generator.setter
    def string_report_generator(self, value):
        self._string_report_generator = value

    @property
    def pdf_report_generator(self):
        return self._pdf_report_generator

    @pdf_report_generator.setter
    def pdf_report_generator(self, value):
        self._pdf_report_generator = value

    @property
    def xbest(self):
        return self._xbest

    @xbest.setter
    def xbest(self, value):
        self._xbest = value

    @property
    def fbest(self):
        return self._fbest

    @fbest.setter
    def fbest(self, value):
        self._fbest = value

    @property
    def number_of_evaluation_fitness_function(self):
        return self._number_of_evaluation_fitness_function

    @number_of_evaluation_fitness_function.setter
    def number_of_evaluation_fitness_function(self, value):
        self._number_of_evaluation_fitness_function = value

    @abstractmethod
    def solve(
        self,
        fitness_function: Callable,
        domain: List[List[float]],
        parameters: List[float],
    ):
        """
        Metoda rozwiązująca problem optymalizacji.
        Przyjmuje funkcję celu, dziedzinę i listę parametrów.
        """
        pass

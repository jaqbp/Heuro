from ObjectiveFunction import ObjectiveFunction
import math
import numpy as np
from time import time
from concurrent.futures import ProcessPoolExecutor, as_completed


best_y = math.inf

def calculate_and_print(x1, x2, x3):
    y = of.FunkcjaCelu.Wartosc(x1, x2, x3)
    if y < best_y:
        print(f"Znaleziono lepszy punkt: ({x1}, {x2}, {x3}) -> {y}")
        return y
    return best_y

if __name__ == "__main__":
    of = ObjectiveFunction()

    # Obliczenie wartości w dowolnym punkcie
    # y = of.FunkcjaCelu.Wartosc(1.26, 1.3, 1.1)
    # print(f"Wartość funkcji w punkcie (1.26, 1.3, 1.1) wynosi: {y}")

    # Wartość referencyjna dla trzech jedynek
    # y2 = of.FunkcjaCelu.Wartosc(1.0, 1.0, 1.0)
    # print(f"Wartość funkcji w punkcie (1.0, 1.0, 1.0) wynosi: {y2}")

    # Optymalizacja w przedziałach [0.5, 1.5] dla każdego z parametrów
    start = time()
    number_of_intervals = 2 
    domain = np.linspace(0.5, 1.5, number_of_intervals)
    print(f"Liczba iteracji: {number_of_intervals ** 3}")
    print("Przedziały: ", list(domain))
    with ProcessPoolExecutor() as executor:
        results = []
        for x1 in domain:
            for x2 in domain:
                for x3 in domain:
                    results.append(executor.submit(calculate_and_print, x1, x2, x3))
        for future in as_completed(results):
            best_y = min(best_y, future.result())
    print(f"Najlepsza wartość funkcji: {best_y}")
    print(f"Czas wykonania: {time() - start} s")



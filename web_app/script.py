from collections import defaultdict
from algorithms.goa import GOA
from utils.get_function_obj import test_function_callbacks
import pandas as pd

"""
Skrypt do zapisywania wyników do pliku Excela.
"""

if __name__ == "__main__":
    N = [10, 20, 40, 80]
    I = [5, 10, 20, 40, 80]
    TESTS = 10

    data = defaultdict(list)
    for idx, test_function_callback in enumerate(test_function_callbacks):
        test_func = test_function_callback()
        for n in N:
            for i in I:
                goa_algorithm = GOA(SearchAgents_no=n, Max_iter=i)
                data = goa_algorithm.calculate_function_data(
                    test_func, [0.34, 0.88], TESTS, data
                )
        print(
            f'N: {data["N"][idx]}, I: {data["I"][idx]}\nbest_y: {data["Goal function best value"][idx]}\nbest_X: {data["Found minimum"][idx]}\n\n'
        )
    df = pd.DataFrame(data)
    df.to_excel("output.xlsx", index=False)
    print(df)

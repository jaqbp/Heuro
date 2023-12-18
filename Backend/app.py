from flask import Flask, render_template, request, jsonify
import importlib
import os
import sys

PARENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PARENT_DIR)

from GOA.main import calculate_function_data, test_functions

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/details", methods=["GET", "POST"])
def details():
    if request.method == "POST":
        data = request.json
        values1 = data["values1"]
        values2 = data["values2"]
        values3 = data["values3"]
        values4 = data["values4"]
        return f"Wartość 1: {values1}, Wartość 2: {values2}, Wartość 3: {values3}, Wartość 4: {values4} odebrane przez Flask"
    return render_template("details.html")


@app.route("/calculations", methods=["POST"])
def calculations():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid data"}), 400

    # Stworzenie obiektów funckji testowych wybranych przez użytkownika
    # Stworzenie obiektu algorytmu
    # Wywołanie metody solve na obiekcie algorytmu z odpowiednimi parametrami i funkcją testową
    # Zwrócenie wyniku w formacie JSON
    # Przykład
    # dla wybranych funckji testowych wykonać w pętli:
    # test_function = RastriginFunction(lb=np.array([-5.12]), ub=np.array([5.12]), dim=10)
    # tutaj na razie tylko jeden algorytm:
    # goa_algorithm = GOA(SearchAgents_no=20, Max_iter=10)
    # best_fitness, best_position = goa_algorithm.solve(
    #     test_function,
    #     domain=[test_function.lb, test_function.ub],
    #     parameters=[0.34, 0.88],
    # )
    # print("Best Fitness: ", best_fitness)
    # print("Best Position: ", best_position)
    # return jsonify({"best_fitness": best_fitness, "best_position": best_position}), 200

    pass


@app.route("/generate_text_report", methods=["POST"])
def generate_text_report():
    # Logika generowania raportu tekstowego, analogia do interfejsu IGenerateTextReport
    try:
        req = request.json
        functionId = req["functionId"]
        algorithmId = req["algorithmId"]
        test_function = [f for f in test_functions if f.id == functionId][0]
        data = {
            "For function": [],
            "Number of params": [],
            "N": [],
            "I": [],
            "Param 'PSRs'": [],
            "Param 'S'": [],
            "Found minimum": [],
            "Goal function best value": [],
            "Goal function worst value": [],
            "Standard deviation of the parameters": [],
            "Standard deviation of the goal function value": [],
            "Coefficient of variation of goal function value": [],
        }
        N = [10, 20, 40, 80]
        I = [5, 10, 20, 40, 80]
        TESTS = 10
        calculate_function_data(N, I, data, TESTS, test_function)
        return jsonify({"response": data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/add_function", methods=["POST"])
def add_function():
    data = request.json
    function_name = data["functionName"]
    function_code = data["functionCode"]

    # Tutaj zapisz kod funkcji w odpowiednim miejscu
    # i/lub dynamicznie załaduj ją do aplikacji

    # Przykład dynamicznego ładowania (uproszczony i wymaga ostrożności)
    module_name = f"dynamic_functions.{function_name}"
    file_path = f"dynamic_functions/{function_name}.py"
    with open(file_path, "w") as file:
        file.write(function_code)

    # Dodanie ścieżki do sys.path, jeśli to konieczne
    if file_path not in sys.path:
        sys.path.append(file_path)

    # Dynamiczne załadowanie modułu
    try:
        module = importlib.import_module(module_name)
        # Przykład wywołania funkcji z załadowanego modułu
        result = module.some_function()  # Użyj odpowiedniej funkcji
        return jsonify({"message": "Funkcja dodana pomyślnie", "result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


class ParamInfo:
    def __init__(self, name, description, upperBoundary, lowerBoundary):
        self.name = name
        self.description = description
        self.upperBoundary = upperBoundary
        self.lowerBoundary = lowerBoundary


if __name__ == "__main__":
    app.run(debug=True)

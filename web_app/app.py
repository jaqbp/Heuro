from flask import Flask, redirect, render_template, request, jsonify, session, url_for
import importlib
import sys

from goa_archive.main import calculate_function_data, test_functions

app = Flask(__name__)
app.secret_key = "secret_key"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/details")
def details():
    return render_template("details.html")


@app.route("/add_details", methods=["POST"])
def add_details():
    data = request.get_json()
    values1 = data["values1"]
    values2 = data["values2"]
    values3 = data["values3"]
    values4 = data["values4"]
    print(values1, values2, values3, values4)
    return jsonify({"message": "Wartości dodane pomyślnie"}), 200


@app.route("/add_function_and_algorithm", methods=["POST"])
def add_function_and_algorithm():
    body = request.get_json()
    if not body or "functionId" not in body or "algorithmId" not in body:
        return jsonify({"error": "Invalid request body"}), 400

    # Now for simplicity just one id
    print(dict(session.items()))
    session["functionId"] = body["functionId"]
    session["algorithmId"] = body["algorithmId"]
    return jsonify({"message": "Funkcja i algorytm dodane pomyślnie"}), 200


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
    try:
        json = request.get_json()
        domain = int(json["domain"])
        dimension = int(json["dimension"])
        numberOfIterations = int(json["numberOfIterations"])
        population = int(json["population"])
        functionId = int(session.get("functionId"))
        algorithmId = int(session.get("algorithmId"))
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
        TESTS = 10
        calculate_function_data(
            population, numberOfIterations, data, TESTS, test_function
        )
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
from flask import Flask, render_template, request, jsonify, session
import importlib
import sys
import os
from algorithms.goa import GOA
from utils.get_function_obj import get_function_obj

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
        test_function = get_function_obj(dimension, domain, functionId)
        goa_algorithm = GOA(SearchAgents_no=population, Max_iter=numberOfIterations)
        TESTS = 10
        data = goa_algorithm.calculate_function_data(test_function, [0.34, 0.88], TESTS)
        os.remove(f"{test_function.name}_{population}.txt")
        return jsonify({"response": data}), 200
    except Exception as e:
        print(str(e))
        return jsonify({"error": str(e)}), 400


@app.route("/pause_calculations", methods=["POST"])
def pause_calculations():
    file_path = "pause.txt"
    try:
        if not os.path.exists(file_path):
            with open(file_path, "w") as file:
                file.write("pause")
            return jsonify({"message": "Obliczenia zatrzymane"}), 200
        else:
            return jsonify({"message": "Plik już istnieje"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/continue_calculations", methods=["POST"])
def continue_calculations():
    file_path = "pause.txt"
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return jsonify({"message": "Obliczenia kontynuowane"}), 200
        else:
            return jsonify({"message": "Plik nie istnieje"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


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

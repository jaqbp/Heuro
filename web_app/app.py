from flask import Flask, render_template, request, jsonify, session
import os
from algorithms.goa import GOA
from utils.get_function_obj import get_function_obj
from concurrent.futures import ProcessPoolExecutor
from time import time

app = Flask(__name__)
app.secret_key = "secret_key"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/details")
def details():
    return render_template("details.html")


@app.route("/get_function_and_algorithm", methods=["GET"])
def get_function_and_algorithm():
    functionIds = session.get("functionIds")
    algorithmIds = session.get("algorithmIds")
    if not functionIds or not algorithmIds:
        return jsonify({"error": "Brak wybranej funkcji lub algorytmu"}), 400

    return jsonify({"functionIds": functionIds, "algorithmIds": algorithmIds}), 200


@app.route("/add_function_and_algorithm", methods=["POST"])
def add_function_and_algorithm():
    body = request.get_json()
    if not body or "functionIds" not in body or "algorithmIds" not in body:
        return jsonify({"error": "Invalid request body"}), 400

    session["functionIds"] = body["functionIds"]
    session["algorithmIds"] = body["algorithmIds"]
    return jsonify({"message": "Funkcja i algorytm dodane pomyślnie"}), 200


def process_function_details(details, algorithm):
    functionId = int(details["id"])
    domain = int(details["domain"])
    dimension = int(details["dimension"])
    numberOfIterations = int(algorithm["numberOfIterations"])
    population = int(algorithm["population"])
    test_function = get_function_obj(dimension, domain, functionId)
    goa_algorithm = GOA(SearchAgents_no=population, Max_iter=numberOfIterations)
    TESTS = 10
    data = goa_algorithm.calculate_function_data(test_function, [0.34, 0.88], TESTS)
    os.remove(f"{test_function.name}_{population}.txt")
    return data


@app.route("/generate_text_report", methods=["POST"])
def generate_text_report():
    MULTIPROCESSING = True
    try:
        json = request.get_json()
        # [{id, domain, dimension}]
        functionsDetails = json["functionsDetails"]
        algorithmsDetails = json["algorithmsDetails"]
        algorithm = algorithmsDetails[0]

        start = time()
        if MULTIPROCESSING:
            with ProcessPoolExecutor() as executor:
                datas = executor.map(
                    process_function_details,
                    functionsDetails,
                    [algorithm] * len(functionsDetails),
                )
        else:
            datas = []
            for details in functionsDetails:
                data = process_function_details(details, algorithm)
                datas.append(data)
        print(f"Calculation took {round(time() - start, 3)} seconds")

        list_datas = list(datas)
        out_data = list_datas[0]
        for data in list_datas[1:]:
            for k, v in data.items():
                out_data[k].extend(v)
        print(out_data)
        return jsonify({"response": out_data}), 200
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


# @app.route("/add_function", methods=["POST"])
# def add_function():
# data = request.json
# function_name = data["functionName"]
# function_code = data["functionCode"]

# # Tutaj zapisz kod funkcji w odpowiednim miejscu
# # i/lub dynamicznie załaduj ją do aplikacji

# # Przykład dynamicznego ładowania (uproszczony i wymaga ostrożności)
# module_name = f"dynamic_functions.{function_name}"
# file_path = f"dynamic_functions/{function_name}.py"
# with open(file_path, "w") as file:
# file.write(function_code)

# # Dodanie ścieżki do sys.path, jeśli to konieczne
# if file_path not in sys.path:
# sys.path.append(file_path)

# # Dynamiczne załadowanie modułu
# try:
# module = importlib.import_module(module_name)
# # Przykład wywołania funkcji z załadowanego modułu
# result = module.some_function()  # Użyj odpowiedniej funkcji
# return jsonify({"message": "Funkcja dodana pomyślnie", "result": result})
# except Exception as e:
# return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)

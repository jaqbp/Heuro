from flask import Flask, render_template, request, jsonify
import os
import sys

PARENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PARENT_DIR)

from GOA.main import calculate_function_data, test_functions

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/save_state", methods=["POST"])
def save_state():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid data"}), 400

    print(data)

    return jsonify({"message": "Data saved successfully"}), 200


@app.route("/load_state", methods=["GET"])
def load_state():
    # Logika zapisu stanu z pliku tekstowego, analogia do interfejsu IStateReader
    pass


@app.route("/generate_pdf_report", methods=["POST"])
def generate_pdf_report():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid data"})

    # Logika generowania pliku PDF, analogia do intefejsu IGeneratePDFReport
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


class ParamInfo:
    def __init__(self, name, description, upperBoundary, lowerBoundary):
        self.name = name
        self.description = description
        self.upperBoundary = upperBoundary
        self.lowerBoundary = lowerBoundary


if __name__ == "__main__":
    app.run(debug=True)

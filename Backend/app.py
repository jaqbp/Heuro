from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/details", methods=['GET','POST'])
def details():
    if request.method == 'POST':
        data = request.json
        values1 = data['values1']
        values2 = data['values2']
        values3 = data['values3']
        values4 = data['values4']
        # print(f'Wartość 1: {values1}, Wartość 2: {values2}, Wartość 3: {values3}, Wartość 4: {values4} odebrane przez Flask')
        return f'Wartość 1: {values1}, Wartość 2: {values2}, Wartość 3: {values3}, Wartość 4: {values4} odebrane przez Flask'
    return render_template("details.html")

@app.route("/result")
def result():
    return render_template("result.html")

@app.route('/save_state', methods=['POST'])
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


@app.route("/generate_text_report", methods=["GET"])
def generate_text_report():
    # Logika generowania raportu tekstowego, analogia do interfejsu IGenerateTextReport
    pass


class ParamInfo:
    def __init__(self, name, description, upperBoundary, lowerBoundary):
        self.name = name
        self.description = description
        self.upperBoundary = upperBoundary
        self.lowerBoundary = lowerBoundary


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, request

app = Flask(__name__)

@app.route('/save_state', methods=['POST'])
def save_state():
    # Logika zapisu stanu do pliku tekstowego, analogia do interfejsu IStateWriter
    pass

@app.route('load_state', methods=['GET'])
def load_state():
    # Logika zapisu stanu z pliku tekstowego, analogia do interfejsu IStateReader
    pass

@app.route('/generate_pdf_report', methods=['POST'])
def generate_pdf_report():
    # Logika generowania pliku PDF, analogia do intefejsu IGeneratePDFReport
    pass

@app.route('/generate_text_report', methods=['GET'])
def generate_text_report():
    # Logika generowania raportu tekstowego, analogia do interfejsu IGenerateTextReport
    pass

class ParamInfo:
    def __init__(self, name, description, upperBoundary, lowerBoundary):
        self.name = name
        self.description = description
        self.upperBoundary = upperBoundary
        self.lowerBoundary = lowerBoundary
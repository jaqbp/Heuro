const testFunctions = [
  {
    id: 0,
    name: "Funkcja Rastrigina",
    formula: "f(x) = A * n + ∑ (x_i^2 - A * cos(2 * π * x_i))",
  },
  {
    id: 1,
    name: "Funkcja Bukina N.6",
    formula: "f(x, y) = 100 * √|y - 0.01*x^2| + 0.01*|x + 10|",
  },
  {
    id: 2,
    name: "Funkcja Rosenbrocka",
    formula: "f(x, y) = ∑(100 * (x_i+1 - x_i^2)^2 + (1 - x_i)^2)",
  },
];

const algorithms = [
  { id: 0, name: "Algorytm genetyczny" },
  { id: 1, name: "Optymalizacja rojem cząstek (PSO)" },
  { id: 2, name: "Algorytm mrówkowy (ACO)" },
  { id: 3, name: "Algorytm optymalizacji kolonii nietoperzy" },
];

const selectedFunctions = new Set();
const selectedAlgorithms = new Set();

const generateReportButton = document.getElementsByClassName(
  "generate-report-btn",
)[0];

const appendCheckboxToParent = (parent, id, text, checkboxValue, type) => {
  const label = document.createElement("label");
  const checkbox = document.createElement("input");
  checkbox.type = "checkbox";
  checkbox.value = checkboxValue;
  checkbox.addEventListener("change", (e) => {
    const checked = e.currentTarget.checked;
    if (type === "function") {
      checked
        ? selectedFunctions.add({ id, text })
        : selectedFunctions.delete({ id, text });
    } else {
      checked
        ? selectedAlgorithms.add({ id, text })
        : selectedAlgorithms.delete({ id, text });
    }
    displaySelectedOptions();
  });

  label.appendChild(checkbox);
  label.appendChild(document.createTextNode(text));
  parent.appendChild(label);
};

// Funkcja do generowania listy funkcji testowych
function generateTestFunctionsList() {
  const listContainer = document.getElementById("test-functions-list");

  testFunctions.forEach((func) =>
    appendCheckboxToParent(
      listContainer,
      func.id,
      ` ${func.name} - ${func.formula}`,
      func.name,
      "function",
    ),
  );
}

// Funkcja do generowania listy algorytmów
function generateAlgorithmsList() {
  const listContainer = document.getElementById("algorithms-list");

  algorithms.forEach((algo) =>
    appendCheckboxToParent(
      listContainer,
      algo.id,
      ` ${algo.name}`,
      algo.name,
      "algorithm",
    ),
  );
}

// Funkcja do zbierania informacji o wybranych opcjach
function displaySelectedOptions() {
  const selectedFunctionsWrapper =
    document.getElementById("selected-functions");
  selectedFunctionsWrapper.replaceChildren(
    ...[...selectedFunctions].map((f) => {
      const p = document.createElement("p");
      p.className = "text text--small";
      p.textContent = f.text;
      return p;
    }),
  );

  const selectedAlgorithmsWrapper = document.getElementById(
    "selected-algorithms",
  );
  selectedAlgorithmsWrapper.replaceChildren(
    ...[...selectedAlgorithms].map((a) => {
      const p = document.createElement("p");
      p.className = "text text--small";
      p.textContent = a.text;
      return p;
    }),
  );
}

function generateHTML(data) {
  const tableHeader = Object.keys(data.response)
    .map((k) => `<th>${k}</th>`)
    .join("");

  const tableRows = data.response[
    "Coefficient of variation of goal function value"
  ]
    .map((_, rowIndex) => {
      return `<tr>${Object.values(data.response)
        .map((columnData) => `<td>${columnData[rowIndex]}</td>`)
        .join("")}</tr>`;
    })
    .join("");

  const tableStyles = `
  <style>
    table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 20px;
    }

    th, td {
      border: 1px solid #dddddd;
      padding: 8px;
      text-align: left;
    }

    th {
      background-color: #f2f2f2;
    }
  </style>
`;

  return `
  <html>
    <head>
      <title>Your Generated HTML Page</title>
      ${tableStyles}
    </head>
    <body>
      <table>
        ${tableHeader}
        ${tableRows}
      </table>
    </body>
  </html>
  `;
}

generateReportButton.addEventListener("click", async () => {
  try {
    generateReportButton.disabled = true;
    generateReportButton.innerText = "Generowanie raportu...";
    console.log("start");
    const res = await fetch("http://127.0.0.1:5000/generate_text_report", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        functionId: [...selectedFunctions].map((f) => f.id)[0],
        algorithmId: [...selectedAlgorithms].map((a) => a.id)[0],
      }),
    });
    const data = await res.json();
    console.log(data);
    const html = generateHTML(data);
    const blob = new Blob([html], { type: "text/html" });
    const url = URL.createObjectURL(blob);
    window.location.href = url;
  } catch (err) {
    console.log(err);
  } finally {
    generateReportButton.disabled = false;
    generateReportButton.innerText = "Generuj raport";
  }
});

// Wywołanie funkcji generujących listy po załadowaniu strony
window.onload = function () {
  generateTestFunctionsList();
  generateAlgorithmsList();
};

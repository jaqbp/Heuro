const testFunctions = [
  {
    name: "Funkcja Rastrigina",
    formula: "f(x) = A * n + ∑ (x_i^2 - A * cos(2 * π * x_i))",
  },
  {
    name: "Funkcja Bukina N.6",
    formula: "f(x, y) = 100 * √|y - 0.01*x^2| + 0.01*|x + 10|",
  },
  {
    name: "Funkcja Rosenbrocka",
    formula: "f(x, y) = ∑(100 * (x_i+1 - x_i^2)^2 + (1 - x_i)^2)",
  },
  { name: "Funkcja Kwadratowa", formula: "f(x) = x^2" },
];

const algorithms = [
  { name: "Algorytm genetyczny" },
  { name: "Optymalizacja rojem cząstek (PSO)" },
  { name: "Algorytm mrówkowy (ACO)" },
  { name: "Algorytm optymalizacji kolonii nietoperzy" },
];

const selectedFunctions = new Set();
const selectedAlgorithms = new Set();

const appendCheckboxToParent = (parent, text, checkboxValue, type) => {
  const label = document.createElement("label");
  const checkbox = document.createElement("input");
  checkbox.type = "checkbox";
  checkbox.value = checkboxValue;
  checkbox.addEventListener("change", (e) => {
    const checked = e.currentTarget.checked;
    if (type === "function") {
      checked ? selectedFunctions.add(text) : selectedFunctions.delete(text);
    } else {
      checked ? selectedAlgorithms.add(text) : selectedAlgorithms.delete(text);
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
      p.textContent = f;
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
      p.textContent = a;
      return p;
    }),
  );
}


// Wywołanie funkcji generujących listy po załadowaniu strony
window.onload = function () {
  generateTestFunctionsList();
  generateAlgorithmsList();
};

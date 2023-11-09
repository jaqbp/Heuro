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

// Funkcja do generowania listy funkcji testowych
function generateTestFunctionsList() {
  const listContainer = document.getElementById("test-functions-list");
  testFunctions.forEach(function (func) {
    const label = document.createElement("label");
    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.value = func.name;

    label.appendChild(checkbox);
    label.appendChild(
      document.createTextNode(` ${func.name} - ${func.formula}`),
    );
    listContainer.appendChild(label);
  });
}

// Funkcja do generowania listy algorytmów
function generateAlgorithmsList() {
  const listContainer = document.getElementById("algorithms-list");
  algorithms.forEach(function (algo) {
    const checkbox = document.createElement("input");
    const label = document.createElement("label");
    checkbox.type = "checkbox";
    checkbox.value = algo.name;

    label.appendChild(checkbox);
    label.appendChild(document.createTextNode(` ${algo.name}`));
    listContainer.appendChild(label);
  });
}

// Funkcja do zbierania informacji o wybranych opcjach
function displaySelectedOptions() {
  const selectedFunctions = [];
  const selectedAlgorithms = [];

  // Zbierz wybrane funkcje testowe
  document
    .querySelectorAll("#test-functions-list input:checked")
    .forEach(function (checkbox) {
      const func = testFunctions.find((f) => f.name === checkbox.value);
      if (func) {
        selectedFunctions.push(`${func.name}: ${func.formula}`);
      }
    });

  // Zbierz wybrane algorytmy
  document
    .querySelectorAll("#algorithms-list input:checked")
    .forEach(function (checkbox) {
      selectedAlgorithms.push(checkbox.value);
    });

  // Wyświetl wybrane opcje
  document.getElementById("selected-functions").innerText =
    selectedFunctions.join("\n");
  document.getElementById("selected-algorithms").innerText =
    selectedAlgorithms.join("\n");
}

document
  .querySelector(".forward-button")
  .addEventListener("click", displaySelectedOptions);

// Wywołanie funkcji generujących listy po załadowaniu strony
window.onload = function () {
  generateTestFunctionsList();
  generateAlgorithmsList();
};

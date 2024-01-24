import { testFunctions, algorithms } from "./consts.js";

const selectedFunctions = [];
const selectedAlgorithms = [];

const continueButton = document.getElementsByClassName("continue-btn")[0];

const appendCheckboxToParent = (parent, id, text, checkboxValue, type) => {
  const label = document.createElement("label");
  const checkbox = document.createElement("input");
  checkbox.type = "checkbox";
  checkbox.value = checkboxValue;
  checkbox.addEventListener("change", (e) => {
    const checked = e.currentTarget.checked;
    if (type === "function") {
      checked
        ? selectedFunctions.push({ id, text })
        : selectedFunctions.splice(selectedFunctions.indexOf({ id, text }), 1);
    } else {
      checked
        ? selectedAlgorithms.push({ id, text })
        : selectedAlgorithms.splice(
            selectedAlgorithms.indexOf({ id, text }),
            1,
          );
    }
    if (selectedFunctions.length > 0 && selectedAlgorithms.length > 0) {
      continueButton.disabled = false;
    } else {
      continueButton.disabled = true;
    }
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

continueButton.addEventListener("click", async () => {
  const res = await fetch("http://127.0.0.1:5000/add_function_and_algorithm", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      functionIds: selectedFunctions.map((f) => f.id),
      algorithmIds: selectedAlgorithms.map((a) => a.id),
    }),
  });

  if (!res.ok) {
    throw new Error("Error while selecting functions and algorithms");
  }

  window.location.href = "/details";
});

// Wywołanie funkcji generujących listy po załadowaniu strony
window.onload = function () {
  generateTestFunctionsList();
  generateAlgorithmsList();
};

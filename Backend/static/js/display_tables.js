const testFunctions = [
    { name: "Funkcja Rastrigina", formula: "f(x) = A * n + ∑ (x_i^2 - A * cos(2 * π * x_i))" },
    { name: "Funkcja Bukina N.6", formula: "f(x, y) = 100 * √|y - 0.01*x^2| + 0.01*|x + 10|" },
    { name: "Funkcja Rosenbrocka", formula: "f(x, y) = ∑(100 * (x_i+1 - x_i^2)^2 + (1 - x_i)^2)" },
    { name: "Funkcja Kwadratowa", formula: "f(x) = x^2" }
  ];
  
  const algorithms = [
    { name: "Algorytm genetyczny" },
    { name: "Optymalizacja rojem cząstek (PSO)" },
    { name: "Algorytm mrówkowy (ACO)" },
    { name: "Algorytm optymalizacji kolonii nietoperzy" }
  ];
  
  // Funkcja do generowania listy funkcji testowych
  function generateTestFunctionsList() {
    const listContainer = document.getElementById('test-functions-list');
    testFunctions.forEach(function(func) {
      const label = document.createElement('label');
      const checkbox = document.createElement('input');
      checkbox.type = 'checkbox';
      checkbox.value = func.name;
      
      const text = document.createTextNode(` ${func.name} - ${func.formula}`);
      
      label.appendChild(checkbox);
      label.appendChild(text);
      listContainer.appendChild(label);
    });
  }
  
  // Funkcja do generowania listy algorytmów
  function generateAlgorithmsList() {
    const listContainer = document.getElementById('algorithms-list');
    algorithms.forEach(function(algo) {
      const label = document.createElement('label');
      const checkbox = document.createElement('input');
      checkbox.type = 'checkbox';
      checkbox.value = algo.name;
      
      const text = document.createTextNode(` ${algo.name}`);
      
      label.appendChild(checkbox);
      label.appendChild(text);
      listContainer.appendChild(label);
    });
  }
  
  // Wywołanie funkcji generujących listy po załadowaniu strony
  window.onload = function() {
    generateTestFunctionsList();
    generateAlgorithmsList();
  };